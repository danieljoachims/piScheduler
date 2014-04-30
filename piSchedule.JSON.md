piSchedule.JSON.md
===========

###piSchedule definition of switch time values

   Switching of devices with __piSchedule__ is defined with the general form

```
    "name of timer": {
       "location": {
          "location_name": {
             "device": "state | state_and_time"
          }
       }
    }
```



   __Date/Time__
   A very flexible date/time handling is achieved with using [dateutil](http://labix.org/python-dateutil/). 
   That utility allows piSchedule to support a very brod range of date/time formats. 
   
   Also switching based on sunrise/sunset is possible. 'ephem' is used for that, for details see [pyphem](http://rhodesmill.org/pyephem/)
   
   

