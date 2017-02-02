#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import deepdish as dd
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

a=''
l='0'
base2=dd.io.load('base2.h5')
base=dd.io.load('base.h5')
q=len(base2['question'])
print q
for i in range(q):
    print u'вопрос: ',base2['question'][0].decode('utf-8')
    print u'Введите 1, если хотите добавить этот вопрос или введите 0 чтобы удалить его',
    l=raw_input()
    if l=='1':
        print u'введите ответ: ',
        a=raw_input()
        a=a.lower()
        base['question'].append(base2['question'][0].lower())
        base['answer'].append(a.decode('cp866'))
    base2['question'].pop(0)
    dd.io.save('base2.h5',base2)
    dd.io.save('base.h5',base)
print u'Вопросы закончились'
raw_input()
