
# The SMART-OS Application is documented with MKDocs

## Start Up the Documentation Server

* `mkdocs serve -a 127.0.0.1:9000` 

Open a terminal and change your directory to the directory of this README.md file.

Now run the following commands in your terminal
```
pip install mkdocs
mkdocs serve -a 127.0.0.1:9000
```
Open your webbrowser and enter "127.0.0.1:9000" in your naviation bar.
Read the documentation thoroughly.

## MKDocs Reference

For full MKDocs documentation visit [mkdocs.org](https://www.mkdocs.org).

# Welcome to SMART-OS Doc
The SolMate Real-Time ObServer Documentation
[![Web Interface of SMART-OS](GUI-screenshot.png)](https://youtu.be/cNrweBXyBPA)
interactive interface with filter and sorting options. The data gets updated in Real-Time.

# Distinctiveness and Complexity
This project uses Asynchronous programming throughout at the back- and frontend. Concurrent programming is used to simulate multiple remote devices at the same machine.

This application does not require continuing client http requests to the server to keep all data updated in Real-Time. Hence this project adds a new level of complexity, performance and enriches the web-development skillset with another useful tool.  

Furthermore this project contains thorough testing capabilities.

The main focus of this project lies in the Real-Time and performant behaviour in data transmission, as well as data simulation. The data customisation is achieved via filter and sorting options.

This project has a real world application, when running the according lightweight python file on any remote device connected with the server. This is because this lightweight python file can easily be customized to represent data of personal interest, related to the machine which it runs on.

## No Social Network
To distuingish from a social network, this project has no ability to post or chat, alltough Django Channels is able to run a chat application very efficiently with Real-Time communication.

## No E-Commerce Site
To distinguish from a Commerce site this project does not contain any selling or buying functionality. 

## Utilizes Django
This App utilizes the Django Framework and makes use of its Channels module, the asynchronous websocket implementation in Django. 

## App is Mobile Responsive
This app has been successfully tested in a local network utilizing Raspberry Pi 4B as remote device (running the lightweight python file), while running the Django Channels Webserver on a computer within this network and accessing it with multiple client devices (Cellphone and laptop) at the same time. The application has been successfully tested with up to 267 simulated remote device instances, updating in Real-Time to the Server, distributed in Real-Time to all clients accessing the server via a browser.

# About SMART-OS
Updated as of 17.03.2024 

## Features
SMART-OS is an App to monitor Data from remote devices and display it in Real-Time publicly to a webserver. This may have an application in tracking device conditions after shipping like battery capacity, software version, power consumption, power generation of photovoltaik panels and keeping the exact geolocation for weather considerations.

### Webserver
The core is made up by a Django Channels server (utilizing asynchronous Daphne server, and a cache maintainance with Redis), enabling the Real-Time data distribution to all clients to this webserver, achieved via a simple GET request to the webservers root route. There is no restriction in accessing the data updates of all updating remote devices.

### Remote Devices
Updates are coming from all devices with active connection to the webserver network, running a single python file ("solmate.py"), stored on the trackable device. After startup it builds up and maintaines a websocket connection to the webserver, sending data only on change (observer pattern) to avoid data overload. By default data history is not stored, all data reflect only the latest updates without access to trends. The latest data received by the server is parallel stored to the database and distributed to all webserver clients. So the database, as well as all connected clients, are updated in Real-Time with the current device parameters. On connection loss the device attempts to reconnect in a defined time interval (default is five seconds). New devices can be automatically registered at the database upon first connection to the webserver. This has to be activated in the according file. 

### Logging
There is a thorough process logging upon startup for the webserver at "solserver/database/log/general.log", storing the latest 1 MB of logging entries. Besides testing procedures all messages towards the server are stored to this file. A data history can therefore be retrieved until this log file is overridden.

## Startup
Detailed information how to start up and test the webserver can be found at the section Start Up.

## TODOs
As any software also this has some potential for improvement and customisation:

* Authentication (device data restriction to owner).

* Pagination (limit results to 10-20 devices each page).

* Break Table (On smaller screen the table should be scrollable while handy to keep an overview).

* Dynamic table entries (Django models should adapt to the monitoring parameters defined by the remote devices - maybe via json file in database).

* Store data history and depict data trends for Machine Learning.

* Show 30 sec trend in GUI upon device click 

* change operating system to Linux for dockerisation and automated documentation. 

* Implement a CI/CD pipeline upon git commit (Each software change ought to be controlled via github actions testing and automated software update distribution to all devices).

* implement remote control for maintainance and software updates (setting parameter and/or runninng downloaded scripts).

* implement capability for IoT (each device should obtain all the data of all the other devices via implementing another channel to achieve this)




# Get started on WINDOWS OS
Before starting up be sure to meet all the system requirements as listed in the specifications section.

run the following command
to start the docker redis container:
```
docker run --rm -p 6379:6379 redis:7
```
#### Unit Testing and Integration Testing
in root/solserver/ directory,
Test the Django server via
```
python .\manage.py test --verbosity 3
```
#### Online Documentation
in root/solserver/ directory,
start the mkdocs server (default: 127.0.0.1:8000) via
```
mkdocs build
mkdocs serve
```
alternatively set an arbitrary Host IP:
```
mkdocs serve -a 192.168.0.192:9000
```
or
```
 mkdocs serve -a 127.0.0.1:9000
```

#### Startup the Django server
in root/solserver/ directory,
start the Django server on port 8080 via:
```
python .\manage.py runserver 127.0.0.1:8080
```
If you want to deploy the app on another Host,
adapt the Django settings.py file (ALLOWED_HOSTS) accordingly.
Also adapt the Host address (SERVER_URL) in the head section of
"root/solserver/solmate_emulation/solmate.py".
Avoid conflicting Port numbers for the mkdocs and the Django server.

#### Real-Time Data Funcitonal Testing 
For Real-Time Data Mimicing start an arbitrary number of SolMate instances.
Go to the root/solserver/solmate_emulation/ directory,
run the solmate.py file via:
```
python .\solmate.py
```
It leads you through a CLI to configure the number and the style of Real-Time Data Mimicing.
```
>>> Please Enter: How many SolMate instances? (<class 'int'>) <<< 
```
It expects you to enter an integer number for the number of emulated SolMate instances.
The System is tested with up to 267 devices at the same time. 

The following questions concern only the distribution of the values and frequency of the updates.
```
>>> Please Enter: Strict monoton behaviour? (y/n) <<< 
```
Enter 'n' to emulate random numbers.
Enter 'y' for emulating data following a function curve.
In the latter case you can choose between linear and sinuid behaviour:
```
>>> Please Enter: sinus curve behaviour? (y/n) <<< 
```
Enter 'n' for linear data behaviour.
Enter 'y' for the data to follow a sinus curve.

Then enter the maximum value for all the emulated data. 
The range goes from 0 - max value and the initial value is chosen randomly.
```
>>> Please Enter: maximum values? (<class 'int'>) <<< 
```
The following questions concern the frequency of data updates.
Enter an integer number to set  the minimum time for the randomly chosen
time between two data updates at the same device.
```
>>> Please Enter: minimum sleep time between two values? (<class 'int'>) <<< 
```
Finally, set the maximum value. 
The value is randomly chosen in this range for each iteration of data update.
```
>>> Please Enter: maximum sleep time between two values? (<class 'int'>) <<< 
```
By default, new devices, not yet registered in the database are not registered.
You can modify this behaviour in the solmate.py file.

## This Documentation is based on MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

### Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

### Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.


# SMART-OS technical details

!['SMART-OS Functional Diagram'](architecture.svg)

# Websocket Interfaces 
All updates are running over websocket connections. Each Remote Device builds up a websocket connection via python websockets module to the webserver

## Communication Protocol
Upon connection via websocket to the webserver root route the server may respond with a string like
```
{"type": "INFO", "message": "Welcome to SMART-Server - SolMate Real-Time ObServer! - SolServerConsumer: groups ['updates']"}
```
Note that the message is JSON formatted and consists of a key "type" and a key "message". The type may be one out of four different message types. 
```
types = ["INFO","FILT","INIT","UPDT"]
```
This type is used to identify how to process the message content.

The actual message is always a string, in the case of the welcome message it contains no info for further processing.
### Capping Identificator
For remote device identification and data integrity each message from the remote devices is a string and contains a capping identificator consisting of four digits Message-ID and the four digits device serial number, separated via a colon.
```
"0001:1234:{'parameter_name':'AT','_parameter_name':430}"
```
### Message Body
The body contains the parameters name and their respective value as a python dict (JSON format). Since the message is stringified in the first place, each message ought to be converted to valid python dict first. 

```
 ... {'parameter_name': 'AT', '_parameter_name': 430}
```
Note, that due to the observer pattern applied in the remote device script, some attributes may be named with a leading underscore throughout initialisation process, which comes into play when a remote device connects with the server for the first time. 

### Initialisation Messages
Upon first startup of Remote Devices, they may transmit a python dictionary with all their respective parameters in it, to give the webserver the possibility to write besides the dynamic parameters also all static parameters to the database models.

+ Typical Initial Message

```
{'type': 'INIT', 'message': '0000:0001:{"serial_number": "0001", "solmate_version": "v1", "_software_version": "v8.6", "_country": "DE", "_postcode": 7445, "_power_income": 377, "_power_inject": 336, "_power_consumption": 400, "_battery": 250, "_capacity": 5184000, "_local_time": null, "server_url": "ws://localhost:8000/update/", "websocket": "", "connected": true, "publish": true, "message_id": "0000", "message_queue": {}, "tasks": "", "meassuring": true, "charging": false, "injecting": false, "pv_connectors": 1}'}
```
Note that some of the parameter names have a leading underscore, allthough they may not during updating. This is because of the applied observer pattern within the remote device python script. It utilizes the inherent python class \_\_dict\_\_ attribute to obtain all parameters and their values for initialisation.

+ An Initial message may also look like

In default mode new devices are not sending an initialisation message as stated above. So the initial message of a remote device coming online may look like a simple update message.
```
{'type': 'UPDT', 'message': '0000:0001:{"battery": 350, "software_version": "v2.0", "country": "AT", "postcode": 9733, "power_income": 388, "power_inject": 357, "power_consumption": 289}'}
```
Note that there are no attributes with leading underline.

The receiving webserver has to distinguish between initialisation and update information, hence has to deal with parameters with and without a leading underscore.
## Messages from Remote Devices to the Webserver (Updating)
While running, upon attribute change any connected device will publish the new parameters in JSON format to the webserver via its websocket connection.

+ Valid Data Update from Remote Device
```
{'type': 'UPDT', 'message': '0116:0001:{"power_consumption": 357}'}
```
Note that the body may contain more than one parameters too. This depends on the bottom boundary for update interval and the frequency of attribute change. This can be set in the remote device python script.

+ Typical Server Response to the Remote Device
```
{"type": "INFO", "message": "0116:0001:OK"}
```
Note that the header is the same (message ID and device serial number), while the body contains "OK" if the update has been successfully received by the webserver. Otherwise the body would contain "ERROR".

## Messages from the Webserver to the Web-Client (Monitoring)

The Webserver either distributes data updates from remote devices via websocket connection to the frontend, responds to a filtering/sorting query via open websocket connection, or answers to an initial HTTP GET request.

+ Typical Response

```
{type: 'UPDT', message: '0008:0001:{"local_time": "2024-03-17 14:59:13.047108"}'}
```
The identificator type "UPDT" gives the necessary information to process the message body accordingly without initializing a new table at the frontend, and updates the according existing field, in this example the field "local_time" of device Serial number "0001".

## Messages from Web Clients to the Webserver (Filtering)
Any client successfully connecting its browser to the webserver address via GET request (to the main route) gets redirected to the index.html site. 
Upon loading a websocket connection to the server is created before the client obtains the full dataset out of the database via this websocket connection.

+ Valid JavaScript websocket connection definition

```
// Open websocket connection.
const ws = new WebSocket(
    "ws://"
    + window.location.host
    + '/client/'
);
```

+ Typical Server Response upon successfull websocket connection

```
{type: 'INFO', message: "Welcome to SMART-Server - SolMate Real-Time ObServer! - ClientConsumer: groups ['broadcast']"}
```
Additionally the client can apply filter and sorting options. These are asynchronously sent via websocket connection to the webserver and the filtered/sorted dataset is responded.

+ Valid Query

```
{"type":"FILT","message":["filter:serial_number:=:0","sort:serial_number:<:abc"]}
```
Note the identificator is "FILT", while the message contains a list of filter and sorting arguments. "filter:serial_number:=:0" stands for: Filter the database for all objects with "serial_number" attribute containing a string ("=") like "0". The response will than contain all devices with a four digit serial number containing a "0" character (i.e. "0001", "2032", "1009", "0023", etc.). The sorting argument "sort:serial_number:<:abc" stands for: Sorting for the "serial_number" in descending order ("<") with respect to the alphabet ("abc"). In fact it does not play a role if "abc" or "123" is applied, since the database will automatically consider either characters or numbers, respectively.

+ Typical Server Response
A typical response may be very large, depending on the number of devices within the database.
```
"{\"type\": \"INIT\", \"message\": [{\"serial_number\": \"0004\", \"software_version\": \"\", \"country\": \"\", \"postcode\": \"\", \"manufacturing_date\": \"2024-03-11T00:43:33.256667Z\", \"power_income\": 0.0, \"power_inject\": 0.0, \"power_consumption\": 144.0, \"battery\": 0.0, \"last_status_update\": \"2024-03-11T00:46:52.690962Z\", \"solmate_version\": \"v2\", \"pv_connectors\": 2, \"local_time\": \"2024-03-11T01:46:48.012456Z\", \"statusdata_ptr\": 467}]}"
```
Note that an initial database query, f.e. when filtering or initially connecting to the server via GET request (and consequently websocket connection), containes an identificator of type:"INIT".
This one is treated differently than uptdates (type="UPDT") by the frontend to generate the underlying tables accordingly. 


## Autotest Coverage
The results of the coverage report indicate an overall coverage for the autotesting framework of 84%.
Run the tests via 
```
python ./manage.py test
```
This ensures major functionality of the database and its serializer, and filtering/sorting functionality by the frontend, as well as the proper function of the Real-Time behaviour of the Django Channels framework.
```
Name                    
                                        Stmts   Miss  Cover
---------------------------------------------------------
database\__init__.py                      0      0   100%
database\admin.py                         3      0   100%
database\apps.py                          4      0   100%
database\consumers.py                   160     52    68%
database\migrations\0001_initial.py       7      0   100%
database\migrations\__init__.py           0      0   100%
database\models.py                       21      0   100%
database\routing.py                       3      3     0%
database\serializers.py                  11      0   100%
database\tests.py                       189      4    98%
database\urls.py                          3      0   100%
database\views.py                         8      2    75%
manage.py               
solserver\wsgi.py                         4      4     0%
---------------------------------------------------------
TOTAL                                   459     74    84%
```
""""

## System Requirements

This Application has been developed on WINDOWS OS and hence comes with its limitations.
Note that a Dockerized Redis Cache is utilized by default (running only on Linux) but can be circumvented via an in memory cache (see Django Channels Documentation). 
Otherwise Docker has to be preinstalled on your system to run this application.
The reqzuirements.txt file looks like the following.
```
asgiref==3.7.2
asttokens==2.4.1
async-timeout==4.0.3
attrs==23.2.0
autobahn==23.6.2
Automat==22.10.0
Babel==2.14.0
beautifulsoup4==4.12.3
bleach==6.1.0
certifi==2024.2.2
cffi==1.16.0
channels==4.0.0
channels-redis==4.2.0
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
comm==0.2.1
constantly==23.10.4
coverage==7.4.3
cryptography==42.0.5
daphne==4.1.0
debugpy==1.8.1
decorator==5.1.1
defusedxml==0.7.1
Django==5.0.3
djangorestframework==3.14.0
exceptiongroup==1.2.0
executing==2.0.1
factory-boy==3.3.0
Faker==24.1.0
fastjsonschema==2.19.1
ghp-import==2.1.0
gmplot==1.4.1
hyperlink==21.0.0
idna==3.6
incremental==22.10.0
iniconfig==2.0.0
ipykernel==6.29.3
ipython==8.22.2
jedi==0.19.1
Jinja2==3.1.3
jsonschema==4.21.1
jsonschema-specifications==2023.12.1
jupyter_client==8.6.0
jupyter_core==5.7.1
jupyterlab_pygments==0.3.0
jupytext==1.16.1
loguru==0.7.2
Mako==1.3.2
Markdown==3.5.2
markdown-it-py==3.0.0
MarkupSafe==2.1.5
matplotlib-inline==0.1.6
mdit-py-plugins==0.4.0
mdurl==0.1.2
mergedeep==1.3.4
mistune==3.0.2
mkdocs==1.5.3
mkdocs-dracula-theme==1.0.7
mkdocs-jupyter==0.24.6
mkdocs-material==9.5.13
mkdocs-material-extensions==1.3.1
msgpack==1.0.8
nbclient==0.9.0
nbconvert==7.16.2
nbformat==5.9.2
nest-asyncio==1.6.0
numpy==1.26.4
packaging==23.2
paginate==0.5.6
pandas==2.2.1
pandocfilters==1.5.1
parso==0.8.3
pathspec==0.12.1
pdoc3==0.10.0
pgeocode==0.4.1
platformdirs==4.2.0
pluggy==1.4.0
prompt-toolkit==3.0.43
psutil==5.9.8
pure-eval==0.2.2
pyasn1==0.5.1
pyasn1-modules==0.3.0
pycparser==2.21
Pygments==2.17.2
pymdown-extensions==10.7.1
pyOpenSSL==24.0.0
pytest==8.0.2
python-dateutil==2.9.0.post0
pytz==2024.1
pywin32==306
PyYAML==6.0.1
pyyaml_env_tag==0.1
pyzmq==25.1.2
redis==5.0.2
referencing==0.33.0
regex==2023.12.25
requests==2.31.0
rpds-py==0.18.0
service-identity==24.1.0
six==1.16.0
soupsieve==2.5
sqlparse==0.4.4
stack-data==0.6.3
tinycss2==1.2.1
toml==0.10.2
tomli==2.0.1
tornado==6.4
traitlets==5.14.1
Twisted==24.3.0
twisted-iocpsupport==1.0.4
txaio==23.1.1
typing_extensions==4.10.0
tzdata==2024.1
urllib3==2.2.1
watchdog==4.0.0
wcwidth==0.2.13
webencodings==0.5.1
websockets==12.0
win32-setctime==1.1.0
zope.interface==6.2
```



# Filestucture
The solserver project contains the single database app within this Django Channels Framework.
```
solserver
    |---database
    |   |---log
    |   |   |---general.log
    |   |
    |   |---migrations
    |   |   |--- "database specific ..."
    |   |   
    |   |---static
    |   |   |---database
    |   |   |   |---styles.css
    |   |
    |   |---templates
    |   |   |---database
    |   |   |   |---client.html
    |   |   |   |---index.html
    |   |     
    |   |---__init__.py
    |   |---admin.py
    |   |---apps.py
    |   |---consumer.py
    |   |---models.py
    |   |---routing.py
    |   |---serializers.py
    |   |---tests.py
    |   |---urls.py
    |   |---views.py
    |
    |---docs
    |   |--- "documentation via mkdocs ..."
    |   
    |---site   
    |   |--- "documentation via mkdocs ..."
    |
    |---solmate_emulation
    |   |---solmate.py
    |
    |---solserver
    |   |---__init__.py
    |   |---asgi.py
    |   |---settings.py
    |   |---urls.py
    |   |---wsgi.py
    |
    |---db.sqlite3
    |---LICENCE
    |---manage.py
    |---mkdocs.yml
    |---README.md
    |---requirements.txt

```
# __Python Backend__

## consumer.py
class SolServerConsumer()
```
## SolServerConsumer
"""Deals with websocket connections from SolMateInstances to HOST/'update/'. Accepts all connections."""

### connect
"""Coro: Called on websocket connection."""

### receive
"""Coro: Called with either text_data or bytes_data for each frame."""

### disconnect
"""Coro: Called when the socket closes."""

### update_database
"""Updating existing table in Database."""

### write_to_database
"""Creating new table in database."""

```
class ClientConsumer()
```
## ClientConsumer
"""Deals with websocket connection from browser clients to HOST/'client/'. Accepts all connections."""

### connect
"""Called on connection."""

### receive
"""Coro: Broadcasts database querysets depending on input filter- and sorting conditions.
        Expected unordered command input Syntax, like: ['filter:serial_number:=:0001','sort:serial_number:>:abc'] """
        # Called with either text_data or bytes_data for each frame.
        
### distribute_updates
"""Coro: broadcasts message transferred to this Consumers groups. Receives from SolServerConsumer."""
        
### interpret_sorting_conditionals
"""Coro: returns sorting conditionals string like '-serial_number'.
        interprets input syntax like: abc = alphabetic, 123 = numeric, "<" = small-big/a-z, ">" = big-small/z-a"""

### interpret_filter_conditionals
"""Coro: returns dict with combined filter conditions, according to input lists."""

### filter_database_sorted
"""Called on filter and sort websocket requests."""

### query_database
"""Called at Site refresh and initial websocket requests."""
```
## models.py
class ProductData()
```
## ProductData
"""Product Details."""
```
class StatusData()
```
## StatusData
"""Current SolMate Status."""
```
class SolMate()
```
## SolMate
"""Model SolMate."""

### __str__
"""Returns proper string representation."""
```
## routing.py
Handles the available websocket routs:

+ ".../update/"
    > SolServerConsumer

+ ".../client/"
    > ClientConsumer

## serializers.py
Serializer for the Model SolMate to return the model data with printed username.

## tests.py
class TestSolServerConsumer()
```
## TestSolServerConsumer
"""Test Websocket connection, message and disconnection behaviour, as well as database integration."""

### setUp
"""Logging"""

### test_http_routing
"""Coro: Views route to expected urls and vice versa."""

### test_connection_response
"""Coro: Websocket Connection to the server is set up correct and the response is as expected."""
        
### test_update_response
"""Coro: The response upon an update message is as expected."""
        
### test_update_database_and_performance
"""TODO Coro: This test ought to send a command to a SolMate instance to alter a value. 
        After that it checks the database if this value was adapted adequately.
        Furthermore it checks the speed of the communication."""
        

### test_disconnect_behaviour
        """Coro: Closing the websocket connection runs without errors."""
```
class TestClientConsumer()
```
## TestClientConsumer
"""Test Websocket connection, message and disconnection behaviour, as well as database integration, querying and filtering."""
    
### setUp
"""Set up in-memory-database and populate with 5 examplary entries. Creates example user."""
        
### test_connection_response
"""Coro: Websocket Connection to the server is set up correct and the response is as expected."""

### test_sorting_command_processing
"""Coro: Returns correct sorting string."""

### test_filter_command_processing
"""Coro: Returns correct filter commands for django models."""

### test_filter_response
"""Coro: Filters single exact match correctly."""
        
### test_filter_multiple_conditions
"""Coro: Filters multiple conditions correctly."""
        
### test_sorting
"""Coro: Sorts according to specification."""

### test_distribute_uptdate
"""TODO Test if updates got distributed to the appropriate consumer and groups."""
```
class TestSolMateModel()
```
## TestSolMateModel
"""Test database functionality and serializer for SolMate data."""
    
### setUp
"""Set up in-memory-database with one SolMate entry. Creates example user."""
        
### test_db_existence
"""Model exists."""

### test_data_integration
"""Model Fields hold expected values."""

### test_solmate_serializer
"""Model serialisation works as expected. The owner field returns name instead of user id.""" 

### test_string_representation
"""Model __str__ returns expected value."""

### test_timestamp_valid
"""Each data update leads to renewed timestamp."""
```
## urls.py
Handles the main route when initially connecting to the server via GET request

+ ".../" > index view

## views.py
function index()
```
## index
"""Handles GET requests to the main url. Redirects to index.html"""
```
## solmate.py
class SolMateBase()
```
## SolMateBase
 """Basic SolMate class, containing common functionality among all versions. 
    Utilizes setter methods to maintain status updates upon attribute change, rather than an interval."""
    

### __init__
"""Initialises the SolMateBase class. Starts up the state publishing asynchronously."""
        
### get_charged
"""Can get charged by PV panels."""

### meassure_power
"""Can measure the power consumption of the household, where they are plugged in."""
        
### inject_power
"""Can inject power into the grid."""

### connect
"""Coro: Opens websocket connection to the server url."""
        
### publish_state
 """Coro: Publishes changed states to websocket URL."""
        
```
class SolMate()
```
## SolMate
"""Version of SolMate."""

### __init__
"""Initialisation of SolMate instance."""

### switch_mode
"""Switches to next operating mode."""

### update_battery
"""Coro: Updates battery state."""

### get_charged
"""Can get charged by PV panels."""

### meassure_power
"""Can measure the power consumption of the household, where they are plugged in."""

### inject_power
"""Can inject power into the grid."""

### get_charged
"""Shadowing parent method. Mimicing handling of increased input charge due to second PV Panel Connector."""
        
### start_real_time_clock
"""Coro: Start displaying real time."""

### stop_real_time_clock
"""Coro: Stop displaying real time."""

### display_real_time
"""Coro: Mimicing a RTC (Real-Time-Clock)."""
```
function get_valid_user_input()
```
## get_valid_user_input
"""Queries user input and verifies if it is of the right data type. booleans are queried with (y/n)."""
``` 
function permute_parameter()
```
## permute_parameter
"""Permutes attributes of instance in a range with customizable behaviour."""
```
function main()
```
## main
"""Coro: Generates arbitrary number of Solmate Simulations, communicating via websocket with the SMART-OS."""
```

# __JavaScript/HTML/CSS Frontend__

## client.html
Contains the layout and rendering details within the header html section.

## index.html
Contains the HTML for Filter/Sorting functionality, dynamically modified and updated with JavaScript.

JavaScript is opening the websocket connection and maintaining all Real-Time updates at the frontend within the clients browser.

To adjust the visualisation of updates at the frontend one can set the ANIMATE_REALTIME_UPDATES variable to false, either manually or via GUI through a click on the related button.
```
let ANIMATE_REALTIME_UPDATES = true;
```
Details about the websocket connection can be explored in the Specifications section.
The JavaScript is mainly consisting of eventListener to deal with the user events.

function toDateIfDate()
```
### toDateIfDate
// Recognises a string as a date, if it is in a range of specific regular expressions and converts it to a Date if it is applicable.            
``` 

