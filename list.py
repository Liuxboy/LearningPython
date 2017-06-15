#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/2/20 <br>
# Time: 17:22 <br>
# Desc:

classmates = ['Michael', 'Bob', 'Tracy']
print(classmates)
print(len(classmates))
classmates.insert(1, 'Jack')
classmates.append("Lcd")
print(classmates)
lcd = classmates.pop(len(classmates) - 1)
print(lcd)
print(classmates)
L = ['Apple', 123, True]
print(L)
S = ['python', 'java', ['asp', 'php'], 'scheme']
print(S)
print(len(S))
print(S[2])

# homework of list
L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
# 打印Apple
print(L[0][0])
# 打印Python
print(L[1][1])
# 打印Lisa
print(L[2][2])
