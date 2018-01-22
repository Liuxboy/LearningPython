#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-1-18 <br>
# Time: 14:25 <br>
# Desc:
# coding=utf-8

import threading
import queue
import time
import urllib

from urllib import request

baseUrl = 'http://www.pythontab.com/html/pythonjichu/'
urlQueue = queue.Queue()
for i in range(2, 20):
	url = baseUrl + str(i) + '.html'
	urlQueue.put(url)
# print(url)


def fetch_url(url_queue):
	while True:
		try:
			# 不阻塞的读取队列数据
			url = urlQueue.get_nowait()
			i = urlQueue.qsize()
		except Exception as e:
			break
		print('Current Thread Name %s, Url: %s ' % (threading.currentThread().name, url))
		try:
			response = urllib.request.urlopen(url)
			response_code = response.getcode()
		except Exception as e:
			continue

		if response_code == 200:
			# 抓取内容的数据处理可以放到这里
			# 为了突出效果， 设置延时
			time.sleep(1)


if __name__ == '__main__':
	startTime = time.time()
	threads = []
	# 可以调节线程数， 进而控制抓取速度
	threadNum = 8
	for i in range(0, threadNum):
		t = threading.Thread(target=fetch_url, args=(urlQueue,))
		threads.append(t)
	for t in threads:
		t.start()
	for t in threads:
		# 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
		t.join()
	endTime = time.time()
	print('Done, Time cost: %s ' % (endTime - startTime))
