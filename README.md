piScheduler
===========

###piSchedule is an python extention for pilight

   Installed on RaspberryPI together with [pilight](http://www.pilight.org/) it supports time scheduled
   switching of devices and with calling
```
         http:// + server + ':' + port + message
```
   __server__ and __port__ have to be stored in a file named __piSchedule.HTTP.json__

   __message__ is build from location, devices and times with state on/off.
      Those details have to be consistent with the pilight-config definitions
      and are stored in a JSON file.
      The JSON file name can be passed to piSchedule as an argument or if
      omitted the file is assumed to be stored in the same directory with 
      the name but with extension '.json'. 


   __Calling__ `python ./piSchedule.py (piSchedule.json)`

   __date/time parsing__
     using `http://labix.org/python-dateutil`
