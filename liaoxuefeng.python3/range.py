#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/5/16 <br>
# Time: 18:33 <br>
# Desc:

r = range(10)
print(list(r))

r = range(1, 10)
print(list(r))

r = range(1, 10, 2)
print(list(r))

r = range(1, 10)
v = range(1, 10, 1)
print(r == v)

r = range(0)
v = range(2, 1, 3)
print(r == v)

r = range(0, 3, 2)
v = range(0, 4, 2)
print(r != v)

for num in range(10, 20):  # 迭代 10 到 20 之间的数字
	print(num)
	for i in range(2, num):  # 根据因子迭代
		if num % i == 0:  # 确定第一个因子
			j = num / i  # 计算第二个因子
			print('%d 等于 %d * %d' % (num, i, j))
			break  # 跳出当前循环
	else:  # 循环的 else 部分
		print(num, '是一个质数')
