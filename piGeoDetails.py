#!/usr/bin/env python 

from urllib2 import urlopen
from contextlib import closing
import json

# Automatically geolocate the connecting IP 
url = 'http://freegeoip.net/json/'
try:
    with closing(urlopen(url)) as response:
        location = json.loads(response.read())
        location['ip'] = 0
        print(location)
        #return location
except:
    error = (" --- piGeoDetails failed! Location could not be determined automatically!")
    print error

