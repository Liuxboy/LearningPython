#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-1-20 <br>
# Time: 11:21 <br>
# Desc:


def f(q):
	sumamount = 0
	for i in (range(10, 20)):
		sumamount += q ** i
	return sumamount - 20


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

print("最终结果：%s" % (a - 1))
print("逼近结果：", re)
