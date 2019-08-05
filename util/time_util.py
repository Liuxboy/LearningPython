#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2019-7-8 <br>
# Time: 14:47 <br>
# Desc:

import datetime

dt = datetime.datetime.now()
print('时间：(%Y-%m-%d %H:%M:%S %f): ', dt.strftime('%Y-%m-%d %H:%M:%S %f'))
print('时间：(%Y-%m-%d %H:%M:%S %p): ', dt.strftime('%y-%m-%d %I:%M:%S %p'))
print('星期缩写%%a: %s ' % dt.strftime('%a'))
print('星期全拼%%A: %s ' % dt.strftime('%A'))
print('月份缩写%%b: %s ' % dt.strftime('%b'))
print('月份全批%%B: %s ' % dt.strftime('%B'))
print('日期时间%%c: %s ' % dt.strftime('%c'))
print('今天是这周的第%s天 ' % dt.strftime('%w'))
print('今天是今年的第%s天 ' % dt.strftime('%j'))
print('今周是今年的第%s周 ' % dt.strftime('%U'))
print('今天是当月的第%s天 ' % dt.strftime('%d'))


today_0_hour = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
today = datetime.date.today().strftime('%Y-%m-%d')
hour_min = datetime.datetime.now().strftime('%H%M')


print('today_0_hour:%s' % today_0_hour)
print('today:%s' % today)
print('now hour:min %s' % hour_min)


