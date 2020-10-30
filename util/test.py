#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:
import datetime
import os
import sched
import time

a = datetime.datetime.strptime('20011018', '%Y%m%d')
b = datetime.datetime.today()
print(a)
print(b)
print((b - a) / 365.2422)

from threading import Timer
import datetime

s = sched.scheduler(time.time, time.sleep)


# 每隔两秒执行一次任务
def printHello():
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = Timer(2, printHello)
    t.start()
    time.sleep(6)


if __name__ == "__main__":
    # printHello()
    result = [1, 8, 3, 4, 5, 6]
    print('max:', max(result))
    for i in range(len(result) - 1, -1, -1):
        # print("index:", i)
        row = result[i]
        print("value:", row)
    print(os.path.split(os.path.realpath(__file__))[0])
