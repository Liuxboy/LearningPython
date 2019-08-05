#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2019-7-13 <br>
# Time: 8:51 <br>
# Desc:
import datetime

a = None
print(a or 0)
a = 10
print(a or 0)

time = datetime.datetime.now().strftime('%H%M')
if "0900" <= time <= "1500":
	print("now is %s, it's trade time" % time)
else:
	print("now is %s, it's not trade time" % time)

s = ""
t = ()
lt = []
d = {}
n = None
if s:
	print("str is not empty")
else:
	print("str is empty")

if not t:
	print("t is not empty")
else:
	print("t is empty")

if d:
	print("d is not empty")
else:
	print("d is not empty")

if not n:
	print("n is not None")
else:
	print("n is None")
