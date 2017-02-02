#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random
import deepdish as dd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#######################################################

from vkGroupApi import *
import config
from common import *

appName='house'

#######################################################


#######################################################

base=dd.io.load('base.h5')
print 'Started...'+appName

# Словарь для команд

command = {'question %d' %a:{'txt':[base['question'][a]],'answer':[base['answer'][a]]} for a in range(len(base['question']))}

#список всех комананд, для помощи
ckeys = loadCommands (command)
command['question 0']['answer']='Переформулируйте пожалуйста. Возможно вы хотели узнать ответы на эти вопросы? Введи вопрос полностью или цифру!\n1)Где у вас можно купить квартиры?\n2)В каком районе есть квартиры?\n3)Где вы строите?\n4)Скольких комнатные у вас квартиры?\n5)По чем однушки?\n6)Есть ли однушки?\n7)Сколько квадратов 1 комн. кв.?\n8)Какие планировки 1 комн. кв.?\n9)Сколько квадратов 2 комн. кв.?\n10)Какие планировки 2 комн. кв.?\n11)Сколько квадратов 3 комн. кв.?\n12)Какие планировки 3 комн. кв.?\n13)Какие цены на квартиры?\n14)Какая отделка?\n15)Есть ли у Вас рассрочка?\n16)Можно купить квартиру в ипотеку?\n17)Работаете ли Вы с материнским капиталом?\n18)Где можно посмотреть проектную декларацию?\n19)Есть ли у Вас разрешение на строительство?\n20)С какими банками Вы работаете?'

while True:

    lastMessages = messagesGet(200,appName)
    startWork(lastMessages, command, appName)

    time.sleep(1)
