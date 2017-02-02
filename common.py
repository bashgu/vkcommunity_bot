#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import random
import time
import xlrd, xlwt
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from vkGroupApi import *
import config
import deepdish as dd
base2=dd.io.load('base2.h5')

#######################################################

def rasp(perm):
    rb = xlrd.open_workbook('./excel.xls',formatting_info=True)
    sheet = rb.sheet_by_index(0)
    i = 0
    j = 1
    timetable = {}
    status = False
    while True:
        if sheet.row_values(i)[0].encode('utf-8') != 'время': i += 1
        else:
            i += 1
            break

    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    while True:
        if sheet.row_values(i)[0] == '': i += 1
        else:
            q = i+1
            val = sheet.row_values(i)[0]
            x = int(val * 24 * 3600)
            my_time = datetime.time(x/3600, (x%3600)/60, x%60)
            if len(str(my_time.hour))==1:
                timetable['0'+str(my_time.hour)+':'+str(my_time.minute)[0]+'0'] = {}
                val = '0'+str(my_time.hour)+':'+str(my_time.minute)[0]+'0'
            else:
                timetable[str(my_time.hour)+':'+str(my_time.minute)[0]+'0'] = {}
                val = str(my_time.hour)+':'+str(my_time.minute)[0]+'0'
            if val == '21:00': status = True
            while True:
                if status == True:
                    if sheet.row_values(q)[2].encode('utf-8') == 'Аэробные классы': break
                    else: q += 1
                else:
                    if sheet.row_values(q)[0] == '': q += 1
                    else: break
            while True:
                if j == 8:
                    j = 1
                    break
                else:
                    start = i
                    end = q
                    forday = ''
                    while True:
                        if start >= end:
                            if forday != '':
                                timetable[val][days[j-1]] = forday
                            j += 1
                            break
                        elif sheet.row_values(start)[j] == '':
                            start = end
                        else:
                            forday += sheet.row_values(start)[j] + ', ' + sheet.row_values(start+1)[j] + '\n'
                            start += 2
            if status == True: break
            else: i = q
    k=timetable.keys()
    k=sorted(k)
    s = ''
    for key in k:
        try:
            timetable[key][perm]
            s += u'В %s будет:\n' %key + timetable[key][perm] +'\n'
        except KeyError:
            pass
    return s

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
