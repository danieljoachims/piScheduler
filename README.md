piScheduler
===========

###piSchedule is an python extension for pilight

   Installed on RaspberryPI together with [pilight](http://www.pilight.org/) it supports time scheduled
   switching of devices.
   
   Switching uses pilight calls
```
         http:// + server + ':' + port + message
```
####   Parameters 
__server__ and __port__ have to be stored in a file named *piSchedule.prefs.json*. That prefs file also hold the geo coordinates to be used for calculating _sunrise/sunset_.

__message__ is build in consistence with the pilight-config definitions
      and holds ```location```, ```device``` and ```time with state on/off```
      
__time with state on/off__ defines the switching of the related 'device' and can a direct action (on/off) 
*OR* a string holding on/off state with the time when it has to be issued. Multiple actions for the same device can be written in one statement. Time can be relative or absolute with the possibility to have random offset or relation to *sunrise/sunset*. 

If date is obmitted from a time value it's assumed to be 'today'. Time values are checked for consistent; time values related to the pass of piSchedule.py execution are ignored.

All time switching parameters are stored in a JSON file, it's name can be passed to 'piSchedule.py' as an argument or if omitted the file is assumed to be stored in the same directory with the same name but with extension '.json'. 


__Calling__ `python ./piSchedule.py [piSchedule.json]`


__Examples of the JSON files__
- [piSchedule.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.json)
- [piSchedule.prefs.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.prefs.json)


####   Installation
  
**piSchedule** runs on the Raspberry. **pilight** has be installed and needs to be running.

piSchedule uses the following **python** packages:
   
- For a flexible **date/time** handling [dateutil](http://labix.org/python-dateutil/). It includes a praser, so simple formatted date/time will be transformed to a full date/time object.
   
- The scheduling works with [Advanced Scheduler](https://pypi.python.org/pypi/APScheduler/2.1.2)
   
- **Sunrise/Sunset** switching is calculated with [ephem](https://pypi.python.org/pypi/ephem/3.7.5.1)



#####A brief installation overview of the required python packages
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
