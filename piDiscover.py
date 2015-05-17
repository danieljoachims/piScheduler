import socket
import struct
import re
import json

# Automatically geolocate the connecting IP
from urllib2 import urlopen
from contextlib import closing
import json
freegeoIP = 'http://freegeoip.net/json/'


def piDiscover(service, timeout=2, retries=1):
#---------------------------------
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}'.format(*group),
        'MAN: "ssdp:discover"',
        'ST: {st}','MX: 3','',''])

    responses = {}
    server = ''
    port = ''
    error = ''

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
                error = 'timeout'
                break;
            except:
                error = 'no pilight ssdp connections found'
                break;

    r = responses.values()

    if len(r) > 0:
       locationsrc = re.search('Location:([0-9.]+):(.*)', str(r[0]), re.IGNORECASE)
       if locationsrc:
           server = locationsrc.group(1).strip()
           port = locationsrc.group(2).strip()
           error = ""

    cPrefs = {}

    configFile = '/etc/pilight/config.json'
    try:
        prefsFile = open(configFile, 'r')
        cPrefs = json.loads(prefsFile.read())
        port = cPrefs['settings']['webserver-http-port']
        #print (" +++  piDiscover pilight/piSchedule  port >>" + port + "<<")

    except:
        print (" +++  piDiscover ** pilight 'prefs' file  >>" + \
        configFile + "<<  not found!")
        error = "  'pilight prefs' file not found!"

    return [server, port, error]
