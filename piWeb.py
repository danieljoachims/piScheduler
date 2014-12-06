#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import os
import signal
import json


from multiprocessing.connection import Client
from bottle import route, run, get, request, post, template

import piDiscover


#-- globals
responses = piDiscover.piDiscover("urn:schemas-upnp-org:service:pilight:1");

server = responses[0]
port = int(responses[1]['port_pilight'])+1
address = (server, port)



def getConfig(setting):
# ---------------------------
   jConfig = '/etc/pilight/config.json'
   
   try:
      confFile = open(jConfig, 'r')

   except:
      msg ("  ***  pilight 'configure' file '", jConfig, 
        "' not found! (Check access rights!")
      print (msg)
      return msg

   configure = json.loads(confFile.read())

   if setting != None: 
      return str(configure['settings'][setting])
   else:
      return configure['settings']


def getConn(code):
    global address

    
    conn = Client(address, authkey=piDiscover.authKey())
    qString = request.query_string
    rv = {}
    rv['cn'] = conn
    rv['qStr'] = qString
    return rv


@route('/')
@post('/')
def login_check():
    message =  "-prefs"

    rv = {'pilight':'http://192.168.178.16:5001'}
    return template('piMain', rv)


@route('/LogID')
def logid():
    message =  "-prefs"

    conn = getConn(True)
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message)

    rv = conn['cn'].recv()
    return template('piLogin', rv)

@route('/prefs')
@post('/prefs')
def prefs():

    message =  "-prefs"

    conn = getConn(None)
    if type(conn) == type(str()):
        print ("  piWeb - ", conn + " " + message)
        return conn
    conn['cn'].send(message)

    rv  = conn['cn'].recv()
    part1 = template('piPrefs', rv)

    hString = str(datetime.datetime.now())[10:19]
    part1 = part1.replace('&&datetime&&', hString)
    part1 = part1.replace('&&timeTable&&', jobs()).replace('\n','')
    return (part1)


@route('/close')
def close():
    message =  "-close"

    conn = getConn(None)
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message)

    rv  = conn['cn'].recv()
    msg = "  piWeb - Send to piSchedule!  message: " + rv

    os.kill(os.getpid(), signal.SIGTERM)
    #return msg


@route('/jobs')
def jobs():
    message =  "-jobs"    

    conn = getConn(None)
    qString = conn['qStr']
    print (" request :" + qString)

    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message)

    rv  = conn['cn'].recv()
    rJobs = json.loads(rv)

    tablebody = '<table class="table table-striped table-bordered"><tbody>'

    n = 0
    output = []
    for n in (rJobs):
       jTime = rJobs[n]['jTime']
       jDetail = rJobs[n]['jDetail']
       #print ("&&--  piWeb  job : " + str(n) + str(jTime) + "  " + str(jDetail))

       output.append("<tr><td> " + str(jTime) + "</td><td> " + str(jDetail) + "</td></tr> ")

    output.sort()

    output = tablebody + str(output) + '</tbody></table>'
    jString = str(output).replace("', '","").replace("']","").replace("['","")
    return (jString)

@post('/logs')
def logs():

    now = datetime.datetime.now()
    today = now.strftime("%A")

    logList()
    rv = {'logList':'', 'today':today, 'selectedDay':''}
    return template('piLogs', rv)

@route('/logs')
@post('/logList')
def logList():

    conn = getConn(None)
    qString = conn['qStr']
    selectedDay = qString.strip()
 
    now = datetime.datetime.now()
    today = now.strftime("%A")
    if selectedDay == "":
        selectedDay = today

    fLog = '/home/pi/piScheduler/' + selectedDay +'.log'

    try:
       logs = open(fLog, 'r')

    except:
       msg = ("  ***  pilight 'log' file '", fLog,
        "' not found! (Check access rights!)")
       print (msg)
       return msg

    output = []

    for line in logs:
      output.append('<li>' + line.replace("\n","") + '</li>')

    output.sort(reverse=True)

    output = '<ul>' + str(output) + '</ul>'
    output = str(output).replace("', '","").replace("']","").replace("['","")

    now = datetime.datetime.now()
    today = now.strftime("%A")
 
    rv = {'logList':output,  'today':today,  'selectedDay': selectedDay}
    return template('piLogs', rv)


#----------------------------------------------
@route('/control')
def pilightControl():
    message =  "-control"

    conn = getConn(None)

    qString = conn['qStr']
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message + qString)

    rv  = conn['cn'].recv()
    return (str(rv))

