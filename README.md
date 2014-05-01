piScheduler
===========

###piSchedule is an python extention for pilight

   Installed on RaspberryPI together with [pilight](http://www.pilight.org/) it supports time scheduled
   switching of devices.
   
   Switching uses pilight calls
```
         http:// + server + ':' + port + message
```
####   Parameters 
__server__ and __port__ have to be stored in a file named __piSchedule.prefs.json__

__message__ is build in consistence with the pilight-config definitions
      and are stored in a JSON file and holds ```location```, ```devices``` and ```time with state on/off```
      
The JSON file name can be passed to piSchedule as an argument or if
   omitted the file is assumed to be stored in the same directory with 
   the name but with extension '.json'. 

__Calling__ `python ./piSchedule.py (piSchedule.json)`


####   Installation
  
**piSchedule** runs on the Raspberry and needs the following **python** utilities:
   
- For a flexible **date/time** handling [dateutil](http://labix.org/python-dateutil/) is used. It includes a praser, so simple formatted date/time can be transformed to a full date/time object.
   
- The scheduling works with [Advanced Scheduler](https://pypi.python.org/pypi/APScheduler/2.1.2)
   
- **Sunrise/Sunset** switching is calculated with [ephem](https://pypi.python.org/pypi/ephem/3.7.5.1)

For installation details see also the [PyPI - the Python Package Index](https://pypi.python.org/pypi)
