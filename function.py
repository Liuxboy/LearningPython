#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project:LearningPython
# Author: liuchundong <br>
# Date: 2017-12-25 <br>
# Time: 14:51 <br>
# Desc:
"""
built-ins function
"""

print(abs(-10.19))
print(abs(1000.00))
print(abs(0))
print(max(1, 20, -10, 5, 0))
print(bool(1))
print(bool(0))
print(bool(''))
print(bool(' '))
a = abs
print(a(-1))

def my_abs(x):
	if x > 0:
		return x
	elif x == 0:
		return 0
	else:
		return -x