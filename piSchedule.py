#!/usr/bin/env python
'''
    Copyright (C) 2014 gWahl

    'piSchedule'  is an python extention for pilight 
      Installed on RaspberryPI together with pilight it supports time scheduled
      switching of devices and with calling
         http:// + server + ':' + port + message

      'server' and 'port' have to be stored in a file named 'piSchedule.prefs.json'

      'message' is build from location, devices and times with state on/off.
         Those details have to be consistent with the pilight-config definitions
         and are stored in a JSON file.
         The JSON file name can be passed to piSchedule as an argument or if
         omitted the file is assumed to be stored in the same directory with 
         the name but with extension '.json'. 

    'piSchedule.JSON.MD'  details for 'piSchedule.json'

    Calling: $ ./piSchedule.py (piSchedule.json)


    Date/Time
         A very flexible date/time handling is achieved with using 
         [dateutil](http://labix.org/python-dateutil/). 
         That utility allows piSchedule to support a very brod range of 
         date/time formats.

         Also switching based on sunrise/sunset is possible. 'ephem' is used 
         for that, for details see [pyphem](http://rhodesmill.org/pyephem/)
'''
version = '0.7'
#-------------------------------------------------------------------------------
import os
import sys
import urllib2
import json
import datetime
import time

from time import sleep

from datetime import date
from dateutil import parser
#dt = parser.parse("Aug 28 1999 12:00AM")

import ephem
import random

from apscheduler.scheduler import Scheduler
sched = Scheduler()
sched.start()        # start the scheduler


# server & port, Coordinates
#--------------------------------
server = "192.xxx.xxx.xx"
port = "xxxx"

Location = ""
Latitude = "51.2500000"
Longitude = "6.9666700"

sunrise = ''
sunset = ''
#--------------------------------
jobs = []      # store scheduled tasks


def fire_pilight(message):
#---------------------------
     url = ('http://' + server + ':' + port + message)
     print " ... piSchedule server:" + server + "  port:" + port + "\n  url:" + url

     request = urllib2.Request(url)
     response = urllib2.urlopen(request)


def main():
#---------------------------
   now=datetime.datetime.now()
   os.system('clear')
   title1 = "\033[1mpiScheduler   vers." + version + "\033[0m"
   print title1 + "  " + str(now)

   scheduleParam = 'piSchedule.prefs.json'
   try:
      paramFile = open(scheduleParam, 'r')
   except:
      print "***  pilight/piScheduler 'prefs' file \033[1m'" + scheduleParam + "'\033[0m not found!"
      exit()

   params = json.loads(paramFile.read())
   if 'server' in params:
      global server
      server = params['server']
   else:
      print "***  pilight/piScheduler 'prefs' \033[1m'server'\033[0m not found!"
      exit()

   if 'port' in params:
      global port
      port = params['port']
   else:
      print "***  pilight/piScheduler 'prefs' \033[1m'port'\033[0m not found!"
      exit()

   #  support Sunrise/Sunset with time values
   if ('Latitude' in params) and ('Longitude' in params):
      global Latitude
      Latitude = params['Latitude']
      global Longitude
      Longitude = params['Longitude']
      if 'Location' in params:
         global Location
         Location = params['Location']

      atHome = ephem.Observer()
      atHome.date = datetime.datetime.now()
      atHome.lat = str(Latitude)
      atHome.lon = str(Longitude)

      sun = ephem.Sun()
      global sunrise
      sunrise = ephem.localtime(atHome.next_rising(sun, date.today()))
      global sunset
      sunset = ephem.localtime(atHome.next_setting(sun, date.today()))

      title2 ="\033[1m  GeoCoordinates\033[0m" \
         + "\n  - Location: " + Location + "  Latitude: " + Latitude + " Longitude: " + Longitude \
         + "\n  - Sunrise: " + str(sunrise) + "  sunset: " + str(sunset)
      print title2

   else:
      print "***  pilight/piScheduler 'prefs': \033[1m GeoCoordinates not supported!\033[0m"


   # schedule file
   if len(sys.argv) == 2:
      job_file = sys.argv[1]
   else:
      job_file = sys.argv[0] + '.json'
      job_file = job_file.replace('.py.json', '.json')
   try:
      jobFile = open(job_file, 'r')
   except:
      print "***  pilight/piScheduler file \033[1m'"  \
         + job_file + "'\033[0m not found!"
      exit()


   jobList = json.loads(jobFile.read())
   for cJob in jobList:

      location = jobList[cJob]["location"]
      for aLocation in location:
         sLocation = str(aLocation)
         cLocation = location[aLocation]

         for aDevice in cLocation:
            print " --------"

            # switch directly with on/off
            if ('on' in cLocation[aDevice]) or ('off' in cLocation[aDevice]):
               message = '/send?{"message":"send","code":{"location":"' + sLocation \
               + '","device":"' + str(aDevice) \
               + '","state":"' + str(cLocation[aDevice]) + '"}}'

         #     print " +++ piSchedule direct on/off switching"
               fire_pilight(message)
               sleep(2)     # for testing .. delay between directly switching

            # using the APScheduler for 'Simple date-based scheduling'
            if 'switch' in cLocation[aDevice]:
               cSwitch = cLocation[aDevice]['switch']

               sTimes = str(cSwitch).split(";")
               sTimesLen = len(sTimes)
               print " +++  piSchedule 'Simple date-based scheduling'  (raw):" + str(cSwitch) + " len:" + str(len(sTimes))
               now0 = datetime.datetime.now()
               print "   *** now       : " + str(now0)[0:19] + " type: "+ str(type(now0))

               onTime = 0  # used to remember last 'on' time 
               jNo = 0
               while jNo < sTimesLen:
                  jTime = sTimes[jNo].split(",")
                  xState = jTime[0]
                  # check for xState is 'on' or 'off' ONLY! Other is error!        ##TODO

                  if xState == 'on' or xState == 'off':
                     message = '/send?{"message":"send","code":{"location":"' + sLocation \
                       + '","device":"' + str(aDevice) \
                       + '","state":"' + xState + '"}}'
                  else:
                     print " *** State for device is not correct! " + sTimes[jNo]
                     excit()

                  # check xTime if valid and process different time options
                  xTime = jTime[1]      # xTime = '2014-04-17 22:06:00'  NEED secs, even if ':00'

                  suntime = False
                  if len(jTime) > 2:    # have dateTime or sunrise or setset
                     if jTime[2] == 'sunrise':
                        now = sunrise
                        suntime = True
                     elif jTime[2] == 'sunset':
                        suntime = True
                        now = sunset
                     else:
                        now = parser.parse(jTime[2])
                     onTime = 0
                  else:
                     now = datetime.datetime.now()
                  now0 = now

                  # --- use timedelta       # add or substract time value
                  if xTime[0] == '+' or xTime[0] == "-"  \
                    or xTime[0] == "~":     # "~"  used for 'random' time 
                     h = 0
                     min = 0
                     sec = 0

                     delta = xTime[1:]
                     xDelta = delta.split(":")
                     nDelta = len(xDelta)
                     if nDelta == 1:
                        h   = 0 if xDelta[0] =='' else int(xDelta[0])
                     if nDelta == 2:
                        min = 0 if xDelta[1] =='' else int(xDelta[1])
                     if nDelta == 3:
                        sec = 0 if xDelta[2] =='' else int(xDelta[2])

                     if onTime != 0:        ## use a previous 'on' time
                        now = parser.parse(onTime)
             #           print "   +++     onTime: " + str(onTime) + "  ::"  + sTimes[jNo]

                     if xTime[0] == '+':    ## add timedelta
             #           print "   +++  timedelta: " + str(now) + "  ::"  + sTimes[jNo]
                        xTime = str(now + datetime.timedelta(hours=h, minutes=min, seconds=sec))

                     if xTime[0] == '-':    ## substract timedelta
             #           print "   +++  timedelta: " + str(now) + "  ::"  + sTimes[jNo]
                        xTime = str(now - datetime.timedelta(hours=h, minutes=min, seconds=sec))

                     elif xTime[0] == '~':  ## add random minutes  
                        rMin = h*60 + min
                        xTime = str(now + datetime.timedelta(minutes=random.randrange(rMin)))
                  # ... use timedelta

                  # remember an 'on' state time, clear for 'off'
                  if xState == 'on':
                     onTime = xTime
                  else:
                     onTime = 0

                  # make sure xTime has correct datetime type/format
                  if str(type(xTime)) == "<type 'str'>":
                      xTime =  parser.parse(xTime) 
#                  print "   ... xTime     : " + str(xTime) + "  ::" + sTimes[jNo]

                  #  check if xTime is before actual time
                  if (xTime <  datetime.datetime.now()):
                     print "   *** wrong time! " + str(xTime)[0:19]\
                        + " before  current time: " + str(datetime.datetime.now())[0:19] \
                        + "  raw: " + sTimes[jNo]

                  else:
                     print "   ... xTime     : " + str(xTime)[0:19] + "  ::" + sTimes[jNo]
                     # job = sched.add_date_job(fire_pilight, '2014-04-22 23:31:00', [message])
                     # job = sched.add_date_job(fire_pilight, str(datetime.datetime(2014, 4, 22, 23, 32, 0)), [message])
                     global jobs  # holds all scheduled 'fire_pilight' jobs
                     jobs.append(sched.add_date_job(fire_pilight, str(xTime), [message]))

                  jNo += 1

   while True:
      os.system('clear')
      print title1 + "   " + str(datetime.datetime.now()) + "\n" + title2
      sched.print_jobs()
      if len(sched.get_jobs()) == 0:
         exit()
      sleep(10)
#---------------------------------------------------------------
if __name__ == "__main__":
    main()
