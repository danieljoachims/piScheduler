#!/usr/bin/env python
'''
    Copyright (C) 2014 gWahl

    'piSchedule'  is an python extension for pilight 
      Installed on RaspberryPI together with pilight it supports time scheduled
      switching of devices and with calling
         http:// + server + ':' + port + message

      'server' and 'port' are those working with pilight and have to be 
         stored in a file named 'piSchedule.prefs.json'

      'message' is build from location, devices and time with state on/off.
         Those details have to be consistent with the pilight-config definitions
         and are stored in a JSON or INI file.
         That file name can be passed to piSchedule as an argument or be
         passed with piClient.py.

    'Calling'  ./piSchedule.py [argument]

    'piSchedule.MD'  more details and descriptions

    Schedule with 'Date/Time'
         A very flexible date/time handling is achieved with using 
         [dateutil](http://labix.org/python-dateutil/). 
         That utility allows piSchedule to support a very broad range of 
         date/time formats.
         Also switching based on sunrise/sunset is possible. 'ephem' is used. 
         Details see [pyphem](http://rhodesmill.org/pyephem/)
'''
# ------------------------------------------------------------------------------
from __future__ import print_function
import os
import sys
import urllib2
import json

import datetime
from datetime import date
from dateutil import parser

import time
from time import sleep

from multiprocessing.connection import Listener
from threading import Event, Thread

import socket

import ephem
import random

from apscheduler.schedulers.background import BackgroundScheduler
import struct
import re

#import signal

#def signal_handler(signal, frame):
#    print ('You pressed Ctrl+C!')
#    sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)



def piParam():
#---------------------------------
   parameter = {}
   def set(n, x):
#      print (n + " is:" + str(x))
      parameter[n] = x
   def get(n):
      if n is None:
          return ""
      else:
         try:    ## make 'onTime' has datetime format
            return parameter[n]
         except:
            return None
   return set, get
piSet,piGet=piParam()


# globals
#---------------------------------
__version__ = '0.1g'


def discover(service, timeout=2, retries=1):
#---------------------------------
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}'.format(*group),
        'MAN: "ssdp:discover"',
        'ST: {st}','MX: 3','',''])

    responses = {}
    i = 0;
    for _ in range(retries):
        i += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 0, 10000));
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(message.format(st=service), group)
        while True:
            try:
                responses[i] = sock.recv(1024);
                break;
            except socket.timeout:
                                break;
            except:
                print ("no pilight ssdp connections found")
                break;
    return responses.values()


sched = BackgroundScheduler()
jobs = []   # store scheduled tasks

def clearTerm():
    if os.name == 'nt':
        command = 'cls'
    else:
        command = 'clear'
    os.system(command)


def suntime():
#---------------------------------
#  support Sunrise/Sunset with time values
#  time is calculated for actual day!

   if (piGet('latitude')) and (piGet('longitude')):

      atHome = ephem.Observer()
      atHome.date = datetime.datetime.now()
      atHome.lat = piGet('latitude')
      atHome.lon = piGet('longitude')

      sun = ephem.Sun()
      piSet('sunrise', ephem.localtime(atHome.next_rising(sun, date.today())))
      piSet('sunset', ephem.localtime(atHome.next_setting(sun, date.today())))

      piSet('geo_message',"\033[1m  GeoLocation\033[0m"
         + "\n     " + piGet('location')
         + "  Latitude: " + piGet('latitude') + " Longitude: " + piGet('longitude')
         + "\n     Sunrise: " + str(piGet('sunrise'))[:19] + "  sunset: " + str(piGet('sunset'))[:19])

   else:
      piSet('geo_message',"***  pilight/piScheduler 'prefs': \033[1m GeoCoordinates not supported!\033[0m")


def fire_pilight(message):
#---------------------------------
     message0 = message.split('|')
     message1 = message0[0]
     message2 = ""
     if len(message0) > 1:
        message2 = message0[1]

     url = ('http://' + piGet('server') + ':' + piGet('port') + message1)
#     print (" ... piSchedule " + str(datetime.datetime.now()) + " | " + message2
#       + "\n  url:", url)

     request = urllib2.Request(url)
     response = urllib2.urlopen(request)


def pilightSchedule(onTime, switchLocation, actualDevice, currentSwitch):
#---------------------------------
   global jobs  # holds all scheduled 'fire_pilight' jobs

   actualSwitch = currentSwitch.strip().split(",")
   message = '/send?{"message":"send","code":{"location":"' + switchLocation \
      + '","device":"' + str(actualDevice) \
      + '","state":"' + str(actualSwitch[0]) + '"}}'

   # piSchedule direct on/off switching 
   if len(actualSwitch) == 1:
      fire_pilight(message)
      sleep(2)     # for testing .. delay between directly switching
      return()

   xTime = datetime.datetime.now()
   deltaTime = "*"

   # check xTime if valid and process different time options
   # xTime = '2014-04-17 22:06:00'  NEED secs, even if ':00'

   for nSwitch in actualSwitch:

       # have dateTime or sunrise or sunset
       if nSwitch == 'sunrise':
          xTime = piGet('sunrise')
       elif nSwitch  == 'sunset':
          xTime = piGet('sunset')


       # --- use deltaTime          
       # '+' add or '-' subtract time value
       # '~' add or '~-' subtract 'random' time value
       elif nSwitch[0] == '+' or nSwitch[0] == "-"  \
         or nSwitch[0] == "~":
           h = 0
           min = 0
           sec = 0

           random_subtract = False
           if nSwitch[0:2] == "~-":    #  subtract random time 
              random_subtract = True
              delta = nSwitch[2:]
           else:
              delta = nSwitch[1:]

           xDelta = delta.split(":")
           nDelta = len(xDelta)
           if nDelta >= 1:
              h   = 0 if xDelta[0] =='' else int(xDelta[0])
           if nDelta >= 2:
              min = 0 if xDelta[1] =='' else int(xDelta[1])
           if nDelta == 3:
              sec = 0 if xDelta[2] =='' else int(xDelta[2])
           deltaTime = datetime.timedelta(hours=h, minutes=min, seconds=sec)

           if nSwitch[0] == '+':    ## add timedelta
              print ("   delta + : ", nSwitch)

           if nSwitch[0] == '-':    ## substract timedelta
              print ("   delta - : ",  nSwitch)
              deltaTime = -deltaTime

           elif nSwitch[0] == '~':  ## add random minutes  
              rMin = h*60 + min
              print ("   random  : ", nSwitch)
              if random_subtract:
                 deltaTime = datetime.timedelta(minutes=random.randrange(rMin))
              else:
                 deltaTime = datetime.timedelta(minutes=random.randrange(rMin))
              print ("   deltaTime  : ", deltaTime)
       # ... use deltaTime

       elif nSwitch == 'on' or nSwitch == "off"  :
          pass
       else:
          xTime = parser.parse(nSwitch)

   if deltaTime != "*":
       xTime = (xTime + deltaTime)

   # make sure xTime has correct datetime type/format
   if str(type(xTime)) == "<type 'str'>":
      xTime =  parser.parse(xTime) 

   # remember  'on' state time, for 'off' set to now
   if actualSwitch[0] == 'on':
       onTime = xTime
   else:
       onTime = datetime.datetime.now()

   #  check if xTime is before actual time
   if (xTime <  datetime.datetime.now()):
      print (" *** error : ", str(xTime)[0:19],
         " :: " + currentSwitch.strip(), " *** before current time ***")
   else:
      print ("   xTime   : ", str(xTime)[0:19], "  ::", currentSwitch)
      jobName = str(int(time.time()*1000))[6:]

      info = '{0:14} {1:14} {2:15}'.format(switchLocation[0:12], actualDevice[0:12], currentSwitch).replace(',',' ')
      jobs.append(sched.add_job(fire_pilight, 'date', run_date=str(xTime), args=[message + "|" + info], name=jobName))

   return onTime


def jobListINI(jobList, name):
#---------------------------------
   '''
        ebene1; lampe2; on
        ebene1; lampe2; on,22:50;off,+:10
        ebene1; lampe2; on,+:02;  off,+:03:00
          * text/comment
        ebene1; lampe2; on,+:02;off,+:03:00
        ebene1; lampe2; on,+01:02,sunrise;off,-01:30,sunset;on,~:10,18:00;off,~:15,21:05
   '''

   for cJobs in jobList:
      cJobs = cJobs.strip()
      # strip out empty or comment lines 
      if len(cJobs) == 0 or cJobs[0] == '*':
         continue

      print (' {0} - Job >{1}<'.format(name, cJobs))

      cJob = cJobs.split(";")
      cJobLen = len(cJob)
      if cJobLen > 1 :
         switchLocation = cJob[0].strip()
         actualDevice = cJob[1].strip()

      now = datetime.datetime.now()
      n = 2
      while n < (cJobLen):
         currentSwitch = cJob[n].strip()
         now = pilightSchedule(now, switchLocation, actualDevice, currentSwitch)
         n += 1

def jobListJSON(jobFile):
#---------------------------------
   jobList = json.loads(jobFile.read())
   for cJob in jobList:

      location = jobList[cJob]["location"]
      for aLocation in location:
         switchLocation = str(aLocation)
         cLocation = location[aLocation]

         for actualDevice in cLocation:
            print (" ----------")

            # switch directly with on/off
            if ('on' in cLocation[actualDevice]) or ('off' in cLocation[actualDevice]):
               message = '/send?{"message":"send","code":{"location":"' + switchLocation \
               + '","device":"' + str(actualDevice) \
               + '","state":"' + str(cLocation[actualDevice]) + '"}}'

            #  +++ piSchedule direct on/off switching"
               fire_pilight(message)
               sleep(2)     # for testing .. delay between directly switching

            # using the APScheduler for 'Simple date-based scheduling'
            if 'switch' in cLocation[actualDevice]:
               currentSwitch = cLocation[actualDevice]['switch']

               sTimes = str(currentSwitch).strip().split(";")
               sTimesLen = len(sTimes)
               now = datetime.datetime.now()
               print (" +++  piSchedule : ", str(now)[0:19], "  ::", str(currentSwitch))

               jNo = 0
               while jNo < sTimesLen:
                  pass
                  now = pilightSchedule(now, switchLocation, actualDevice, sTimes[jNo])
                  jNo += 1


def next_switchTime():
#---------------------------------
    nextSwitchTime = piGet('nextSwitchTime')

    if date.today() == nextSwitchTime:
       nextSwitchTime = date.today() + datetime.timedelta(hours=24)
       suntime()

    piSet('nextSwitchTime', nextSwitchTime)
    return nextSwitchTime


def updateJobsListing():
#---------------------------------
    clearTerm()
    print (piGet('mainTitle'),  
       str(datetime.datetime.now())[:19], 
      " (", str(piGet('nextSwitchTime'))[:19] + ")",
      "\n" + piGet('geo_message'),
      "\n" + "\033[1m  Current Jobs \033[0m" + "    [" + str(piGet('job_file')) + "]")


    if len(sched.get_jobs()) == 0:
       pass 
       #exit()
    else:
       n = 0
       output = []
       while n < len(sched.get_jobs()):
           info = str(sched.get_jobs()[n].args).split('|')

           output.append("   " + (str(sched.get_jobs()[n].trigger).replace("date",'') + "  "
             + str(sched.get_jobs()[n].name) + "  "
             + info[1].replace("',)",'')))
           n += 1
           output.sort()

       n = 0
       while n < len(output):
          print (output[n])
          n += 1


def job_commands(message, name):
#---------------------------------
    if message != None:
    #  process as new switch file or string passing
        if '.json' in message or '.ini' in message:
           piSet('job_file', message)
           try:
              jobFile = open(message, 'r')
              if '.json' in message:
                 jobListJSON(jobFile)
              if '.ini' in message:
                 jobListINI(jobFile, name)

           finally:
              pass

        else:
           #   ebene1; lampe2; on,22:00
           jobListINI([message], name)


def jobs_listing(exit_event, name, calling):
#---------------------------------
   try:
      while not exit_event.is_set():   # loop to keep scheduler alive
          updateJobsListing()
          ''' TODO
            replace with threading /Event 
            see   http://blog.thomnichols.org/2010/11/use-pythons-threadingevent-for-interruptable-sleep
          '''
          if date.today() == piGet('nextSwitchTime'):
              next_switchTime()
              if name == "":
                  pass
                  # log this to file
              else:
                  job_commands(piGet('job_file'), name)
          if calling != "":
              job_commands(piGet('job_file'), calling)
              calling = ""
          sleep(10)

   finally:
       print (' piScheduler - Exit >{0}<'.format(name))


def job_serve(exit_event, name):
#---------------------------------
    address = (piGet('server'), 6000)
    listener = Listener(address, authkey='secret password')

    try:
        while True:
            connection = listener.accept()
            message = connection.recv().strip()

            #
            # process the incoming message...
            #
#            print (' .... incoming msg: ', message)
            if (message[0] != "-"):
               job_commands(message, name)

            else:
               print(' {0} - Command >{1}<'.format(name, message[1:]))

               if message[1:] == 'close':
                  break

               if message[1:] == 'update':
                  updateJobsListing()
    except:
       pass

    finally:
        caller = str(listener.last_accepted)
        if caller == 'None':
            caller = 'User'
        print(' {0} - Connection closed from {1}'.format(name, caller))

        exit_event.set()
        listener.close()
        sched.shutdown()
        sys.exit(0)


def startup():
#---------------------------------
   os.system('clear')

   now = datetime.datetime.now()
   next = next_switchTime()

   title1 = piGet('mainTitle') + str(now)[0:19] + "   next: " + str(next)

   jPrefs = 'piSchedule.prefs.json'
   try:
      prefsFile = open(jPrefs, 'r')
   except:
      print (title1, "\n***  pilight/piScheduler 'prefs' file \033[1m'",
        jPrefs, "'\033[0m not found!")
      exit()


   prefs = json.loads(prefsFile.read())

#   responses = discover("urn:schemas-upnp-org:service:pilight:1");
#   print ('***** discover values **** : \n', str(responses),'\n\n')
   responses = ""   # TODO 

   if len(responses) > 0:
      locationsrc = re.search('Location:([0-9.]+):(.*)', str(responses[0]), re.IGNORECASE)
      if locationsrc:
          server = locationsrc.group(1)
          port = locationsrc.group(2)

          print (" **** discover   server/port : ", server, port)

   if 'server' in prefs:
          piSet('server', prefs['server'])
   else:
          print (title1, "\n***  pilight/piScheduler 'prefs' \033[1m'server'\033[0m not found!")
          exit()

   if 'port' in prefs:
      piSet('port', prefs['port'])
   else:
      print (title1, "\n***  pilight/piScheduler 'prefs' \033[1m'port'\033[0m not found!")
      exit()

   next_switchTime()
#   suntime(prefs)   #sunrise, sunset, geoInfo = geo_info(prefs)
   if ('Latitude' in prefs) and ('Longitude' in prefs):

      piSet('latitude', str(prefs['Latitude']))
      piSet('longitude', str(prefs['Longitude']))
      if 'Location' in prefs:
         piSet('location', str(prefs['Location']))
      suntime()
   else:
      piSet('geo_message',"***  pilight/piScheduler 'prefs': \033[1m GeoCoordinates not supported!\033[0m")

   print (piGet('mainTitle'), "  ",
      str(datetime.datetime.now())[:19], "   next: ", str(next)[:19],
      "\n", piGet('geo_message'))


def main():
#---------------------------------
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    if len(sys.argv) == 2:
        calling = sys.argv[1]
        piSet('job_file', calling)
    else:
        calling = '  ..  ' + str(datetime.datetime.now())

    sched.start()  # start the scheduler
    piSet('mainTitle', "\033[1mpiScheduler   vers." + __version__ + "\033[0m"  + "  ")
    piSet('nextSwitchTime', date.today())

    exit_event = Event()
    startup()
    Thread(target=jobs_listing, args=(exit_event, 'pilight Jobs', calling)).start()
    job_serve(exit_event, 'piScheduler')

    print ('are we done??')
    sched.shutdown()
    exit()
#---------------------------------
if __name__ == "__main__":
    main()
