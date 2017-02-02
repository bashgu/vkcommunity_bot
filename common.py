#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from vkGroupApi import *
import config
import deepdish as dd
base2=dd.io.load('base2.h5')

#######################################################

def findCommand(read,command,row,appName):
    # перебераем в цикле наш словарь команд и отправляем сообщение если нашли

    for cmd,otvet in command.iteritems():
        attachment=''
        sticker_id=''

        # если нашли совпадение команды
        if read in otvet['txt']:

            if 'attachment' in otvet:
                attachment = otvet['attachment']

            if 'sticker_id' in otvet:
                messagesSend(row['user_id'],row['id'],'','',otvet['sticker_id'],appName=appName)

            if not 'answer' in otvet:
                otvet['answer']=''

            time.sleep(1)

            result = messagesSend(row['user_id'],row['id'],otvet['answer'][0],attachment,appName=appName)

            if not result:
                print 'Break ...'
                break

            print '------------------------------'
            print (str(row['user_id'])+': "'+read + '" --> ' + cmd)

            return True # нашли команду и выходим

    return False


def startWork(lastMessages, command, appName, noAnswerSend=True):

    for row in lastMessages:

        status=0

        if int(row['read_state']) == 0:

            # очищаем текст пользователя
            read = stripRead(row['body'])

            # перебераем в цикле наш словарь команд и отправляем если нашли
            status=findCommand(read,command,row,appName)

            if status==0 and noAnswerSend:
                # print (str(i['user_id'])+': "'+read + '" != Не понял команду')
                messagesSend(row['user_id'],row['id'],command['question 0']['answer'], appName=appName)
                base2['question'].append(read)
                dd.io.save('base2.h5',base2)

                return False





def stripRead(read):
    # очищаем текст пользователя

    read = read.encode('utf8')
    read = read.decode('utf8').lower()
    read = read.strip('.').strip('!').strip('?').strip('/')

    return read


def loadCommands(command):
    ckeysList=[]
    for key,row in command.iteritems():
        if not 'skip' in row:
            if row['txt'][0]!='skip':
                ckeysList.append(row['txt'][0])

    ckeys='\n'.join(ckeysList)
    print ckeys

    return ckeys
