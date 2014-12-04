*piSchedule*
==========

### *piSchedule* is a python extension for pilight

   Installed on RaspberryPI together with [pilight](http://www.pilight.org/) it supports time scheduled
   switching of devices.   

*piSchedule* runs on a terminal session and generates output with overview of the upcoming day schedule and writes also status details.   

A more convient use is to display and operate that output on a PC or also on mobile devices using a browser like Firefox. (See below __piSchedule with [Browser](#web)__)
   

### How it works
   *piSchedule* switches the devices using __pilight__ calls
```
    http:// + server + ':' + port + message
```

__server__ and __port__  are read from the pilight configuration file `config.json`. *piSchedule* uses the pilight port and the two next ports also.

__message__  is build in consistence with the pilight configuration and holds `device` and `switch` with state `on/off` with `time` values.

__switch__  defines the switching of the related 'device' and can be a direct action (on/off) *OR* a string holding on/off state with the time when it has to be issued. Multiple actions for the same device can be written with one statement. Time can be relative or absolute with the possibility to have *random offset* or relation to *sunrise/sunset*. 

If date is obmitted from a time value -- which is the 'normal' case -- it's assumed to be 'today'. Time values are checked for consistent; time values related to the past of the program execution are ignored, but flagged on the *piSchedule* console output.

###DaySchedule  
 A daily switching plan can be passed to *'piSchedule.py'*. The switch details are stored in a JSON or INI file, it's assumed to be stored in the same directory as *'piSchedule.py'*.

The daily switch plan (JSON/INI file) will be reloaded with day change including new values for sunrise/sunset and new random times if defined.

*See* `piSchedule.setup.MD'`  *for details about* `'piSchedule.json'/'piSchedule.ini'`

 ---------
##*Setup - piSchedule* before Starting  
 Before starting *piSchedule* two parameters has to be configured:     

_**Location**_ is used to calculate the geolocation parameters for the daily recalculation of *sunrise/sunset*.  

_**LogID**_ protects *piSchedule* and has to be used similar to a password at start up on the *web pages*.  
The setup is supported with a python program   
```
     piSetup.py Location='yourTown' LogID='yourIDcode'
```
 __*Note*__   
*The setup parameters are stored to a file* `piSchedule.prefs.json`. *The 'LogID' is hashed and only the hash is stored.*   
*To check your 'LogID' against the stored hash, use*
``` 
     piSetup.py hash='yourIDcode'
``` 
*instead.*


-------------
## Starting *piSchedule*
*piSchedule.py* has to be run on the RaspberryPI and will output to the console the current 'daySchedule' as well as other logging details.   

Starts with:   
``` 
    python piSchedule.py [piSchedule.json|piScedule.ini]`
``` 
It's recommended to run 'piSchedule.py' with **tmux**. Helpful in a RPI configuration without keyboard/terminal using a SSH connection.

---------------
##<a name="web"></a> *piSchedule* with Browser (PC and Smartphone)

After starting *piSchedule* on the console, a browser page can be used to monitor the *piSchedule* operation.   
The current implementation has

 *   __Open the web pages with 'LogID'__   
 ![pic1][pic1]   
[pic1]:https://dl.dropboxusercontent.com/u/35444930/piScheduler/home.png   

*   __Main Menu to select different functions__    
![pic2][pic2]
[pic2]:https://dl.dropboxusercontent.com/u/35444930/piScheduler/mainMenu.png   

 *   __List 'Day Schedule and Prefs' (Location, Sunrise/Sunset, Geocoordinates)__   
 ![pic3][pic3]
[pic3]:https://dl.dropboxusercontent.com/u/35444930/piScheduler/prefs%26jobs%28w%29.png

 *   __List the daily jobs excecuted already__    
![pic4][pic4]
[pic4]:https://dl.dropboxusercontent.com/u/35444930/piScheduler/dayList.png   

__*Note*__ *More functions on the web page to come ..*


---------------------


## *piConsole*
*piConsole* is used together with *piSchedule*. When *piSchedule* has been started *piConsole* can pass commands or the name of a day schedule file to *piSchedule*. That way additional switching instructions can be added and the current day schedule will be replaced by the new one with the next day change.
```
    ./piConsole.py [argument]
```
__'argument'__ follows the definition for 'piSchedule.ini' or 'piSchedule.json' files


---------------------

## Examples of the .JSON and .INI files

- [piSchedule.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.json)
- [piSchedule.ini](https://github.com/neandr/piScheduler/blob/master/piSchedule.ini)
- [piSchedule.prefs.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.prefs.json)

------------------

## Installation
  
**_piSchedule_** runs on the Raspberry.   
**_pilight_** is required to be installed and needs to be running.

**_piSchedule_** uses the following **python** packages:

- For a flexible **date/time** handling [dateutil]. It includes a praser, so simple formatted date/time will be transformed to a full date/time object.  
- The **Scheduling** works with **[Advanced Scheduler vers.3](https://pypi.python.org/pypi/APScheduler)**
- **Location/Geolocation/Sunrise/Sunset** switching is calculated with [ephem] and [geopy] 
- **LogID** will be hashed using [pbkdf2]
- **Web Pages** are supported with [bottle] and [bootstrap]
- **Multiprocessing/Threads** uses [multiprocessing] [threading]   
   
   
#### A brief installation overview of the required python packages
Installing python [pip](http://www.pip-installer.org/en/latest/installing.html)
```
- download $ get-pip.py to a working directory
- run  $ sudo python get-pip.py
```

Install python packages with pip

```
'dateutil': 
$ sudo pip install python-dateutil

'APScheduler'
$ sudo pip install apscheduler

'ephem'
$ sudo pip install ephem    (for python 3)
$ sudo pip install pyephem  (for python 2.x)
'geopy'
$ sudo pip install geopy

'pbkdf2'
$sudo pip install pbkdf2

'bottle'
$ sudo pip install bottle

'bootstrap'
That libs are referenced on the web page definition and loaded on request


```

For installation details see also the [PyPI - the Python Package Index](https://pypi.python.org/pypi)   


------------------
<p align='center'>Using <http://markable.in/editor/></p>
