
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

