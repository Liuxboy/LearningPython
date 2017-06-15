#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/5/17 <br>
# Time: 11:08 <br>
# Desc: 

a = int(input())
b = int(input())
c = int(input())
d = int(input())
point = 517
if a + b - c * d == point:
    print('a + b - c * d')
elif a + b - c / d == point:
    print('a + b - c / d')
elif a + b * c / d == point:
    print('a + b * c / d')
elif a + b * c - d == point:
    print('a + b * c - d')
elif a + b / c * d == point:
    print('a + b / c * d')
elif a + b / c - d == point:
    print('a + b / c - d')

elif a - b + c * d == point:
    print('a - b + c * d')
elif a - b + c / d == point:
    print('a - b + c / d')
elif a - b * c + d == point:
    print('a - b * c + d')
elif a - b * c / d == point:
    print('a - b * c / d')
elif a - b / c + d == point:
    print('a - b / c + d')
elif a - b / c * d == point:
    print('a - b / c * d')

elif a * b + c - d == point:
    print('a * b + c - d')
elif a * b + c / d == point:
    print('a * b + c / d')
elif a * b - c * d == point:
    print('a * b - c * d')
elif a * b - c / d == point:
    print('a * b - c / d')
elif a * b / c + d == point:
    print('a * b / c + d')
elif a * b / c - d == point:
    print('a * b / c - d')

elif a / b + c - d == point:
    print('a / b + c - d')
elif a / b + c * d == point:
    print('a / b + c * d')
elif a / b - c + d == point:
    print('a / b - c + d')
elif a / b - c * d == point:
    print('a / b - c * d')
elif a / b * c - d == point:
    print('a / b * c - d')
elif a / b * c + d == point:
    print('a / b * c + d')
else:
    print("没有找到解法")

