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

dialogs=[]

#######################################################

def findCommand(words,command,row,appName):
    # перебераем в цикле наш словарь команд и отправляем сообщение если нашли

    for cmd,otvet in sorted(command.iteritems()):
        attachment=''
        sticker_id=''
        # если нашли совпадение команды
        for read in words.split():
            read = read.strip('.').strip('!').strip('?').strip('/').strip(',').strip(' ')
            if read in otvet['txt']:
                
                global x
                x=1

                if 'attachment' in otvet:
                    attachment = otvet['attachment']

                if 'sticker_id' in otvet:
                    messagesSend(row['user_id'],row['id'],'','',otvet['sticker_id'],appName=appName)

                if not 'answer' in otvet:
                    otvet['answer']=''
                time.sleep(1)

                result = messagesSend(row['user_id'],row['id'],otvet['answer'],attachment,appName=appName)

                if not result:
                    print 'Break ...'
                    break

                print '------------------------------'
                print (str(row['user_id'])+': "'+read + '" --> ' + cmd)

            #return True # нашли команду и выходим
    print(x)
    return False

def startWork(lastMessages, command, appName, noAnswerSend=True, dialogs={}):

    for row in lastMessages:

        global x
        x=0

        if int(row['read_state']) == 0:

            # очищаем текст пользователя
            read = stripRead(row['body'])

            # перебераем в цикле наш словарь команд и отправляем если нашли
            status=findCommand(read,command,row,appName)

            if x==0:
                print(x)
                if not row['user_id'] in dialogs:
                    # посылаем в 1 сообщении faq
                    messagesSend(row['user_id'],row['id'],command['0']['answer'], appName=appName)
                    dialogs[row['user_id']]='1'
                    print (str(row['user_id'])+': "'+read + '" -->  first FAQ' )

                elif x==0:                    # print (str(i['user_id'])+': "'+read + '" != Не понял команду')
                    messagesSend(row['user_id'],row['id'],'Прости, не понял тебя.' + command['1']['answer'], appName=appName)
                    print (str(row['user_id'])+': "'+read + '" -->  Dont understand' )

                    return False



def firstAnswer():

    # for user_id,j in userList.iteritems():
    #     # Первое сообщение
    #
    #     ustxtany = ['']
    #     textw1 = 'Добро пожаловать, мы скинем вам рассписание скажите свою группу'
    #
    #     if j['status'] == 0:
    #         messagesSend(user_id,j['msg_id'],textw1,'photo,photo-128566598_432688189')
    #         j['status'] = 0

    return

def userList():
    # for items in dialogs:
    #     user_id = items['message']['user_id']
    #     user['msg_id'] = items['message']['user_id']
    #     user['status'] = 0
    #
    #     userList[user_id]=user
    return

def stripRead(read):
    # очищаем текст пользователя

    read = read.encode('utf8')
    read = read.decode('utf8').lower()

    return read


def loadCommands(command):
#    ckeysList=[]
    for key,row in command.iteritems():
        if not 'skip' in row:
            ckeysList.append(row['txt'][0])

    ckeys=', '.join(ckeysList)
    print ckeys
    return ckeys
