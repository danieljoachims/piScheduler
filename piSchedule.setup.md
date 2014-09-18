piSchedule.setup.md
===========

###piSchedule setup of switch time values

   Switching of devices with __piSchedule__ offers the following features:


   __Date/Time__
   
   The very flexible date/time handling is achieved with using [dateutil](http://labix.org/python-dateutil/). That utility allows piSchedule to support a very brod range of date/time formats. 
   
   __Time Delta__
   
   An absolute date/time value can be changed with a delta time, this can be added or subtracted from the absolute time value. Also with an absolute time a random time can be added, that way on/off time points can be varied from day to day.
   
   
   __Sunrise/Sunset__
   
   To follow sunrise/sunset with switch time values, those are calculated with just the keyword. Also those time values can be varied with add/substract or random add (see Time Delta). The geo coordinates has to be added to piSchedule.prefs.json.
 

#### Schedule plan

To configure which device at what time should be switched on/off is defined in a file which is passed to piScheduler.py.

That setup file has to a be a JSON or an easy text (INI) format. See below **Definitions** about the syntax.

**Day Schedule**
The schedule is always for one day. With date change the schedule which was passed with a .JSON or .INI file will be reloaded. That way the sunrise/sunset parameters as well as all random time values are recalculated.

**JSON**
```
    "name of timer": {
       "location": {
          "location_name": {
             "device_name": [state | state_and_time]
          }
       }
    }

```
**Text INI**
```
   location_name; device_name; [state | state_and_time]
   * comment line starting with asterisk - can have leading space(s)
       empty line allowed, will be ignored
```
_*Note*_   
*JSON definitions are not always parsed in the sequence of the occurrence in the file. That can be a problem with switch definitions only holding on/off. This problem doesn't exists with the INI format.*


### Definitions

A **'state'** OR **'state_and_time'** is REQUIRED, but both are NOT allowed for one device.


      state            = "on" | "off"
                       
                         This is direct switching method and will be executed  
                         as 'piSchedule' is called.

      For JSON
      state_and_time   = { "switch" : "switchDef" *[";switchDef"]}

      For INI   
      state_and_time   = "switchDef" *[";switchDef"]

                         'switchDef' MUST occur once and CAN occur more than once.

      switchDef        = ( "on|off,absoluteTime" )
                        / ( "on|off,[deltaTime][,vTime]")
                         A switch point needs a state 'on' OR 'off'.
                         Time value can be an 'absolute' date/time or a time delta definition 
                         'off' definition without vTime follows the previous 'on' time.
                         'deltaTime' and 'vTime' can be given in any order


      absoluteTime     = formats conform to 'dateutil'

      deltaTime        = '+|-|~|~-h:min'
                          A leading control character MUST occur once
                            leading plus  = add 'h:min' to vTime
                            leading minus = subtract 'h:min' from vTime
                            leading ~     = add a random 'h:min' to vTime
                                            random value is calculated with 'h:min'
                            leading ~-    = subtracts a random time
                           Leading character MUST occur


      vTime            = OPTIONAL, if NOT defined vTime is assumed the actual date/time
                         vTime without a date is parsed to actual day

                         vTime CAN be 'sunrise' OR 'sunset' but for that the 'Latitude' and
                         'Longitude' HAS to be defined in 'pySchedule.prefs.json'


   
   __Example__
   
   See **[piSchedule.json](https://github.com/neandr/piScheduler/blob/master/piSchedule.json)** 
   **[piSchedule.ini](https://github.com/neandr/piScheduler/blob/master/piSchedule.ini)** 
