#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-1-20 <br>
# Time: 11:21 <br>
# Desc:


def f(q):
	r = q ** 19 + q ** 18 + q ** 17 + q ** 16 + q ** 15 + q ** 14 + q ** 13 + q ** 12 + q ** 11 + q ** 10 - 20
	return r


print(f(1.00001))
print(f(1.00002))
print(f(1.00003))

a = 1.0000001
re = 1.000000
while abs(re) > 0.00001:
	a += 0.0000001
	re = f(a)
	print(a)
	print(re)

print("最终结果：%f", a - 1)
print("逼近结果：", re)
