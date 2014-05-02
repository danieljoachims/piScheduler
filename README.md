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
__server__ and __port__ have to be stored in a file named __piSchedule.prefs.json__

__message__ is build in consistence with the pilight-config definitions
      and holds ```location```, ```device``` and ```time with state on/off```
      
__time with state on/off__ defines the switching of the related 'device' and can a direct action (on/off) 
*OR* a string holding on/off state with the time when it has to be issued. Multiple actions for the same device can be written in one statement. Time can be relative or absolute with the possibility to have random offset or relation to *sunrise/sunset*. 

If date is obmitted from a time value it's assumed to be 'today'. Time value are checked for consistent, time values related to the pass are ignored.

      
All parameters for the _http_ call are stored in a JSON file, it's name can be passed to 'piSchedule.py' as an argument or if
   omitted the file is assumed to be stored in the same directory with the name but with extension '.json'. 


__Calling__ `python ./piSchedule.py [piSchedule.json]`


####   Installation
  
**piSchedule** runs on the Raspberry. **pilight** has be installed and needs to berunning.\n
piSchedule needs the following **python** utilities:
   
- For a flexible **date/time** handling [dateutil](http://labix.org/python-dateutil/) is used. It includes a praser, so simple formatted date/time can be transformed to a full date/time object.
   
- The scheduling works with [Advanced Scheduler](https://pypi.python.org/pypi/APScheduler/2.1.2)
   
- **Sunrise/Sunset** switching is calculated with [ephem](https://pypi.python.org/pypi/ephem/3.7.5.1)

For installation details see also the [PyPI - the Python Package Index](https://pypi.python.org/pypi)
