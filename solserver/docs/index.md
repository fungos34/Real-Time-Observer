

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
