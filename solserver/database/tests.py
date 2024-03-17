from django.test import TestCase
from django.contrib.auth.models import User
from .models import SolMate
from .consumers import SolServerConsumer, ClientConsumer
from .serializers import SolMateSerializer
from channels.testing import WebsocketCommunicator
import datetime
import time
import math
import json
from django.urls import reverse
from django.urls import resolve

import logging
logger = logging.getLogger('general')


class TestSolServerConsumer(TestCase):
    """Test Websocket connection, message and disconnection behaviour, as well as database integration."""

    def setUp(self):
        """Logging"""
        logger.info(f'Starts another test in {self.__class__.__name__}.')

    async def test_http_routing(self):
        """Coro: Views route to expected urls and vice versa."""
        url = reverse('index')
        test1 = url == '/'
        resolver = resolve('/')
        test2 = resolver.view_name == 'index'
        assert test1
        assert test2
        return [test1, test2]


    async def test_connection_response(self):
        """Coro: Websocket Connection to the server is set up correct and the response is as expected."""
        communicator = WebsocketCommunicator(SolServerConsumer.as_asgi(), "update/")
        connected, subprotocol = await communicator.connect()
        assert connected
        response = await communicator.receive_from()
        response = json.loads(response)
        assert response['type'] == "INFO"
        assert response['message'] == "Welcome to SMART-Server - SolMate Real-Time ObServer! - SolServerConsumer: groups ['updates']"


    async def test_update_response(self):
        """Coro: The response upon an update message is as expected."""
        communicator = WebsocketCommunicator(SolServerConsumer.as_asgi(), "update/")
        await communicator.connect()
        welcome_response = await communicator.receive_from()
        now = datetime.datetime.now()
        id_code = "0203:1234:"
        updt_msg = id_code + json.dumps({"_local_time":str(now),"power_inject":340})
        await communicator.send_to(json.dumps({
            'type':'UPDT',
            'message': updt_msg
            }))
        response = await communicator.receive_from()
        response = json.loads(response)
        assert response['type'] == "INFO"
        assert response['message'] == f"{id_code}OK"
       

    async def test_update_database_and_performance(self):
        """TODO Coro: This test ought to send a command to a SolMate instance to alter a value. 
        After that it checks the database if this value was adapted adequately.
        Furthermore it checks the speed of the communication."""
        test_value_1 = 240.943
        test_value_2 = 23.9
        assert True


    async def test_disconnect_behaviour(self):
        """Coro: Closing the websocket connection runs without errors."""
        communicator = WebsocketCommunicator(SolServerConsumer.as_asgi(), "update/")
        connected, subprotocol = await communicator.connect()
        assert connected
        try:
            await communicator.disconnect()
            assert True
        except Exception as e:
            logger.critical(f'Failed to disconnect, error: {e}')
            assert False


class TestClientConsumer(TestCase):
    """Test Websocket connection, message and disconnection behaviour, as well as database integration, querying and filtering."""
    SN = '1234'
    SW = 'v1.0'
    CT = 'us'
    PC = '8020'
    PIN = 150.55
    PIJ = 250.89
    PCO = 300.12
    BT = 92.5
    SV = 'v2'
    PV = 2

    def setUp(self):
        """Set up in-memory-database and populate with 5 examplary entries. Creates example user."""
        logger.info(f'Starts another test in {self.__class__.__name__}.')
        # Create a user
        test_user = User.objects.create_user(
            username='EET', password='EET')
        test_user.save()
        for i in range(5):
            if i%2 == 0:
                solm_vers = 'v1'
                pv_conn = 1
            else:
                solm_vers = self.SV
                pv_conn = self.PV
            solmate = SolMate.objects.create(
                serial_number = str(int(self.SN) + i),
                software_version = self.SW,
                country = self.CT,
                postcode = self.PC,
                owner = test_user,
                power_income = self.PIN + (i * 15),
                power_inject = self.PIJ + (i * 20),
                power_consumption = self.PCO - (i * 10),
                battery = self.BT - (5 * i),
                solmate_version = solm_vers,
                pv_connectors = pv_conn,
                )
            solmate.save()


    async def test_connection_response(self):
        """Coro: Websocket Connection to the server is set up correct and the response is as expected."""
        communicator = WebsocketCommunicator(ClientConsumer.as_asgi(), "update/")
        connected, subprotocol = await communicator.connect()
        assert connected
        response = await communicator.receive_from()
        response = json.loads(response)
        assert response['type'] == "INFO"
        assert response['message'] == "Welcome to SMART-Server - SolMate Real-Time ObServer! - ClientConsumer: groups ['broadcast']"


    async def test_sorting_command_processing(self):
        """Coro: Returns correct sorting string."""
        name_1,cond_1,value_1 = ["A","<","abc"]
        name_2,cond_2,value_2 = ["A",">","123"]
        name_3,cond_3,value_3 = ["A","^","abc"]
        sorting_conditions = await ClientConsumer().interpret_sorting_conditionals(name_1,cond_1,value_1)
        assert sorting_conditions == "A"
        sorting_conditions = await ClientConsumer().interpret_sorting_conditionals(name_2,cond_2,value_2)
        assert sorting_conditions == "-A"
        sorting_conditions = await ClientConsumer().interpret_sorting_conditionals(name_3,cond_3,value_3)
        assert sorting_conditions == "A"


    async def test_filter_command_processing(self):
        """Coro: Returns correct filter commands for django models."""
        test_names, test_conditionals, test_values = [["A","B","C","D","E","F","G","H"], ["<",">","<=",">=","==","=","^","FAIL"], [9.2,8.5,7.7,89.1,8.23,'icon','80',None]]
        filter_conditions = await ClientConsumer().interpret_filter_conditionals(test_names,test_conditionals,test_values)
        assert filter_conditions == {'A__lt': 9.2, 'B__gt': 8.5, 'C__lte': 7.7, 'D__gte': 89.1, 'E': 8.23, 'F__icontains': 'icon', 'G__startswith': '80', 'H': '80'}


    async def test_filter_response(self):
        """Coro: Filters single exact match correctly."""
        communicator = WebsocketCommunicator(ClientConsumer.as_asgi(), "client/")
        await communicator.send_to(json.dumps({
            'type':'FILT',
            'message':["filter:serial_number:=:1234","sort:serial_number:>:abc"]
            }))
        response = await communicator.receive_from()
        response = json.loads(response)
        assert response['type'] == "FILT"
        assert len(response['message']) == 1
        assert response["message"][0]['serial_number'] == '1234'


    async def test_filter_multiple_conditions(self):
        """Coro: Filters multiple conditions correctly."""
        communicator = WebsocketCommunicator(ClientConsumer.as_asgi(), "client/")
        await communicator.send_to(json.dumps({
            'type':'FILT',
            'message':['filter:power_inject:>=:300', 'filter:solmate_version:=:v2', 'filter:postcode:^:8', 'sort:serial_number:<:abc']
            }))
        response = await communicator.receive_from()
        response = json.loads(response)
        assert response['type'] == "FILT"
        assert len(response['message']) == 1
        assert response["message"][0]['serial_number'] == '1237'


    async def test_sorting(self):
        """Coro: Sorts according to specification."""
        communicator = WebsocketCommunicator(ClientConsumer.as_asgi(), "client/")
        await communicator.send_to(json.dumps({
            'type':'FILT',
            'message': ['filter:serial_number:=:1', 'sort:postcode:>:abc', 'sort:serial_number:>:abc']
            }))
        response = await communicator.receive_from()
        response = json.loads(response)
        assert response['type'] == "FILT"
        assert len(response['message']) == 5
        assert response["message"][0]['serial_number'] == '1238'
        assert response["message"][-1]['serial_number'] == '1234'
    
    async def test_distribute_uptdate(self):
        """TODO Test if updates got distributed to the appropriate consumer and groups."""
        assert True


class TestSolMateModel(TestCase):
    """Test database functionality and serializer for SolMate data."""
    SN = '1234'
    SW = 'v1.0'
    CT = 'us'
    PC = '0000'
    PIN = 100.55
    PIJ = 150.89
    PCO = 300.12
    BT = 92.5
    SV = 'v2'
    PV = 2
    USERNAME = 'EET'
    PASSWORD = 'EET'

    def setUp(self):
        """Set up in-memory-database with one SolMate entry. Creates example user."""
        logger.info(f'Starts another test in {self.__class__.__name__}.')
        # Create a user
        test_user = User.objects.create_user(
            username=self.USERNAME, password=self.PASSWORD)
        test_user.save()

        solmate = SolMate.objects.create(
            serial_number=self.SN,
            software_version = self.SW,
            country = self.CT,
            postcode = self.PC,
            owner = test_user,
            power_income = self.PIN,
            power_inject = self.PIJ,
            power_consumption = self.PCO,
            battery = self.BT,
            solmate_version = self.SV,
            pv_connectors = self.PV,
            )
        solmate.save()
    
    def test_db_existence(self):
        """Model exists."""
        solmates = SolMate.objects.all()
        test1 = len(solmates) == 1
        assert test1
        logger.info(f"{test1}: {self.test_db_existence.__doc__}")

    def test_data_integration(self):
        """Model Fields hold expected values."""
        solmate = SolMate.objects.get(serial_number=self.SN)
        assert solmate.software_version == self.SW
        assert solmate.country == self.CT
        assert solmate.postcode == self.PC
        user = solmate.owner
        assert user.username == self.USERNAME
        assert solmate.power_income == self.PIN
        assert solmate.power_inject == self.PIJ
        assert solmate.power_consumption == self.PCO
        assert solmate.battery == self.BT
        assert solmate.solmate_version == self.SV
        assert solmate.pv_connectors == self.PV

    def test_solmate_serializer(self):
        """Model serialisation works as expected. The owner field returns name instead of user id.""" 
        solmate = SolMate.objects.all()
        serializer = SolMateSerializer(solmate, many=True)
        data = json.loads(json.dumps(serializer.data))
        assert len(data) == 1
        assert data[0]['owner'] == self.USERNAME 

    def test_string_representation(self):
        """Model __str__ returns expected value."""
        solmate = SolMate.objects.get(serial_number=self.SN)
        assert solmate.__str__() == f"{solmate.serial_number} {solmate.owner.username}"

    def test_timestamp_valid(self):
        """Each data update leads to renewed timestamp."""
        solmate = SolMate.objects.get(serial_number=self.SN)
        last = solmate.last_status_update
        time.sleep(3)
        solmate.serial_number = self.SN # simulating update
        solmate.save()
        new = solmate.last_status_update
        delta = new - last
        delta_sec = delta.total_seconds()
        assert math.isclose(delta_sec, 3, abs_tol=1e-1)
        

if __name__ == '__main__':
    pass