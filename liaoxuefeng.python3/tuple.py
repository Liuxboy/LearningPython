#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/2/20 <br>
# Time: 18:08 <br>
# Desc:
# tuple 初始化后就不可以更改
tuples = ('LCD', 'ZW', 'LH')
print(tuples)
# list 初始化后可以随时更改
classmates = ['Michael', 'Bob', 'Tracy']
print(classmates[-1])
print(classmates[-2])
print(classmates[-3])
print(classmates.pop())
print(classmates.pop(1))
t = (1)
print(t)
t = (1,)
print(t)
t = ('a', 'b', ['A', 'B'])
t[2][0] = 'X'
t[2][1] = 'Y'
print(t)
# t[0] = 'c'   # TypeError: 'tuple' object does not support item assignment
print(t)
t = ('a', 'b', ('A', 'B'))
t[2][0] = 'X'   # 元组不可更改
t[2][1] = 'Y'   # 元组不可更改
print(t)

