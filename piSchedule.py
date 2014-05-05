#!/usr/bin/env python
'''
    Copyright (C) 2014 gWahl

    'piSchedule'  is an python extension for pilight 
      Installed on RaspberryPI together with pilight it supports time scheduled
      switching of devices and with calling
         http:// + server + ':' + port + message

      'server' and 'port' have to be stored in a file named 'piSchedule.prefs.json'

      'message' is build from location, devices and time with state on/off.
         Those details have to be consistent with the pilight-config definitions
         and are stored in a JSON or INI file.
         That file name can be passed to piSchedule as an argument or if
         omitted the file is assumed to be stored in the same directory with 
         the name but with extension '.json'. 

         'piSchedule.setup.MD'  details for 'piSchedule.json'/'piSchedule.ini'

    Calling: $ ./piSchedule.py [piSchedule.json|piSchedule.ini]


    Date/Time
         A very flexible date/time handling is achieved with using 
         [dateutil](http://labix.org/python-dateutil/). 
         That utility allows piSchedule to support a very brod range of 
         date/time formats.

         Also switching based on sunrise/sunset is possible. 'ephem' is used 
         for that, for details see [pyphem](http://rhodesmill.org/pyephem/)
'''
version = '0.8h'
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
onTime = 0  # used to remember last 'on' time 

title1 = ''
titleGeo = ''
#--------------------------------
jobs = []      # store scheduled tasks


def fire_pilight(message):
#---------------------------
     url = ('http://' + server + ':' + port + message)
     print " ... piSchedule server:" + server + "  port:" + port + "\n  url:" + url

     request = urllib2.Request(url)
     response = urllib2.urlopen(request)



def pilightSchedule(sLocation, aDevice, cSwitch):
#-----------------------------
   global onTime
   aSwitch = cSwitch.strip().split(",")
   message = '/send?{"message":"send","code":{"location":"' + sLocation \
      + '","device":"' + str(aDevice) \
      + '","state":"' + str(aSwitch[0]) + '"}}'

   # piSchedule direct on/off switching 
   if len(aSwitch) == 1:
      fire_pilight(message)
      sleep(2)     # for testing .. delay between directly switching
      return()

   now = datetime.datetime.now()

   sleep(2)     # for testing .. delay between directly switching

   # check xTime if valid and process different time options
   xTime = aSwitch[1]      # xTime = '2014-04-17 22:06:00'  NEED secs, even if ':00'

   if len(aSwitch) > 2:    # have dateTime or sunrise or setset
       if aSwitch[2] == 'sunrise':
          now = sunrise
       elif aSwitch[2]  == 'sunset':
          now = sunset
       else:
          now = parser.parse(aSwitch[2] )

       onTime = now

   # --- use timedelta         # add or substract time value
   if aSwitch[1][0] == '+' or aSwitch[1][0] == "-"  \
     or aSwitch[1][0] == "~":  # "~"  used for 'random' time 
       h = 0
       min = 0
       sec = 0

       delta = aSwitch[1][1:]
       xDelta = delta.split(":")
       nDelta = len(xDelta)
       if nDelta >= 1:
          h   = 0 if xDelta[0] =='' else int(xDelta[0])
       if nDelta >= 2:
          min = 0 if xDelta[1] =='' else int(xDelta[1])
       if nDelta == 3:
          sec = 0 if xDelta[2] =='' else int(xDelta[2])

       try:    ## make 'onTime' has datetime format
          now = parser.parse(onTime)
       except:
          pass

       if xTime[0] == '+':    ## add timedelta
          print "   +++  timedelta: " + str(now)[0:19] + "  ::"  + cSwitch
          xTime = str(now + datetime.timedelta(hours=h, minutes=min, seconds=sec))

       if xTime[0] == '-':    ## substract timedelta
          print "   +++  timedelta: " + str(now)[0:19] + "  ::"  + cSwitch
          xTime = str(now - datetime.timedelta(hours=h, minutes=min, seconds=sec))

       elif xTime[0] == '~':  ## add random minutes  
          rMin = h*60 + min
          print "   +++     random: " + str(now)[0:19] + "  ::"  + cSwitch
          xTime = str(now + datetime.timedelta(minutes=random.randrange(rMin)))
   # ... use timedelta

   # make sure xTime has correct datetime type/format
   if str(type(xTime)) == "<type 'str'>":
      xTime =  parser.parse(xTime) 

   # remember an 'on' state time, clear for 'off'
   if aSwitch[0] == 'on':
       onTime = xTime
   else:
       onTime = 0

   #  check if xTime is before actual time
   if (xTime <  datetime.datetime.now()):
      print "   *** wrong time! " + str(xTime)[0:19]\
          + " before current time!   ::" + cSwitch.strip()
   else:
      print "   ... xTime     : " + str(xTime)[0:19] + "  ::" + cSwitch
       # job = sched.add_date_job(fire_pilight, '2014-04-22 23:31:00', [message])
       # job = sched.add_date_job(fire_pilight, str(datetime.datetime(2014, 4, 22, 23, 32, 0)), [message])
      global jobs  # holds all scheduled 'fire_pilight' jobs
      jobs.append(sched.add_date_job(fire_pilight, str(xTime), [message]))



def jobListINI(jobList):
#---------------------------
   for cJobs in jobList:
      cJobs = cJobs.strip()
      if len(cJobs) == 0 or cJobs[0] == '*':
         continue
      print "-----------"
      print " +++ next Jobs: "  + cJobs

      cJob = cJobs.split(";")
      cJobLen = len(cJob)

      sLocation = cJob[0].strip()
      aDevice = cJob[1].strip()

      '''
        ebene1; lampe2; on
        ebene1; lampe2; on,22:50;off,+:10
        ebene1; lampe2; on,+:02;  off,+:03:00
          * text/comment
        ebene1; lampe2; on,+:02;off,+:03:00
        ebene1; lampe2; on,+01:02,sunrise;off,-01:30,sunset;on,~:10,18:00;off,~:15,21:05
      '''

      n = 2
      while n < (cJobLen):
         cSwitch = cJob[n].strip()
         pilightSchedule(sLocation, aDevice, cSwitch)
         n += 1


def jobListJSON(jobFile):
#---------------------------
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

            #  +++ piSchedule direct on/off switching"
               fire_pilight(message)
               sleep(2)     # for testing .. delay between directly switching

            # using the APScheduler for 'Simple date-based scheduling'
            if 'switch' in cLocation[aDevice]:
               cSwitch = cLocation[aDevice]['switch']

               sTimes = str(cSwitch).strip().split(";")
               sTimesLen = len(sTimes)
               now0 = datetime.datetime.now()
               print " +++  piSchedule : " + str(now0)[0:19] + "  ::" + str(cSwitch)

               onTime = 0  # used to remember last 'on' time 
               jNo = 0
               while jNo < sTimesLen:
                  pass
                  pilightSchedule(sLocation, aDevice, sTimes[jNo])
                  jNo += 1


def suntime(prefs):
#---------------------------
#  support Sunrise/Sunset with time values
#  time is calculated for actual day!

   if ('Latitude' in prefs) and ('Longitude' in prefs):
      global Latitude
      Latitude = prefs['Latitude']
      global Longitude
      Longitude = prefs['Longitude']
      if 'Location' in prefs:
         global Location
         Location = prefs['Location']

      atHome = ephem.Observer()
      atHome.date = datetime.datetime.now()
      atHome.lat = str(Latitude)
      atHome.lon = str(Longitude)

      sun = ephem.Sun()
      global sunrise
      sunrise = ephem.localtime(atHome.next_rising(sun, date.today()))
      global sunset
      sunset = ephem.localtime(atHome.next_setting(sun, date.today()))

      global titleGeo
      titleGeo ="\033[1m  GeoCoordinates\033[0m" \
         + "\n  - Location: " + Location + "  Latitude: " + Latitude + " Longitude: " + Longitude \
         + "\n  - Sunrise: " + str(sunrise) + "  sunset: " + str(sunset)
      print titleGeo

   else:
      print "***  pilight/piScheduler 'prefs': \033[1m GeoCoordinates not supported!\033[0m"



def main():
#---------------------------
   now=datetime.datetime.now()
   os.system('clear')
   title0 = "\033[1mpiScheduler   vers." + version + "\033[0m"  + "  " 
   title1 = title0 + str(now)[0:19] + "   "

   jPrefs = 'piSchedule.prefs.json'
   try:
      prefsFile = open(jPrefs, 'r')
   except:
      print title1 + "\n***  pilight/piScheduler 'prefs' file \033[1m'" + jPrefs + "'\033[0m not found!"
      exit()

   prefs = json.loads(prefsFile.read())
   if 'server' in prefs:
      global server
      server = prefs['server']
   else:
      print title1 + "\n***  pilight/piScheduler 'prefs' \033[1m'server'\033[0m not found!"
      exit()

   if 'port' in prefs:
      global port
      port = prefs['port']
   else:
      print title1 + "\n***  pilight/piScheduler 'prefs' \033[1m'port'\033[0m not found!"
      exit()

   # schedule file
   if len(sys.argv) == 2:
      job_file = sys.argv[1]
   else:
      job_file = sys.argv[0] + '.json'
      job_file = job_file.replace('.py.json', '.json')
   try:
      jobFile = open(job_file, 'r')
   except:
      print title1 + "\n***  pilight/piScheduler file \033[1m'"  \
         + job_file + "'\033[0m not found!"
      exit()

   print title1 + job_file
   suntime(prefs)

   if '.json' in job_file:
      jobListJSON(jobFile)

   elif '.ini' in job_file:
      jobListINI(jobFile)

   else:
      print title1 + "\n***  pilight/piScheduler file \033[1m'"  \
         + job_file + "'\033[0m is not valid!" \
         + "\n   *** Need JSON or INI format. "
      exit()


   while True:   # loop to keep scheduler alive
      os.system('clear')
      print title0 + "  " + job_file + "  " + str(datetime.datetime.now())[0:19] + "\n" + titleGeo
      sched.print_jobs()
      if len(sched.get_jobs()) == 0:
         exit()
      sleep(10)

#---------------------------------------------------------------
if __name__ == "__main__":
    main()


