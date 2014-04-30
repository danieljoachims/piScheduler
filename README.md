piScheduler
===========

###piSchedule is an python extention for pilight

   Installed on RaspberryPI together with [pilight](http://www.pilight.org/) it supports time scheduled
   switching of devices.
   
   Switching uses pilight calls
```
         http:// + server + ':' + port + message
```
   Parameters 
   __server__ and __port__ have to be stored in a file named __piSchedule.PARAM.json__
   
   __message__ is build in consistence with the pilight-config definitions
      and are stored in a JSON file and holds ```location```, ```devices``` and ```times with state on/off```
      
   The JSON file name can be passed to piSchedule as an argument or if
   omitted the file is assumed to be stored in the same directory with 
   the name but with extension '.json'. 


   __Calling__ `python ./piSchedule.py (piSchedule.json)`

   __date/time settings__
   To have a very flexible date/time handling piScheduler is using `http://labix.org/python-dateutil`. 
   That utility allows piSchedule to support a very brod range of date/time formats. 
   
   Also switching based on sunrise/sunset is possible. 'ephem' is used for that, for details see
    `http://rhodesmill.org/pyephem/`
