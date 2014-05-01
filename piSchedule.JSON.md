piSchedule.JSON.md
===========

###piSchedule definition of switch time values

   Switching of devices with __piSchedule__ offers the following features:


   __Date/Time__
   
   The very flexible date/time handling is achieved with using [dateutil](http://labix.org/python-dateutil/). That utility allows piSchedule to support a very brod range of date/time formats. 
   
   __Time Delta__
   
   An absolute date/time value can be changed with a delta time, this can be added or substracted from the absolute time value. Also with an absolute time a random time can be added, that way on/off time points can be varied from day to day.
   
   
   __Sunrise/Sunset__
   
   To follow sunrise/sunset with switch time values, those are calculated with just the keyword. Also those time values can be varied with add/substract or random add (see Time Delta). The geo coordinates has to be added to piSchedule.prefs.json.
 

#### Schedule plan
is defined in a JSON format and follows the following notation:


```
    "name of timer": {
       "location": {
          "location_name": {
             "device": [state | state_and_time]
          }
       }
    }

```
   A 'state' OR 'state_and_time' is REQUIRED, but both are NOT allowed for one device.
   


      state            = "on" | "off"
                       
                         This is direct switching method and will be exceuted 
                         as 'piSchedule' is called.

      state_and_time   = { "switch" : "switchDef" *[";switchDef"]}
                       
                         'switchDef' MUST occure once and CAN occure more than once.

 

      switchDef        = ( "on|off,absoluteTime" )
                       / ( "on|off,deltaTime[,vTime]")
                         A switch point needs a state 'on' OR 'off'.
                         Time value can be an 'absolute' date/time or a time delta definition 

      absoluteTime     = formats conform to 'dateutil'

      deltaTime        = '+|-|~h:min'
                          A Leading control character MUST occur once
                            leading plus  = add 'h:min' to vTime
                            leading minus = substract 'h:min' from vTime
                            leading ~     = adds a random 'h:min' to vTime
                                            random value is calculated with 'h:min'


      vTime            = OPTIONAL, if NOT defined vTime is assumed the actual date/time
                         vTime without a date is parsed to actual day

                         vTime CAN be 'sunrise' OR 'sunset' but for that the 'Latitude' and
                         'Longitude' HAS to be defined in 'pySchedule.prefs.json'


   
   __Example__
   
   See **piSchedule.json**
