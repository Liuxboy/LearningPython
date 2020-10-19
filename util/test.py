#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:
import re as regx
import time

a = 1.13
if a > 1:
    print(True)
else:
    print(False)
data = '1600147108|  0   0 100   0   0| 251M 1324M 2108k  224M|   0  2048M|   0     0 |0.02 0.02 0.05|  20k 2540b|11.7G 5461M: 192M  822M'
# print(regx.split(r'\s+|\|', data))
# print(list(filter(None, regx.split(r'\s+|\|', data))))
regex = regx.compile('\s+|\||:')
print(regex.split(data))
lt = [0, 1, 2, 3, 4, 5]
print(lt[1:])

sp=time.time()
print(sp)
print("4.把时间戳转成字符串形式: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sp)))

for i in range(60):
    print(i)