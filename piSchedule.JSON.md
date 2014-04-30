piSchedule.JSON.md
===========

###piSchedule definition of switch time values

   Switching of devices with __piSchedule__ is defined with the general form

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
   
   
   Format Definition:  The values are defined by the following notation:



      state            = "on" | "off"
                       ;
                       ; This is direct switching method and will be exceuted 
                       ; as 'piSchedule' is called.

      state_and_time   = { "switch" : "switchDef" *[";switchDef"]}
                       ;
                       ; 'switchDef' CAN occure more than once.

 

      switchDef        = ( "on|off,absoluteTime" )
                       / ( "on|off,deltaTime[,vTime]")

      absoluteTime     = formats conform to 'dateutil'

      deltaTime        = '+|-|~h:min'
                       ;  leading plus  = add 'h:min' to vTime
                       ;  leading minus = substract 'h:min' from vTime
                       ;  leading ~     = adds a random 'h:min' to vTime
                       ;                  random value is calculated with 'h:min'
                       ;  Leading character MUST occur

      vTime            = OPTIONAL, if NOT defined vTime = actual date/time
                       ; vTime without a date is parsed to actual day

                       ; vTime CAN 'sunrise' OR 'sunset' but the 'Latitude' and
                       ; 'Longitude' HAS to be defined in 'pySchedule.prefs.json'



   __Date/Time__
   
   A very flexible date/time handling is achieved with using [dateutil](http://labix.org/python-dateutil/). That utility allows piSchedule to support a very brod range of date/time formats. 
   
   
   __Sunrise/Sunset__
   
   Also switching based on sunrise/sunset is possible. 'ephem' is used for that, for details see [pyphem](http://rhodesmill.org/pyephem/)
   
   
   __Example__
   
   See ´piSchedule.json´
