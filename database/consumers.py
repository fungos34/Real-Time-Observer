from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ProductData, StatusData, SolMate, User
from .serializers import SolMateSerializer
import json
import logging
logger = logging.getLogger('general')

class SolServerConsumer(AsyncWebsocketConsumer):
    """Deals with websocket connections from SolMateInstances to HOST/'update/'. Accepts all connections."""
    groups = ["updates"] # Consumer joining these groups.

    async def connect(self):
        """Coro: Called on websocket connection."""
        await self.accept()
        logger.info('SolMate connected over websocket.')
        await self.send(json.dumps({
            'type':'INFO',
            'message': f'Welcome to SMART-Server - SolMate Real-Time ObServer! - {self.__class__.__name__}: groups {self.groups}'
            }))


    async def receive(self, text_data=None, bytes_data=None):
        """Coro: Called with either text_data or bytes_data for each frame."""
        received = json.loads(text_data)
        message_id, serial_number, plain = received['message'].split(':',2)
        await self.send(
            text_data = json.dumps({
                "type": "INFO",
                "message": message_id + ':' + serial_number + ':' + "OK"
            }))
        logger.info(f'received: {received}')
        await self.channel_layer.group_send(
            "broadcast",  # Each Consumer part of this group needs the according event handler.
            {
                "type": "distribute_updates", # name of event handler function 
                "message": received # message
             }
        )
        if received['type'] == 'INIT':
            if not await self.write_to_database(serial_number, plain):
                await self.update_database(serial_number, plain)
        elif received['type'] == 'UPDT':
            if not await self.update_database(serial_number, plain):
                self.write_to_database(serial_number, plain)
        
    async def disconnect(self, close_code):
        """Coro: Called when the socket closes."""
        logger.info(f"Lost connection {self} with code {close_code}")


    @database_sync_to_async
    def update_database(self, serial_number, fields) -> bool:
        """Updating existing table in Database."""
        logger.debug('updating database.')
        fields = json.loads(fields)
        solmates = SolMate.objects.filter(serial_number = serial_number)
        # Deal with existing SolMate instances.
        if len(solmates) == 1:
            solmate = SolMate.objects.get(serial_number = serial_number)
            for name,value in fields.items():
                if hasattr(solmate, name):
                    setattr(solmate, name, value)
                    logger.debug(f'successfully set model {solmate.serial_number} field {name} to {value}')
                elif hasattr(solmate, str(name).replace('_','',1)):
                    # initially the parameter from solmate instances may stem from a __dict__ and hence contain a leading underscore.
                    setattr(solmate, str(name).replace('_','',1), value)
                    logger.debug(f'successfully set model {solmate.serial_number} field {str(name).replace("_","",1)} to {value}')
                else:
                    continue
            solmate.save()
        elif len(solmates) == 0:
            logger.debug(f'Failed to update table. SN {serial_number} does not exist. proceed with creating new table database!')
            return False
        else:
            logger.critical(f'Multiple similar entries in database SN {serial_number}, ID {[solmates[i].id for i in range(len(solmates))]}')
        return True

    @database_sync_to_async
    def write_to_database(self, serial_number, fields) -> bool:
        """Creating new table in database."""
        logger.debug('writing to database.')
        fields = json.loads(fields)
        solmates = SolMate.objects.filter(serial_number = serial_number)
        # Deal with existing SolMate instances.
        if len(solmates) == 1:
            logger.debug(f'Failed to create new table. SN {serial_number} already exists. proceed with database update!')
            return False
        # Deal with new SolMate instance.
        elif len(solmates) == 0:
            solmate = SolMate()
            solmate.serial_number = serial_number
            solmate.software_version = fields.get('_software_version')
            solmate.country = fields.get('_country')
            solmate.postcode = fields.get('_postcode')
            solmate.owner = User.objects.get(username = 'EET')
            solmate.power_income = fields['_power_income']
            solmate.power_inject = fields['_power_inject']
            solmate.battery = fields['_battery']
            solmate.solmate_version = fields['solmate_version']
            solmate.pv_connectors = fields["pv_connectors"]
            solmate.local_time = fields['_local_time']
            solmate.power_consumption = fields['_power_consumption']
            solmate.save()
        else:
            logger.critical(f'Multiple similar entries in database SN {serial_number}, ID {[solmates[i].id for i in range(len(solmates))]}')
        return True


class ClientConsumer(AsyncWebsocketConsumer):
    """Deals with websocket connection from browser clients to HOST/'client/'. Accepts all connections."""
    groups = ["broadcast"]

    async def connect(self):
        # Called on connection.
        await self.channel_layer.group_add(
            "broadcast", # self.room_group_name
            self.channel_name
        )
        await self.accept()
        logger.info('Client connected via Websocket.')
        await self.send(text_data=json.dumps({
                'type': 'INFO',
                'message': f'Welcome to SMART-Server - SolMate Real-Time ObServer! - {self.__class__.__name__}: groups {self.groups}'
            }))
        content_data = await self.query_database()
        await self.send(text_data=json.dumps({
                'type': 'INIT',
                'message': content_data
            }))


    async def receive(self, text_data: list[str] = {'type':'FILT','message':["filter:serial_number:=:0001","sort:serial_number:>:abc"]}, bytes_data = None) -> None:
        """Coro: Broadcasts database querysets depending on input filter- and sorting conditions.
        Expected unordered command input Syntax, like: ['filter:serial_number:=:0001','sort:serial_number:>:abc'] """
        # Called with either text_data or bytes_data for each frame.
        filter_names, filter_conditionals, filter_values = [], [], []
        combined_sorting_conditions = [] 
        text_data = json.loads(text_data)
        text_data = text_data['message']
        for i in range(len(text_data)):
            command, name, conditional, value = text_data[i].split(':')
            if command.lower() == 'filter':
                filter_names.append(name)
                filter_conditionals.append(conditional)
                filter_values.append(value)
            elif command.lower() == 'sort':
                sorting_condition = await self.interpret_sorting_conditionals(name, conditional, value)
                combined_sorting_conditions.append(sorting_condition)
            else:
                continue

        combined_filter_conditions = await self.interpret_filter_conditionals(filter_names,filter_conditionals, filter_values)
        content_data = await self.filter_database_sorted(combined_filter_conditions, combined_sorting_conditions)
        await self.send(text_data=json.dumps(
            {
                'type': 'FILT',
                'message': content_data
            }))

    async def distribute_updates(self, event):
        """Coro: broadcasts message transferred to this Consumers groups. Receives from SolServerConsumer."""
        message_incl_header = event['message']
        await self.send(text_data=json.dumps({
            'type': message_incl_header['type'],
            'message': message_incl_header['message'],
        }))

    async def interpret_sorting_conditionals(self, name: str = 'serial_number', conditional: str = '<', value: str = 'abc') -> str:
        """Coro: returns sorting conditionals string like '-serial_number'.
        interprets input syntax like: abc = alphabetic, 123 = numeric, "<" = small-big/a-z, ">" = big-small/z-a"""
        match conditional:
            case '<':
                prefix = ''
                sorting_name = str(name)
            case '>':
                prefix = '-'
                sorting_name = str(name)
            case _:
                logger.critical(f'Sorting conditional "{conditional}" unknown. Interpreted as "<".')
                prefix = ''
                sorting_name = str(name)
        sorting_conditions = f'{prefix}{sorting_name}'
        return sorting_conditions


    async def interpret_filter_conditionals(self, names: list[str], conditionals: list[str] = None, values: list[type] = None) -> dict:
        """Coro: returns dict with combined filter conditions, according to input lists."""
        filter_conditions = {}
        for i in range(len(conditionals)):
            match conditionals[i]:
                case '<':
                    postfix = '__lt'
                    value = float(values[i])
                case '>':
                    postfix = '__gt'
                    value = float(values[i])
                case '<=':
                    postfix = '__lte'
                    value = float(values[i])
                case '>=':
                    postfix = '__gte'
                    value = float(values[i])
                case '==' : # equality of numbers.
                    postfix = ''
                    value = float(values[i])
                case '=' : # equality of strings.
                    postfix = '__icontains'
                    value = str(values[i])
                case '^' :
                    postfix = '__startswith'
                    value = str(values[i])
                case _ :
                    logger.critical(f'Filtering conditional "{conditionals[i]}" unknown. Interpreted as "=".')
                    postfix = ''
            field_name = f'{names[i]}{postfix}'
            filter_conditions.update({field_name:value})
        return filter_conditions


    @database_sync_to_async
    def filter_database_sorted(self, filter_conditions: dict, sorting_conditions: list) -> str:
        """Called on filter and sort websocket requests."""
        solmates = SolMate.objects.filter(**filter_conditions).order_by(*sorting_conditions)
        content_serializer = SolMateSerializer(solmates, many=True)
        content_data = content_serializer.data
        return content_data


    @database_sync_to_async
    def query_database(self) -> str:
        """Called at Site refresh and initial websocket requests."""
        solmates = SolMate.objects.all()
        content_serializer = SolMateSerializer(solmates, many=True)
        content_data = content_serializer.data
        return content_data
        

        