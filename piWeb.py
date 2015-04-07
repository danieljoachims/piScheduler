#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import os
import shutil
import signal
import json
import glob
import urllib2
import locale

from multiprocessing.connection import Client
from bottle import route, run, get, request, post, template

import piDiscover

import xStrings
xS = xStrings.piString()

#-- globals
responses = piDiscover.piDiscover("urn:schemas-upnp-org:service:pilight:1");
if responses[2] != "":
    print ("  **** piSchedule error with server/port \n" + str(responses))
    exit()      # the can happen if pilight isn't installed/started!

server = responses[0]
port = int(responses[1])+1
port0 = int(responses[1])

address = (server, port)


def getConfig(typ):
# ---------------------------
    global server, port0

    message = 'config'
    url = ('http://' + server + ':' + str(port0) + '/'  + message)

    request = urllib2.Request(url)
    response = urllib2.urlopen(request).read()
    return  json.loads(urllib2.unquote(response))[typ]


def getConn(code):
    global address

    conn = Client(address, authkey="X")
    qString = request.query_string

    rv = {}
    rv['cn'] = conn
    rv['qStr'] = qString
    return rv


@route('/')
def login_check():
    message =  "-prefs"

    # build 'ini' file menu for edit
    fHtml = '<li role="presentation"><a href="/edit?&&fName&&">&&fName&&</a></li>'

    iniFiles =  sorted(glob.glob("*.ini"))

    fileList = "<a role='menuitem' >&nbsp;&nbsp; " + xS('piWeb.editSchedule') + "... </a>"
    for x in iniFiles:
       fileList += fHtml.replace('&&fName&&',x)

    fileList += "</li><li role='presentation'><a href='/edit?newSchedule'>" + xS('piWeb.newSchedule') + "</a></li>"
    fileList += "<li class='divider'></li><li role='presentation'><a href='/edit?addJob'>"+ xS("piWeb.addJob") + "</a></li>"

    rv = {'pilight':'http://'+str(server)+':'+str(port-1)}
    page = templateSetup('piMain', rv)
    page = page.replace('&&iniFileList&&',fileList)

    return page.replace('&&language&&', xStrings.getLocale())


@route('/prefs')
def _prefs():
    message =  "-prefs"

    conn = getConn(None)
    if type(conn) == type(str()):
        print ("  piWeb - ", conn + " " + message)
        return conn
    conn['cn'].send(message)
    rv  = conn['cn'].recv()
    page = templateSetup('piPrefs', rv)

    hString = str(datetime.datetime.now())[10:19]
    page = page.replace('&&datetime&&', hString)
    page = page.replace('&&timeTable&&', jobs()).replace('\n','')
    return page


def templateSetup(templ, rv):
    textStr = xStrings.xS[templ][xStrings.getLocale()]
    both = {key: value for (key, value) in (rv.items() + textStr.items())}
    return template(templ, both)


@route('/close')
def close():
    message =  "-close"

    conn = getConn(None)
    qString = conn['qStr']
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message+qString)

    rv  = conn['cn'].recv()
    os.kill(os.getpid(), signal.SIGTERM)


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
       #print ("&&---  piWeb  job : " + str(n) + str(jTime) + "  " + str(jDetail))

       output.append("<tr><td> " + str(jTime) + "</td><td> " + str(jDetail) + "</td></tr> ")

    output.sort()

    output = tablebody + str(output) + '</tbody></table>'
    jString = str(output).replace("', '","").replace("']","").replace("['","")
    return (jString)


@route('/logs')
def logList():
    message =  "-logs"

    conn = getConn(None)
    qString = conn['qStr']
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message + qString)

    selectedDay = qString.strip()
 
    now = datetime.datetime.now()
    today = now.strftime("%A")
    if selectedDay == "":
        selectedDay = today

    fLog = '/home/pi/piScheduler/' + selectedDay +'.log'

    output = []

    try:
        logss = open(fLog, 'r')

        for line in logss:
          output.append('<li>' + line.replace("\n","") + '</li>')

        output.sort(reverse=True)

        output = '<ul>' + str(output) + '</ul>'
        output = str(output).replace("', '","").replace("']","").replace("['","")

    except:
       msg = " +++  " + xS("piWeb.piLogFile") + " "+ fLog + " " + xS("notFound")
       print (msg)
       #return msg


    rv = {'logList':output,  'today':today}

    page = templateSetup('piLogs', rv)
    page = page.replace("&&currentDay&&",xS("piLogs."+selectedDay))
    return page


@route('/locale')
def setLanguage():
    message =  "-locale"

    conn = getConn(None)
    qString = conn['qStr']
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send(message + qString)

    rv  = conn['cn'].recv()

    print ("  piWeb  locale :" + str(rv))
    return (str(rv))


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


@route('/cmd')
def piCmd():
    message =  "-cmd"

    conn = getConn(None)
    qString = conn['qStr']
    if type(conn) == type(str()):
        print (conn + " " + message)
        return conn
    conn['cn'].send("-" + qString)

    rv  = conn['cn'].recv()
    return (str(rv))


@route('/edit')
@post('/edit')
def edit():
    message =  "-prefs"

    addJob = False

    conn = getConn(None)
    if type(conn) == type(str()):
        print ("  piWeb - ", conn + " " + message)
        return conn
    conn['cn'].send(message)

    rv  = conn['cn'].recv()
    page = templateSetup('piEdit', rv)

    fileName  = conn['qStr']
    if fileName == 'addJob':
       addJob = True

    # build the html list of devices
    devices = getConfig('devices')

    #<a role="menuitem" onclick="changeDevice(this)">Haustuer</a>
    deviceList = ""
    for d in devices:
       deviceList += '<a role="menuitem" onclick="changeDevice(this)">'+d+'</a>'

    page = page.replace('&&deviceList&&', deviceList)


    # replace date/time string
    hString = str(datetime.datetime.now())[10:19]
    page = page.replace('&&datetime&&', hString)

    if addJob == True:
       page = page.replace('&&JOBS&&',"")
       page = page.replace('&&FILE&&',"")

       page = page.replace('&&jobDefEdit&&','display:none')
       page = page.replace('&&jobDefExec&&','display:block')

       page = page.replace('&&displaySchedule&&','display:none')

       page = page.replace('&&jobAdd&&','display:none')
       page = page.replace('&&jobExec&&','display:block')

    else:
       page = page.replace('&&jobDefEdit&&','display:block')
       page = page.replace('&&jobDefExec&&','display:none')

       page = page.replace('&&displaySchedule&&','display:block')

       page = page.replace('&&jobAdd&&','display:block')
       page = page.replace('&&jobExec&&','display:none')


       #  newSchedule
       if fileName == 'newSchedule':
           fileName = 'newDaySchedule.ini'
           f = open(fileName, 'w')
           f.write(' * Define new Schedule')
           f.close()

       if fileName == "" or fileName == None:
           fileName = 'piSchedule.ini'

       # read the selected 'ini' file to textbox
       jobList = jobs_read(fileName, 'piEdit')
       page = page.replace('&&JOBS&&',str(jobList))

       # set the 'ini' file name  
       page = page.replace('&&FILE&&',str(fileName))

    return (page)



@post('/fDelete')
def fDelete():
    qStr = request.query_string
    qString = json.loads(urllib2.unquote(qStr))

    fName = qString[0]['fName']
    pName = qString[1]['pName']
    if fName == "":
       fName = pName
    os.remove(fName)



@route('/fSave')
@post('/fSave')
def fSave():
    qStr = request.query_string
    qString = json.loads(urllib2.unquote(qStr))

    fName = qString[0]['fName']
    pName = qString[1]['pName']
    if fName == "":
      fName = pName

    iniFiles =  glob.glob("*.ini")
    fileList = ""
    for x in iniFiles:
       if fName == x:
           shutil.copy2(fName, fName + '.bak')

    xjobs = qString[2]['jobs'].replace('|','\n')

    f = open(fName, 'w')
    f.write(xjobs)
    f.close()


def jobs_read(message, name):
#---------------------------------
    jobList = ""
    if message != None:

        if '.ini' in message:
           jobList =""
           jobFile = open(message, 'r')
           for cJobs in jobFile:
              jobList = jobList + '<option>' + cJobs +'</option>'

    return jobList

