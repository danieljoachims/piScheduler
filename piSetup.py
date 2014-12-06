from __future__ import print_function

import sys
import datetime

import struct
import re
import json
from pbkdf2 import crypt
from geopy.geocoders import Nominatim

aLocation = ""
aLogin = ""


def pw(prefs, code, type):
#---------------------------------
    if type == 'get':  # get new LogID hash
        hash = crypt(str(code))
        prefs['piHash'] = str(hash)
        return prefs

    if type == 'check':
        hash = str(prefs['piHash'])
        print("   Check LogID:", hash)

        if crypt(code, hash) != hash:
            print('   *** ERROR ***  LogID failed.')
            return #"<p>  piWeb - LogID failed.</p>"
        else:
            print('   LogID  OK.')
            return




def getGeo(prefs, timeout):

    prefs['Latitude'] = "" 
    prefs['Longitude'] = ""
 
    location = Nominatim().geocode(aLocation,timeout=int(timeout))

    prefs['Latitude'] = str(location.latitude)
    prefs['Longitude'] = str(location.longitude)

    return prefs


#----------------------------------
print ("piScheduler Setup")

nArg = len(sys.argv)

help =   "piSetup Help"
help +=  "\n   Used to setup or change LogID and Geolocation"
help +=  "\n   Call:  piSetup [LogIn='code'] [hash='code'] [Location='city' [GeoTimeout='timeout']]"


aLogID = "logID"
hash = "hash"
aLocation = "location"
gTimeout = 10


for arg in sys.argv:

   if "LogID=" == arg[0:6]:          
      aLogID = arg[6:]

   if "hash=" == arg[0:5]:
      hash = arg[5:]

   if "Location=" == arg[0:9]:          
      aLocation= arg[9:]

      if "GeoTimeout=" == arg[0:11]:
          gTimeout= arg[11:]


prefs = {}

jsonPrefs = 'piSchedule.prefs.json'
try:
    prefsFile = open(jsonPrefs, 'r')
    prefs = json.loads(prefsFile.read())
except:
    print ("\n***  pilight/piScheduler 'prefs' file\n \033[1m'",
      jsonPrefs, "'\033[0m not found!")
    error = "  'prefs' file not found!"
    exit()

# write a bak copy of current prefs
f = open((jsonPrefs + '.bak'), 'w')
f.write(json.dumps(prefs))
f.close()

if aLocation != 'location':
    prefs['Location'] = aLocation
    getGeo(prefs, (gTimeout *1))

if aLogID != "logID":
    pw(prefs, aLogID, 'get')

if hash != "hash":
    pw(prefs, hash, 'check')

print ("   >> ", str(prefs), "\n", jsonPrefs)

# write new prefs file 
f = open(jsonPrefs, 'w')
f.write(json.dumps(prefs))
f.close()
