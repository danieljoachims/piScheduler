piSchedule
==========

### piSchedule is an python extension for pilight

   Installed on RaspberryPI together with [pilight](http://www.pilight.org/) it supports time scheduled
   switching of devices.
   
   Switching uses pilight calls
```
    http:// + server + ':' + port + message
```
### Parameters 
__server__ and __port__  have to be stored in a file named *piSchedule.prefs.json*. That prefs file also hold the geo coordinates to be used for calculating _sunrise/sunset_.

__message__  is build in consistence with the pilight-config definitions
and holds `location`, `device` and `time with state on/off`

__time with state on/off__  defines the switching of the related 'device' and can a direct action (on/off) *OR* a string holding on/off state with the time when it has to be issued. Multiple actions for the same device can be written in one statement. Time can be relative or absolute with the possibility to have *random offset* or relation to *sunrise/sunset*. 

If date is obmitted from a time value it's assumed to be 'today'. Time values are checked for consistent; time values related to the past of piSchedule.py execution are ignored.

__DaySchedule__  
 A daily switching plan can be passed to 'piSchedule.py'. The switch details are stored in a JSON or INI file, it's assumed to be stored in the same directory as 'piSchedule.py'.

The daily switch plan (JSON/INI file) will be reloaded with day change including new values for sunrise/sunset and new random times if defined.

See
`piSchedule.setup.MD'`  for details about `'piSchedule.json'/'piSchedule.ini'`


### Calling
`python ./piSchedule.py [piSchedule.json|piScedule.ini]`

It's recommended to run 'piSchedule.py' with tmux. That way the current status of the daily switch plan can be recalled. Helpful in a RPI configuration without keyboard/terminal using a SSH connection.

### Examples of the .JSON and .INI files

- [piSchedule.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.json)
- [piSchedule.ini](https://github.com/neandr/piScheduler/blob/master/piSchedule.ini)
- [piSchedule.prefs.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.prefs.json)


### Installation
  
**piSchedule** runs on the Raspberry. **pilight** is required to be installed and needs to be running.

piSchedule uses the following **python** packages:
   
- For a flexible **date/time** handling [dateutil](http://labix.org/python-dateutil/). It includes a praser, so simple formatted date/time will be transformed to a full date/time object.
   
- The scheduling works with **[Advanced Scheduler vers.3](https://pypi.python.org/pypi/APScheduler)**
   
- **Sunrise/Sunset** switching is calculated with [ephem](https://pypi.python.org/pypi/ephem/3.7.5.1)



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
```

For installation details see also the [PyPI - the Python Package Index](https://pypi.python.org/pypi)
