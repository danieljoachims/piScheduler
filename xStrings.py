#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 xStrings   description
    Supports language text strings for different subsystems: 
      -- bottle with 'template' and {{string}} replacement
      -- JS/HTML replacement

    'lang' (eg. DE or EN) controls the return of the language string, if asked 
     with unknown code, returns default (EN) string  

 "xStrings.json" Details:
 piSchedule
    text items for 'piSchedule.py' called like 'piStr('nopilight')
    language selection with global 'xpiString.lang'

 other
     see 'piWeb.py' and 'templateSet(templ, rv)'
     it combines two json strings and passed to bottle 'template'
      
     'templ' template name like 'piEdit'  of 'piEdit.tpl' 
     'rv' return values from piWeb calls
'''
import json

lang = ""

xS = ""
xStringsJSON = "xStrings.json"
if xS == "":
    xfileJSON = open(xStringsJSON, 'r')
    xS = json.loads(xfileJSON.read())


def getLocale():
    global lang, piPrefs
    try:
        x = xS['piPrefs'][lang]
    except:
        lang = 'EN'
    return lang


def piString():
#---------------------------------
    global lang, xS

    def get(n):
        getLocale()

        if n is None:
            return ""
        else:
            strings = n.split(".")

            if len(strings) == 1:
                try:
                    return xS['piSchedule'][n][lang]
                except:
                    return xS['piSchedule'][n]['EN']    #  default string
            else:
                try:
                    return xS[strings[0]][lang][strings[1]]
                except:
                    return xS[strings[0]]['EN'][strings[1]]

    return get
