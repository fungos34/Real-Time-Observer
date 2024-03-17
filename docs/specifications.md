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