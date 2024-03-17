import random
import asyncio
import datetime
from abc import ABC, abstractmethod
import websockets
from loguru import logger
import json
from typing import Literal
import sys
import math

SERVER_URL = 'ws://localhost:8000/update/' # 'ws://localhost:8080/update/' # 'ws://localhost:8000/update/' # 'ws://192.168.0.192:8000/update/'
PUBLISH_INITIALIZER = False # When set to True the initial message upon connection to the webserver contains information about initialisation of this device within the backend database.

class SolMateBase(ABC):
    """Basic SolMate class, containing common functionality among all versions. 
    Utilizes setter methods to maintain status updates upon attribute change, rather than an interval."""
    
    def __init__(self, serial_number: str, solmate_version: Literal['v1','v2']) -> None:
        """Initialises the SolMateBase class. Starts up the state publishing asynchronously."""
        self.serial_number = serial_number
        self.solmate_version = solmate_version

        self._software_version = "" # software version
        self._country = "" # country
        self._postcode = "" # postcode
        self._power_income = 0 # W - current power coming from the PV panels.
        self._power_inject = 0 # W - currently injected power from the SolMate into the grid.
        self._power_consumption = 0 # W - currently consumed power by the household.
        self._battery = 0 # % - state of charge of the battery
        self._capacity = 5184000
        self._local_time = None
        
        self.server_url = SERVER_URL
        self.websocket = websockets.WebSocketClientProtocol
        self.connected = False
        self.publish = True
        self.message_id = f'{0:04}'
        self.message_queue = {}

        self.tasks = []
        self.tasks.append(asyncio.create_task(self.publish_state(publish_initializer=PUBLISH_INITIALIZER)))

    @property
    def local_time(self):
        return self._local_time
    
    @local_time.setter
    def local_time(self, value):
        self._local_time = value
        self.message_queue.update({'local_time':value})


    @property
    def software_version(self):
        return self._software_version
    
    @software_version.setter
    def software_version(self, value):
        self._software_version = value
        self.message_queue.update({'software_version':value})

    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        self._country = value
        self.message_queue.update({'country':value})

    @property
    def postcode(self):
        return self._postcode
    
    @postcode.setter
    def postcode(self, value):
        self._postcode = value
        self.message_queue.update({'postcode':value})


    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        self.message_queue.update({'capacity':value})

    @property
    def battery(self):
        return self._battery
    
    @battery.setter
    def battery(self, value):
        self._battery = value
        self.message_queue.update({'battery':value})


    @property
    def power_income(self):
        return self._power_income
    
    @power_income.setter
    def power_income(self, value):
        self._power_income = value
        self.message_queue.update({'power_income':value})


    @property
    def power_inject(self):
        return self._power_inject
    
    @power_inject.setter
    def power_inject(self, value):
        self._power_inject = value
        self.message_queue.update({'power_inject':value})


    @property
    def power_consumption(self):
        return self._power_consumption
    
    @power_consumption.setter
    def power_consumption(self, value):
        self._power_consumption = value
        self.message_queue.update({'power_consumption':value})


    @abstractmethod
    def get_charged():
        """Can get charged by PV panels."""
        pass

    @abstractmethod
    def meassure_power():
        """Can measure the power consumption of the household, where they are plugged in."""
        pass
    
    @abstractmethod
    def inject_power():
        """Can inject power into the grid."""
        pass

    async def connect(self):
        """Coro: Opens websocket connection to the server url."""
        async with websockets.connect(self.server_url) as self.websocket:
            logger.info(f'SN:{self.serial_number} connected to "{self.server_url}"')
            self.connected = True
            while self.websocket.open:
                await asyncio.sleep(1)
        logger.info(f'SN:{self.serial_number} disconnected from "{self.server_url}"')
        self.connected = False

    async def publish_state(self, transmit: str = None, interval: int = None, publish_initializer: bool = False) -> None:
        """Coro: Publishes changed states to websocket URL."""
        while True:
            if len(self.message_queue) > 0:
                transmit = json.dumps(self.message_queue.copy())
                self.message_queue = {}
                while self.publish and self.connected:
                    try:
                        if publish_initializer:
                            if int(self.message_id) <= 1:
                                header = 'INIT'
                                initial = self.__dict__.copy()
                                initial["websocket"] = ''
                                initial["tasks"] = ''
                                transmit = json.dumps(initial)
                            else:
                                header = 'UPDT'
                        else:
                            header = 'UPDT'
                        message = self.message_id + ':' + str(self.serial_number) + ':' + transmit
                        outgoing = json.dumps({
                            'type': header,
                            'message': message
                        })
                        await self.websocket.send(outgoing)
                        logger.debug(f'>>> {json.loads(outgoing)}')
                        response = await asyncio.wait_for(self.websocket.recv(), 5)
                        logger.info(f'<<< {response}')
                    except Exception as e:
                        logger.info(str(self.message_id) + ':' + 'ERROR')
                        logger.debug(repr(e))
                    finally:
                        self.message_id = f'{(int(self.message_id) + 1):04}'
                        if interval != None:
                            await asyncio.sleep(interval)
                            continue
                        else:
                            break
            else:
                if self.publish and not self.connected:
                    self.tasks.append(asyncio.create_task(self.connect()))
                    await asyncio.sleep(5)
                await asyncio.sleep(0.2)
        


class SolMate(SolMateBase):
    """Version of SolMate."""
    
    def __init__(self, serial_number: str, solmate_version: Literal['v1','v2']) -> None:
        """Initialisation of SolMate instance."""
        super().__init__(serial_number, solmate_version)
        self.meassuring = True
        self.charging = False
        self.injecting = False
        
        self.meassure_power()
        # Version differentiation.
        if self.solmate_version.lower() == 'v1':
            self.pv_connectors = 1
        elif self.solmate_version.lower() == 'v2':
            self.display_rtc = False
            self.pv_connectors = 2
            self.tasks.append(asyncio.create_task(self.start_real_time_clock()))
        

    def switch_mode(self):
        """Switches to next operating mode."""
        if self.meassuring == True:
            self.charging = True
            self.meassuring = False
            self.injecting = False
            self.get_charged()
        elif self.charging == True:
            self.injecting = True
            self.charging = False
            self.meassuring = False
            self.inject_power()
        else:
            self.meassuring = True
            self.charging = False
            self.injecting = False
            self.meassure_power()

    async def update_battery(self):
        """Coro: Updates battery state."""
        while True:
            if self.charging:
                capacity = (self.capacity * (self.battery/100)) + self.power_income
                if (capacity/self.capacity) >= 1:
                    self.battery = 100
                else:
                    self.battery = (capacity/self.capacity) * 100
                
            elif self.injecting:
                capacity = (self.capacity * (self.battery/100)) - self.power_inject
                if (capacity/self.capacity) <=0:
                    self.battery = 0
                else:
                    self.battery = (capacity/self.capacity) * 100
            await asyncio.sleep(1)

    def get_charged(self):
        """Can get charged by PV panels."""
        self.power_income = 340 # W
        self.power_inject = 0
        self.power_consumption = 0

    def meassure_power(self):
        """Can measure the power consumption of the household, where they are plugged in."""
        self.power_income = 0
        self.power_inject = 0
        self.power_consumption = random.choice(range(150)) # W
    
    def inject_power(self):
        """Can inject power into the grid."""
        self.power_income = 0
        self.power_inject = 340 # W
        self.power_consumption = 0

    def get_charged(self):
        """Shadowing parent method. Mimicing handling of increased input charge due to second PV Panel Connector."""
        self.power_income = 340 * 2 # W
        self.power_inject = 0
        self.power_consumption = None


    async def start_real_time_clock(self):
        """Coro: Start displaying real time."""
        self.display_rtc = True
        await self.display_real_time()

    async def stop_real_time_clock(self):
        """Coro: Stop displaying real time."""
        self.display_rtc = False

    async def display_real_time(self):
        """Coro: Mimicing a RTC (Real-Time-Clock)."""
        reftime = datetime.datetime.now()
        while self.display_rtc:
            nowtime = datetime.datetime.now()
            if nowtime - reftime >= datetime.timedelta(seconds=15):
                reftime = nowtime
                self.local_time = str(nowtime)
            print(f'SN:{self.serial_number},ZIP:{self.postcode}, Local Time: {nowtime}')
            await asyncio.sleep(1)
    


# if __name__ == "__main__":
    # print(f'running {__file__}')
    # async def config(solmate):
    #     for i in range(10):
    #         solmate.switch_mode()
    #         print(solmate.power_consumption, solmate.power_income, solmate.power_inject)
    #         print(solmate.battery)
    #         await asyncio.sleep(random.choice(range(5)))

    # async def update(solmate):
    #     await solmate.update_battery()

    # async def main():
    #     solmate = SolMate('1234','v0.0','AT','8055')
    #     await asyncio.gather(
    #         config(solmate),
    #         update(solmate) 
    #                    )
        
    # asyncio.run(main())
            

def get_valid_user_input(input_info: str, expected_input_type: int|float|str|bool) -> int|float|str|bool:
    """Queries user input and verifies if it is of the right data type. booleans are queried with (y/n)."""
    while True:
        try:
            if expected_input_type == bool:
                value = input('>>> Please Enter: ' + input_info + ' (y/n) <<< ')
                if value.lower() == 'y':
                    return True
                elif value.lower() == 'n':
                    return False
                else:
                    continue
            else:
                value = input('>>> Please Enter: ' + input_info + ' (' + str(type(expected_input_type())) + ') <<< ')
                try:
                    return expected_input_type(value)
                except Exception:
                    print(f'Invalid input type.')
                    continue
        except KeyboardInterrupt as e:
            sys.exit(e)
    

async def permute_parameter(instance: type, attribute_name: str, strict_monotone_behaviour: bool = False, sin_curve: bool = True, value_range_max: int = 340, sleep_time_range_min: int  = 10, sleep_time_range_max: int  = 60):
    """Coro: Permutes attributes of instance in a range with customizable behaviour."""
    start_value = random.choice(range(0,value_range_max,1))
    counter = 0
    m = 0
    # infinite Loop.
    while True:
        n = 0
        m += 1
        # Strict monotone behaviour.
        if strict_monotone_behaviour:
            # Set inrease/decrease range parameters.
            counter += 1
            if counter % 2 == 0:
                step = -1
                end_value = 0
            else:
                step = 1
                end_value = value_range_max
            
            if sin_curve:
                value_range = range(start_value, end_value, step)
                curve_range = [round((math.sin((i+1)/len(value_range)) * (end_value-start_value)) + start_value) for i in range(len(value_range))]
            else:
                curve_range = range(start_value, end_value, step)
            values = iter(curve_range)
            # logger.critical(curve_range)

        # Range Loop.
        while True:
            n += 1
            # Either iterate over value range or choose a random one
            if strict_monotone_behaviour:
                try:
                    value = next(values)
                    start_value = value
                except StopIteration:
                    break
            else:
                value = random.choice(range(value_range_max))
                
            # New sleep time range for new decay/increase.
            sleep_range = random.choice(range(sleep_time_range_min, sleep_time_range_max, 1))

            # Set the attribute to a new value.
            setattr(instance, attribute_name, value)
            # logger.info(f'changed {attribute_name}: {value}')
            await asyncio.sleep(random.choice(range(sleep_range)))


async def main():
    """Coro: Generates arbitrary number of Solmate Simulations, communicating via websocket with the SMART-OS."""
    device_tasks = []
    solmates = []

    for i in range(number_solmates): # <= 250
        solmate = SolMate(f'{i+1:04}',random.choice(['v1','v2']))
        solmates.append(solmate)

    for i in range(len(solmates)):
        await asyncio.sleep(1)
        solmates[i].battery = random.choice(range(20))
        solmates[i].software_version = f'v{random.choice(range(0,9,1))}.{random.choice(range(0,9,1))}'
        solmates[i].country = random.choice(['AT','DE','CH','IT','SI'])
        solmates[i].postcode = random.choice(range(7000,9999,1))
        for attribute_name in ["power_income","power_inject","power_consumption","battery"]:
            device_tasks.append(asyncio.create_task(permute_parameter(solmates[i], attribute_name, monoton_behaviour, sin_behaviour, value_range_to, sleep_time_min, sleep_time_max)))
            [device_tasks.append(j) for j in solmates[i].tasks]

    await asyncio.gather(
        *device_tasks
    )



if __name__ == "__main__":
    print(f'Running {__file__}')

    # Configurations
    number_solmates = get_valid_user_input("How many SolMate instances?", int)
    monoton_behaviour = get_valid_user_input("Strict monoton behaviour?", bool)
    if monoton_behaviour:
        sin_behaviour = get_valid_user_input("sinus curve behaviour?", bool)
    else:
        sin_behaviour = False
    value_range_to = get_valid_user_input("maximum values?", int)
    sleep_time_min = get_valid_user_input("minimum sleep time between two values?", int)
    sleep_time_max = get_valid_user_input("maximum sleep time between two values?", int)
   
    # Start async eventloop
    asyncio.run(main())

