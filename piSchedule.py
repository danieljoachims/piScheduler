#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Copyright (C) 2015 gWahl

    'piSchedule'  is an python extension for pilight 
      Installed on RaspberryPI together with pilight it supports time scheduled
      switching of devices.

    Schedule with 'Date/Time'
         A very flexible date/time handling is achieved with using 
         [dateutil](http://labix.org/python-dateutil/). 
         That utility allows piSchedule to support a very broad range of 
         date/time formats.
         Also switching based on sunrise/sunset is possible. 'ephem' is used. 
         Details see [pyphem](http://rhodesmill.org/pyephem/)

    See 'piScheduleOverview.html'  for more details and installation
'''
# ------------------------------------------------------------------------------
from __future__ import print_function

import os
import signal
import glob

import sys
import json

import datetime
from datetime import date
from dateutil import parser

import time
from time import sleep

from multiprocessing.connection import Listener
from multiprocessing.connection import Client

from threading import Event, Thread

from bottle import route, run, get, request, post, template
import urllib2
import socket

import ephem
import random

from apscheduler.schedulers.background import BackgroundScheduler
import struct
import re

import piDiscover
import piWeb

import xStrings
xS = xStrings.piString()

pilightPrefsFile = '/etc/pilight/config.json'
pilightPrefs =[]

prefsJSONfile = 'piSchedule.prefs.json'
#def signal_handler(signal, frame):
#    print ('You pressed Ctrl+C!')
#    sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)

# Automatically geolocate the connecting IP
from urllib2 import urlopen
from contextlib import closing
import json
freegeoIP = 'http://freegeoip.net/json/'


prefs = {}


def piParam():
#---------------------------------
   parameter = {}
   def set(n, x):
      parameter[n] = x
   def get(n):
      if n is None:
          return ""
      else:
         try:
            return parameter[n]
         except:
            return None
   return set, get
piSet,piGet=piParam()


# globals
#---------------------------------
__version__ = '0.4'
prefs = {}
jobs  = []   # store scheduled tasks
sched = BackgroundScheduler()


def clearTerm():
    if os.name == 'nt':
        command = 'cls'
    else:
        command = 'clear'
    os.system(command)



#---------------------------------
def getGeo():
    try:
        with closing(urlopen(freegeoIP)) as response:
            location = json.loads(response.read())
            location['ip'] = 0
            return location

    except:
        error = (" --- piGeoDetails failed! Location could not be determined automatically!")
        return error


def prefsSetup():
    geoRV = getGeo()
    if (type(geoRV) is dict):
        '''
        geoRV = 
        {u'city': u'Mettmann', u'region_code': u'NW', u'region_name': u'North Rhine-Westphalia',
         u'ip': 0, u'time_zone': u'Europe/Berlin',
         u'longitude': 6.971, u'metro_code': 0, 
         u'latitude': 51.256, 
         u'country_code': u'DE', 
         u'country_name': u'Germany', 
         u'zip_code': u'40822'}
        '''
        prefs['Location'] = str(geoRV['city'])
        prefs['Longitude'] = str(geoRV['longitude'])
        prefs['Latitude'] = str(geoRV['latitude'])
        prefs['locale'] = str(geoRV['country_code'])
    else:
        prefs['Longitude'] = ""
        piSet('geo_message'," +++  pilight/piSchedule 'prefs': \033[1m " + xS("noGeoCordinates") + "\033[0m")

    responses = piDiscover.piDiscover("urn:schemas-upnp-org:service:pilight:1");
    prefs['server'] = responses[0]
    prefs['port_pilight'] = responses[1]

    prefsSave(None, None)
    return prefs


def prefsSave(aName, aPref):
    global prefsJSONfile, prefs

    # write a bak copy of current prefs
    f = open((prefsJSONfile + '.bak'), 'w')
    f.write(json.dumps(prefs))
    f.close()

    if aPref != None:
        prefs[aName] = aPref

    # write new prefs file 
    f = open(prefsJSONfile, 'w')
    f.write(json.dumps(prefs))
    f.close()






#----------------------------------------

def prefsSet(item, value):
    pass
    prefsSave(item, value)


def prefsGet(item):
    global prefsJSONfile, prefs

    try:
        p = prefs[item]
    except:
        prefsRead()
        p = prefs[item]

    return p


def prefsRead():
    global prefsJSONfile, prefs

    #print("&&--- prefsRead    prefs:" + str(prefs))
    if prefs == {}:
        try:
            prefsFile = open(prefsJSONfile, 'r')
            prefs = json.loads(prefsFile.read())

        except:
            print  (str( "\n +++  " + xS("prefsFile") + " >>" +
             + prefsJSONfile + "<< setup."))

            prefs = prefsSetup()


def logFile():
    now = datetime.datetime.now()
    return '/home/pi/piScheduler/' + now.strftime("%A") +'.log'


def pilightPrefsGet(setting):
# ---------------------------
    global pilightPrefsFile
    global pilightPrefs

    if pilightPrefs == []:
        try:
           pilightJSON = open(pilightPrefsFile, 'r')
           pilightPrefs = json.loads(pilightJSON.read())
        except:

           msg = (" +++  pilight 'configure' file >>" +
             pilightPrefsFile + "<<  not found! (Check access rights!")
           print (msg)
           return xS('noconfigFile') #"No configure file or missing access rights!"

    return str(pilightPrefs['settings'][setting])


def suntime():
#---------------------------------
#  support Sunrise/Sunset with time values
#  time is calculated for actual day!

   if ('Latitude' in prefs) and ('Longitude' in prefs):

      atHome = ephem.Observer()
      atHome.date = datetime.datetime.now()
      atHome.lat = prefs['Latitude']
      atHome.lon = prefs['Longitude']

      sun = ephem.Sun()
      sunrise = (ephem.localtime(atHome.next_rising(sun, date.today())))
      sunset  = (ephem.localtime(atHome.next_setting(sun, date.today())))
      prefs['sunrise'] = str(sunrise)
      prefs['sunset']  = str(sunset)

      piSet('geo_message',"\033[1m  GeoLocation\033[0m"
        + "\n     " + str(prefs['Location'])
        + "  Latitude: " + str(prefs['Latitude']) + " Longitude: " + str(prefs['Longitude'])
        + "\n     Sunrise: " + str(sunrise)[:19] + "  sunset: " + str(sunset)[:19])

   else:
      piSet('geo_message'," +++  " + xS('noGeoloaction')) 


def fire_pilight(arg):
#---------------------------------
    message = arg['message']
    info = arg['info']

    url = ('http://' + prefs['server'] + ':' + str(prefs['port_pilight']) + message)

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    message = message.replace('/send?{"action":"control","code":','')
    message = message.replace('{','').replace('}','')

    now = datetime.datetime.now()
    f = open(logFile(), 'a')
    f.write(str(now)[0:19] + " : " + info + "\n")
    f.close()



def pilightSchedule(onTime, actualDevice, currentSwitch):
#---------------------------------
   ''' lampe2; on,+:02
       actualDevice=    lampe2; 
       currentSwitch=   on,+:02
   '''
   global jobs  # holds all scheduled 'fire_pilight' jobs

   #actualSwitch = currentSwitch.strip().split(",")
   actualSwitch = currentSwitch.strip().replace("%20","").split(",")

   if ('on' in actualSwitch or 'off' in actualSwitch) == False:
      return xS("noState")  #ERROR: no on/off

   #http://192.168.178.16:5001/send?{"action":"control","code":{"device":"Bad","state": "on"}}
   message = '/send?{"action":"control","code":{"device":"' + actualDevice \
      + '","state":"' + str(actualSwitch[0]) + '"}}'

   # piSchedule direct on/off switching 
   if len(actualSwitch) == 1:
      arg = {}
      arg['message'] = message
      info = '{0:12} {1:15}'.format(actualDevice[0:12], currentSwitch.replace(',',' '))
      arg['info'] = info
      fire_pilight(arg)
      sleep(2)     # for testing .. delay between directly switching
      return()

   xTime = onTime
   deltaTime = "*"

   # check xTime if valid and process different time options
   # xTime = '2014-04-17 22:06:00'  NEED secs, even if ':00'

   for nSwitch in actualSwitch:
       nSwitch = nSwitch.strip()

       # have dateTime or sunrise or sunset
       if nSwitch == 'sunrise':
          xTime = parser.parse(prefs['sunrise'])
       elif nSwitch  == 'sunset':
          xTime = parser.parse(prefs['sunset'])

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
              if random_subtract:
                 deltaTime = datetime.timedelta(minutes=random.randrange(rMin))
              else:
                 deltaTime = datetime.timedelta(minutes=random.randrange(rMin))
              print ("   random  : ", nSwitch, " --> deltaTime  : ", deltaTime)
       # ... use deltaTime

       elif nSwitch == 'on' or nSwitch == "off" or nSwitch == "time" :
          pass
       else:
          try: 
            if (nSwitch == "24:00"):
                nSwitch = "23:59"  
            xTime = parser.parse(nSwitch)
          except: 
             nSwitch = 'err:' + nSwitch
             print(" +++ " + xS("unknownString") + ">>", nSwitch,"<<")


   if deltaTime != "*":
       xTime = (xTime + deltaTime)

   # remember 'on' state time
   onTime = xTime

   # check if xTime is before actual time
   if (xTime <  datetime.datetime.now()):
      print (" +++  SKIP : ", str(xTime)[0:19], "  :: ",
         currentSwitch.strip(), "   +++ " + xS("beforeTime") + " +++")
   else:
      print ("   xTime   : ", str(xTime)[0:19], "  :: ", currentSwitch, "  :: ", actualDevice)
      jobName = str(int(time.time()*1000))[6:]

      info = '{0:12} {1:15}'.format(actualDevice[0:12], currentSwitch.replace(',',' '))
      jobs.append(sched.add_job(fire_pilight, 'date', run_date=str(xTime), args=[{'message':message, 'info':info}], name=jobName))
   return onTime


def jobListINI(jobList, name):
#---------------------------------
   '''  lampe2; on
        lampe2; on,22:50;off,+:10
        lampe2; on,+:02;  off,+:03:00
          * text/comment
        lampe2; on,+:02;off,+:03:00
        lampe2; on,+01:02,sunrise;off,-01:30,sunset;on,~:10,18:00;off,~:15,21:05
   '''
   for cJobs in jobList:
      cJobs = cJobs.strip()
      # strip out empty or comment lines 
      if len(cJobs) == 0 or cJobs[0] == '*':
         continue

      print ('--------------------------\n {0} - Job >{1}<'.format(name, cJobs))

      cJob = cJobs.split(";")
      cJobLen = len(cJob)
      if cJobLen > 1 :
         actualDevice = cJob[0].strip().replace("%20","")

      now = datetime.datetime.now()
      n = 1
      while n < (cJobLen):
         currentSwitch = cJob[n].strip().replace("%20","")
         now = pilightSchedule(now, actualDevice, currentSwitch)
         n += 1
   return now


def jobListJSON(jobFile):
#---------------------------------
    ''' 
    {"job1": {
        "device": "lampe2",
        "switch": "on,+:02;off,+:03:00"
    },
    "job2": {
        "device": "lampe2",
        "switch": "off,23:30"
    }
    }
    '''

    jobList = json.loads(jobFile.read())
    for cJob in jobList:

        actualDevice = jobList[cJob]['device']
        switchList = jobList[cJob]['switch']
        switches = switchList.split(';')

        for actualSwitch in switches:
            print (" ----------")

            # switch directly with on/off
            if ('on' == actualSwitch) or ('off' == actualSwitch):

               #http://192.168.178.16:5001/send?{"action":"control","code":{"device":"Bad","state": "on"}}
               message = '/send?{"action":"control","code":{"device":"' + actualDevice \
                  + '","state":"' + (actualSwitch) + '"}}'

            #  +++ piSchedule direct on/off switching"
               arg = {}
               arg['message'] = message
               info = '{0:12} {1:15}'.format(actualDevice[0:12], actualSwitch.replace(',',' '))
               arg['info'] = info
               #fire_pilight(arg)
               sleep(2)     # for testing .. delay between directly switching

            # using the APScheduler for 'Simple date-based scheduling'
            else:
               now = datetime.datetime.now()
               print (" +++  piSchedule : ", str(now)[0:19], "  :: ", str(actualSwitch))
               now = pilightSchedule(now, actualDevice, actualSwitch)



def next_switchTime():
#---------------------------------
    nextSwitchTime = piGet('nextSwitchTime')

    if date.today() == nextSwitchTime:
       nextSwitchTime = date.today() + datetime.timedelta(hours=24)
       suntime()
       # handle log files
       try:
           os.remove(logFile())
           now = datetime.datetime.now()
           f = open(logFile(), 'a')
           f.write(str(now)[0:19] + "\n")
           f.close()
       except:
           pass

    piSet('nextSwitchTime', nextSwitchTime)
    return nextSwitchTime


def updateJobsListing():
#---------------------------------
    clearTerm()

    print(piGet('mainTitle'),  
       str(datetime.datetime.now())[:19], 
       " (", str(piGet('nextSwitchTime'))[:19] + ")", " " + prefs['server'] + ":" 
          + str(int(prefs['port_pilight'])+2),
       "\n" + piGet('geo_message'),
       "\n" + "\033[1m  " + xS("daySchedule") +" \033[0m" + "    [" + str(piGet('job_file')) + "]    [" + logFile() +"]")

    if len(sched.get_jobs()) == 0:
       pass 

    else:
       n = 0
       output = []
       while n < len(sched.get_jobs()):
           info = str(sched.get_jobs()[n].args[0]['info'])

           output.append("   " + (str(sched.get_jobs()[n].trigger).replace("date",'') + "  " \
             + str(sched.get_jobs()[n].name) + "  " + info))
           n += 1
           output.sort()

       n = 0
       while n < len(output):
          print (output[n])
          n += 1


def jobsDict():
#---------------------------------
    jDict = {}
    if len(sched.get_jobs()) == 0:
       pass 
       #exit()
    else:
       n = 0
       while n < len(sched.get_jobs()):
           info = str(sched.get_jobs()[n].args[0]['info'])
           jNumber = str(sched.get_jobs()[n].name)
           jDict[jNumber] = {}
           jDict[jNumber]['jTime'] = str(sched.get_jobs()[n].trigger).replace("date",'')
           jDict[jNumber]['jDetail'] = info
           n += 1

    return(jDict)


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
           #   Lampe2; on,22:00
           msg = jobListINI([message], name)
           return msg


def jobs_listing(jobs_event, name, calling):
#---------------------------------
   try:
      while not jobs_event.is_set():   # loop to keep scheduler alive
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
       print (' piSchedule - Exit >{0}<'.format(name))



def jobs_serve(jobs_event, name):
#---------------------------------
    global prefs

    address = prefs['server'], int(prefs['port_pilight'])+1
    #listener = Listener(address, authkey=piDiscover.authKey())
    try:
        listener = Listener(address, authkey="X")
    except:
        err = str(sys.exc_info()[0])
        print("\n\n  *** piSchedule already running. Terminating! ***\n  "
               + err + "  >>" + prefs['server'] + ":" + str(int(prefs['port_pilight'])+1) + "<<")
        os.kill(os.getpid(), signal.SIGTERM)


    control = True
    while control:
        try:
            connection = listener.accept()
            message = connection.recv().strip()
            reply = ('  Error:  {0} - Command >{1}< unknown'.format(name, message[1:]))

            #
            #print ('&&------ incoming msg: ', message)
            #
            if (message[0] != "-"):
               msg = job_commands(message, name)
               reply = 'Done. ' + str(msg)

            else:
               if message[1:] == 'logs':
                  reply = 'logs listing.' 

               if message[1:] == 'update':
                  updateJobsListing()
                  reply = 'Have updated job listing.' 

               elif message[1:] == 'jobs':
                  reply  = json.dumps(jobsDict())

               elif message[1:] == 'prefs':
                  reply  = (prefs)

               elif message[1:7] == 'locale':
                  reply  = ("locale: ", message[7:])
                  if message[7:] == "":
                      reply = ("  Locale:  no language id!")
                  else:
                        cmsg = message[7:]
                        xStrings.lang = cmsg
                        #print ("&&---  piSchedule  'locale' >>" + cmsg + "<<")
                        prefsSave('locale', cmsg)
                        reply = ("  Locale set:" + cmsg)

               elif message[1:8] == 'control':
                  reply  = ("control: ", message[8:])
                  if message[8:] == "":
                      reply = ("  Control:  no control string!")
                  else:
                      cmsg = message[8:].replace("%20","")
                      job_commands(cmsg, name)
                      reply = ("control:" + cmsg)


               elif message[1:8] == 'addJobs':
                  jobs = message[9:] 
                  reply  = ("addJobs: " + jobs)
                  if jobs == "":
                     reply = ("  addJobs:  no Jobs to add!")
                  else:
                     # load the jobs 
                     xjobs = jobs.replace("%20"," ")
                     print ("&--- jobs to add \n" + xjobs)
                     aJobs = xjobs.split("|")
                     for cJob in aJobs:
                        if cJob != "" and cJob[0:1] != "*":
                           print(" cJob :" + cJob)
                           job_commands(cJob, 'addJobs')
                     reply = ("addJobs" )


               elif message[1:11] == 'removeJobs':
                  sched.shutdown()
                  sched.start()
                  reply  = ("Scheduler has removed all Jobs: ", "")


               elif message[1:9] == 'loadJobs':
                  addINI = message[10:] 
                  msg = "  piSchedule 'loadJobs'  >>" + addINI + "<<  "
                  print (msg)
                  reply  = (msg)

                  errMsg = "Getting File failed !"

                  if addINI == "":
                    reply = (msg + errMsg)
                  else:
                    try:
                        jobFile = open(addINI, 'r')
                        jobListINI(jobFile, name)
                        errMsg = ""
                        piSet('job_file', addINI)
                    except:
                        err = str(sys.exc_info()[0])
                        errMsg =  "  File read failed! \n   " + err
                    reply = (msg + errMsg)


               elif message[1:6] == 'close':
                   caller = str(listener.last_accepted)

                   if caller == 'None':
                      caller = 'User'
                   reply = ('  {0} - Connection closed from {1}'.format(name, caller))
                   print (reply + "\n" + message[6:].replace("%20"," "))
                   connection.send(reply)
                   connection.close()

                   jobs_event.set()
                   listener.close()
                   sched.shutdown()
                   control = False
                   break

            print (" ---  piSchedule - reply:", reply)
            connection.send(reply)
            connection.close()

        except:
           err = str(sys.exc_info()[0])
           print ("   ",name, str(err).replace("type 'exceptions.","").replace("'",""))
           os.kill(os.getpid(), signal.SIGTERM)


def startup():
#---------------------------------
    global prefs

    clearTerm()
    now = datetime.datetime.now()
    next = date.today() + datetime.timedelta(hours=24)
    piSet('nextSwitchTime', next)

    title1 = piGet('mainTitle') + str(now)[0:19] + "   next: " + str(next)

    prefsRead()     #prefsSetup()
    xStrings.lang = prefs['locale']

    print(" +++  piSchedule   prefs:" + str(prefs))

    next_switchTime()
    suntime()

    print (piGet('mainTitle'), "  ",
        str(datetime.datetime.now())[:19], "   next: ", str(next)[:19], " " + prefs['server'] 
         + " " + str(int(prefs['port_pilight'])+2), "\n" , piGet('geo_message'))

    return None


def runWeb(aserver, aport):
    run(host=aserver, port=aport, debug=True)



def main():
#---------------------------------
    global prefs
    try:
        calling = sys.argv[1]
    except:
        calling = ""

    if (len(sys.argv) == 1) or (calling == "--help"):
        print ("""  piSchedule Help
    Call for 'piSchedule.py'
       piSchedule.py [argument] 
    
    argument is:
       INI-filename  Pass a day schedule file name with jobs
       
       -ini          List ini files and allow selection

       -close        Close a running instance of piSchedule.py
       -addJobs      Add Jobs from a INI-file to a running instance, file is 
                     assumed to be stored to the same directory
                       call: piSchedule.py -add [filename]
        --help       
    """)
        return


    now = datetime.datetime.now()
    next = date.today() + datetime.timedelta(hours=24)
    piSet('nextSwitchTime', next)

    prefsRead()
    _server = prefs['server']
    _port = int(prefs['port_pilight'])+1
    address = (_server, _port)

    xStrings.lang = prefs['locale']

    if calling == "-close":
        print("  piSchedule Control  " + calling)

        conn = Client(address, authkey="X")
        conn.send(calling)

        print("  piSchedule  Done ")
        conn.close()
        return

    if calling == "-removeJobs":
        print("  piSchedule Control  " + calling)

        conn = Client(address, authkey="X")
        conn.send(calling)

        print("    piSchedule  Done: ", conn.recv)
        return


    if calling == "-addJobs":
        print("  piSchedule Control  " + calling )

        if (len(sys.argv) == 2):
           print("  *** piSchedule  '-addJobs' needs filename")
           return

        addINI = sys.argv[2]

        conn = Client(address, authkey="X")
        conn.send(calling + ":" + addINI)

        print("  piSchedule  Done: " + conn.recv())
        conn.close()
        return


    if calling == "-loadJobs":
        print("  piSchedule Control  " + calling )

        if (len(sys.argv) == 2):
           print("  *** piSchedule  '-loadJobs' needs filename")
           return

        addINI = sys.argv[2]

        conn = Client(address, authkey="X")
        conn.send(calling + ":" + addINI)

        print("  piSchedule  Done: " + conn.recv())
        conn.close()
        return


    if calling == "-control":
        print("  piSchedule Control  " + calling )

        job = sys.argv[2]

        conn = Client(address, authkey="X")
        conn.send(calling + job)
        print("  piSchedule  Done: " + conn.recv())
        conn.close()
        return


    if calling == "-ini":
        iniFiles =  sorted(glob.glob("*.ini"))
        #print (" INI Files :\n" +str(iniFiles))

        prefsSetup()

        fileList = "\n --- " + xS('startWithINI') + " ---"
        no = 1
        for x in iniFiles:
           fileList += "\n    " + str(no) + "  " + x
           no = no + 1

        print (fileList)

        userNumber = raw_input("\n     " + xS('selectINI') + "  ")
        try:
            userNumber = int(userNumber)
        except ValueError:
            userNumber = 0

        if userNumber > (no -1):
            print ("     " + xS('selectionMax') + str(no -1))
            return
        if userNumber < 1:
            print ("     " + xS('terminated') )
            return

        print ("\n     " + xS('iniIs') + "  [" + str(userNumber) + "]: " + iniFiles[userNumber - 1])
        calling = iniFiles[userNumber - 1]


    piSet('job_file', calling)

    piSet('mainTitle', "\033[1mpiSchedule   vers." + __version__ + "\033[0m"  + "  ")
    piSet('nextSwitchTime', date.today())
    jobs_event = Event()

    _startup = startup()
    if _startup != None:
       print ("\033[1m" + _startup + "\033[0m")
       exit()

    sched.start()  # start the schedule

    tJobs = Thread(target=jobs_listing, args=(jobs_event, xS('scheduleList'), calling)).start()
    tWeb = Thread(target=runWeb, args=(prefs['server'], int(prefs['port_pilight'])+2)).start()

    jobs_serve(jobs_event, 'piSchedule')

    try:
       sched.shutdown()
       tJobs.shutdown()
       tWeb.shutdown()
    except:
       pass

    print ('  piSchedule - Done.')
    os.kill(os.getpid(), signal.SIGTERM)
    #exit()

#---------------------------------
if __name__ == "__main__":
    main()
