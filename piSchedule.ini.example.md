*piSchedule* -- Scheduling Examples
------------------------------------

The *piSchedule* control commands follow the notation described on the [pilight documentation](http://www.pilight.org/getting-started/configuring/):

>    Devices

>    The first step is to define the pilight devices.

      "devices": {
            "Television": {
                "protocol": [ "relay" ],
                  "id": [{
                  "gpio": 3
                }],
                "state": "off",
                "default": "off"
            }
      },

>    The first JSON key 'Television' is the id used by pilight to identify a specific device, the value of the name (in this case Television with a capital T) setting is the name communicated by pilight.


__*piSchedule*__ uses those config.json details for scheduling. For a complete list of the commands, the usage and grammar have a look [here](https://github.com/neandr/piScheduler/blob/.../piSchedule.setup.md)

###piSchedule Examples

To show how a dedicated device can be controlled, here are some examples:

The example device is defined in ___config.json___ with:

        "Haustuer": {
                "protocol": [ "pollin" ],
                "id": [{
                        "systemcode": 21,
                        "unitcode": 1
                }],
                "state": "off"
        }

**Simple and direct switching**

    Haustuer; on;
    Haustuer; off;

**Time delayed switching**

    Haustuer; on,+:01;  off,+:2:00
'On' is delayed by one second; after 2 minutes it will be switched off

**Random Time delay**

    Haustuer; on,~01:00;
A random time between 'now' and 'in one hour' will be used to switch on

**Using Sunrise/Sunset**

    Haustuer; on, sunrise, +:30:00;
Switch time is 30 minutes after sunrise

    Haustuer; on, sunset, ~-:45:00; off,sunset, +3:15:00;
On/off switch is oriented at sunset, 'on' varies between 0 and 45 minutes __*before*__ sunset, 'off' will be 3 hours and 15 minutes after sunset

**Multiple switching with one command line**

    Haustuer; on, 19:45, ~:10:00; off, 21:05; on, 21:30; off, +2:00:00;
This has two time pairs to define time periods, first switched 'on' at 19:45 (with random time variation) and 'off' at 21:05; the second set is from 21:30 until 23:30

###piSchedule.py
As a Python program it can be started on a terminal running on client(PC). It's recommended to use a terminal program like 'tmux'. That way a started *piSchedule* session can be controlled also after the client has terminated.

__Terminal Output__

    python piSchedule.py piSchedule.ini

would write an output to the terminal like this:

![pic3][pic3]
[pic3]:https://dl.dropboxusercontent.com/u/35444930/piScheduler/prefs%26jobs%28c%29.png    

_Description_

Line 1: Header with actual date/time, following the next day the INI file is read again and the server:port

Line 2 .. 4: GeoLocation data with sunrise and sunset values for the day

Line 5: Header for the list of currently scheduled jobs. 
The list was generated with definitions in [piSchedule.ini] and the excecuted switches are stored to [Thursday.log]

Line 6: Showing a switch definition: the date/time in parentheses shows the switch time for  'Stehlampe', it was calculated from 'sunset' plus 10 minutes out of a random span of 30 minutes.
    
An example with **two scheduled events**:
![pic2][pic2]
[pic2]: https://dl.dropboxusercontent.com/u/35444930/piScheduler/piSchedule_2.png 

_Description_

Line 6 and 7 show two remaining definitions, both scheduled with switch time 23:45 and both random variation of 15 minutes. As can be seen the resulting time values differ with 23:46 and 23:51

The two schedules have been set from the following lines in 'piSchedule.ini':
```
    Stehlampe; on,22:35;off,~:15,23:45
    Kueche; on,19:15;off,~:15,23:45
```
    

__Day Log File__  
All processed switcedh events are written to a log file which is named with the actual day, like [Thursday.log] (see header of example above).     
The example shows a terminal snapshot taken at 23:21, the both 'on' schedules have been issued already and are removed from the list. Those removed schedule lines are written to the named log file.

###piConsole.py
With *piSchedule* running, the second helpful program is *piConsole*. It's purpose is to pass commands, schedule instructions or a piSchedule.ini or .json file to 'piSchedule.py', example:

    python piClient.py "Haustuer; on, sunrise; off, sunset;
    python piClient.py piSchedule.ini
    
_Description_

First passes just one schedule instruction to *piSchedule*; the second passes a complete set of schedules stored to a file named 'piSchedule.ini'.

With passing a file name that file is remembered by *piSchedule*. With day change the schedule of that file is updated for the new day and sunrise/sunset and all random settings are recalculated.


--------------------
<p align='center'>Using http://markable.in/editor/</p>
