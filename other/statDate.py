#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-5-8 <br>
# Time: 9:49 <br>
# Desc:

import random

# 原始数据，30个[10，16]之间的整数
aMonth = []
for i in range(30):
	aMonth.append(random.randint(10, 16))
print("原始数据:", str(aMonth))
# 结果
reMonth = []
# 阈值
threshold = 13
print("阈值:", threshold)
# 遍历1号到28的窗口期
for n in range(28):
	# 如果窗口期第一天，第二天，第三天都大于阈值，则将改窗口期第一天标记为1
	if aMonth[n] > threshold and aMonth[n + 1] > threshold and aMonth[n + 2] > threshold:
		reMonth.append(n + 1)
	else:
		reMonth.append(0)
print("窗口计算结果(0表示不满足条件):", str(reMonth))
# 窗口日期(号)
windowDate = 0
# 窗口日期最长的长度(天)
windowDateMaxLength = 0
for m in range(len(reMonth)):
	length = 0
	n = m
	while reMonth[n] != 0:
		n += 1
		length += 1
	# 如果发现length比前面的最大窗口长度还大，则替换之
	if length > windowDateMaxLength:
		windowDateMaxLength = length
		windowDate = m + 1
if windowDate == windowDateMaxLength == 0:
	print("没有长到符合调教的窗口期")
else:
	print("最大窗口日期在:", windowDate, "号，其长度为:", windowDateMaxLength + 2, "天")
