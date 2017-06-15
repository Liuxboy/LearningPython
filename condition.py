#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/5/15 <br>
# Time: 13:31 <br>
# Desc: 
age = 1
if age >= 18:
    print('your age is', age)
    print('adult')
elif age > 8:
    print('your age is', age)
    print('teenager')
else:
    print('kid')
# 它是从上往下判断，如果在某个判断上是True，把该判断对应的语句执行后
# 就忽略掉剩下的elif和else，所以有短路作用
age = 20
if age >= 6:
    print('teenager')
elif age >= 18:
    print('adult')
else:
    print('kid')

# 只要x是非零数值、非空字符串、非空list等，就判断为True，否则为False
x = 'a'
if x:
    print(x + x)
'''
birth = input('birth: ')
if birth < 2000:
    print('00前')
else:
    print('00后')
'''

birth = input('birth: ')
if int(birth) < 2000:
    print('00前')
else:
    print('00后')

weight = 61.5
height = 1.80
bmi = weight / (height * height)
print("bmi:", bmi)
if bmi < 18.5:
    print("过轻")
elif 18.5 <= bmi < 25:
    print("正常")
elif 25 <= bmi < 28:
    print("过重")
elif 28 <= bmi < 32:
    print("肥胖")
else:
    print("严重肥胖")
