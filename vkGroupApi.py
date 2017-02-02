#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random

from colorama import *
init(autoreset=True)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

appName='life'

#######################################################

def loadConfig(appName=appName):
    import config

    # print 'loaded config for:'+appName

    access_token = config.vk[appName]['access_token']
    peer_id = config.vk[appName]['peer_id']

    return access_token, peer_id

def requestVk(metod,param='',appName=appName):
    access_token, peer_id = loadConfig(appName)

    vk_url="https://api.vk.com/method/"
    vk_ver='5.53'

    resp = requests.get(vk_url+metod,param+'&access_token={}&v={}'.format(access_token,vk_ver))

    result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    try:
        if 'response' in result:
            if 'items' in result['response']:
                return result['response']['items']
            else:
                return result['response']

        elif 'error' in result:
            print (Fore.RED + 'error_msg: '+result['error']['error_msg'])
            return False

    except Exception as e:
        return result

#######################################################

def messagesGetDialogs(appName=appName):

    return requestVk('messages.getDialogs','',appName)


def messagesGet(count=30,appName=appName):

    return requestVk('messages.get',
                    '&count={}'.format(count),appName)


def messagesGetHistory(user_id,start_message_id='',count=30,appName=appName):

    return requestVk('messages.getHistory',
            '&user_id={}&start_message_id={}&peer_id={}&count={}'
            .format(user_id, start_message_id, peer_id, count),appName)


def messagesSend(user_id,chat_id=1,message='',attachment='',sticker_id='',appName=appName):
    access_token, peer_id = loadConfig(appName)

    result = requestVk('messages.send',
            '&user_id={}&peer_id={}&chat_id={}&message={}&attachment={}&sticker_id={}'
            .format(user_id,peer_id, chat_id,message,attachment,sticker_id),appName)

    return result
