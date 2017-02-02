#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import random
import time
import deepdish as dd
import xlrd, xlwt
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#######################################################

from vkGroupApi import *
import config
from common import *

appName='student'

#######################################################


#######################################################

base=dd.io.load('base.h5')
print 'Started...'+appName

# Словарь для команд

command = {'question %d' %a:{'txt':[base['question'][a]],'answer':[base['answer'][a]]} for a in range(len(base['question']))}

#список всех комананд, для помощи
ckeys = loadCommands (command)
command['question 0']['answer']='Извини, я тебя не понял. Переформулируй пожалуйста.\nЧтобы получить справку по командам, напиши "справка"'
sq=3
while sq<10:
    command['question %d' %sq]['answer'][0]=rasp(command['question %d' %sq]['txt'][0].encode('utf-8'))
    sq+=1

while True:

    lastMessages = messagesGet(200,appName)
    startWork(lastMessages, command, appName)

    time.sleep(1)
