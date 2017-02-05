#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#######################################################

from vkGroupApi import *
import config
from common import *

appName='bro'

#######################################################

def loadAnekdot(count=100):

    import html2text

    resp = requests.get('http://www.umori.li/api/get?site=bash.im&name=bash&num={}'.format(count))

    result = resp.json()

    anekdot=[]

    for row in result:
        html=row['elementPureHtml']
        txt= html2text.html2text(html).strip().encode('utf-8')
        anekdot.append(txt)
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
    return anekdot


#######################################################

anekdot=loadAnekdot()

print 'Started...'+appName

# Словарь для команд

command = {
    'bro':{
        'txt':['бро','bro', 'привет','как дела']
        ,'answer':'bro!'
        ,'attachment':'photo,photo-128566598_432688170'
    },
    'lesson':{
        'txt':['расписание','что сегодня', 'на неделю', 'lesson']
        ,'answer':'Расписание: - нет расписания'
    },
    'shutka':{
        'txt':['шутка','анекдот','цитата','ещё','еще']
        ,'answer':anekdot[int(round(random.random()*98))]
    },
    'help':{
        'txt':['помощь','help']
        ,'answer':'Команды: '
    },
}

#список всех комананд, для помощи
ckeys = loadCommands (command)
command['help']['answer']='Что ты хочешь узнать? Например: '+ckeys+' ... просто набери любую из этих фраз'

#блок try...except добавил чтоб не выкидовало при ошибках

while True:
    try:

        lastMessages = messagesGet(200,appName)
        #command['shutka']['answer']=anekdot[int(round(random.random()*98))]

        startWork(lastMessages, command, appName)

        time.sleep(1)
    except Exception as inst:
        print inst
