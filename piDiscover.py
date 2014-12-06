import socket
import struct
import re
import json
from pbkdf2 import crypt

def getPrefs():

    prefs = {}
    server = ''
    port = ''
    error = ''

    jsonPrefs = '/etc/pilight/config.json'
    try:
        prefsFile = open(jsonPrefs, 'r')
        piPrefs = json.loads(prefsFile.read())
    except:
        print ("\n***  pilight 'prefs' file\n \033[1m'",
        prefsPrefs, "'\033[0m not found!")
        error = "  'pilight prefs' file not found!"
        return [server, port, error, prefs]


    jsonPrefs = 'piSchedule.prefs.json'
    try:
        prefsFile = open(jsonPrefs, 'r')
        prefs = json.loads(prefsFile.read())
    except:
        print ("\n***  pilight/piScheduler 'prefs' file\n \033[1m'",
        jsonPrefs, "'\033[0m not found!")
        error = "  'prefs' file not found!"
        return [server, port, error, prefs]

    prefs['port_pilight'] = piPrefs['settings']['webserver-port']
    #print ("\n***  pilight/piScheduler 'prefs' file:  \033[1m", jsonPrefs, "\033[0m")

    return (prefs)


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
    #print ("discover:\n", r)

    if len(r) > 0:
       locationsrc = re.search('Location:([0-9.]+):(.*)', str(r[0]), re.IGNORECASE)
       if locationsrc:
           server = locationsrc.group(1).strip()
           port = locationsrc.group(2).strip()
           error = ""

    return [server, getPrefs(), error]


def pw(pw):
#---------------------------------
    prefs = getPrefs()
    hash = prefs['piHash']

    #print("  piDiscover pw:", hash)
    
    if crypt(pw, hash) != hash:
        print('  piWeb - Login failed. Password error')
        return "<p>  piWeb - Login failed.</p>"

    return None


def authKey():
#--------------------------------
    prefs = getPrefs()
    return str(prefs['piHash'])
