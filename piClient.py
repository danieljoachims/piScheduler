#!/usr/bin/env python
'''
    Copyright (C) 2014 gWahl

    'piClient' is used with 'piSchedule' a python extension for pilight.
      Installed on RaspberryPI together with pilight it supports time scheduled
      switching of devices 
      'piClient.py' passes commands or the name of a file which contains
      commands to be processed by 'piSchedule'.

    'Calling'  ./piClient.py [argument]

    'piSchedule.MD'  more details and descriptions
'''
# ----------------------------------------------------

import sys
import datetime
from multiprocessing.connection import Client
import json

jsonPrefs = 'piSchedule.prefs.json'
try:
   prefsFile = open(jsonPrefs, 'r')
except:
   print (title1, "\n***  pilight/piScheduler 'prefs' file \033[1m'",
     jsonPrefs, "'\033[0m not found!")
   exit()

prefs = json.loads(prefsFile.read())
server = prefs['server']


if len(sys.argv) == 2:
    message = sys.argv[1]
else:
    message = 'pyClient : ' + str(datetime.datetime.now())

address = (server, 6000)

conn = Client(address, authkey='secret password')
conn.send(message)

# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()
