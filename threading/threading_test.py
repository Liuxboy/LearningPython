#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2019-7-10 <br>
# Time: 14:44 <br>
# Desc:

import threading
import time

num = 0
# 创建一把锁
mutex = threading.Lock()


class MyThread(threading.Thread):
	def run(self):
		global num
		# 上锁
		mutex_flage = mutex.acquire()
		print('线程(%s)的锁状态为%d' % (self.name, mutex_flage))
		# 判断是否上锁成功
		if mutex_flage:
			num = num + 1
			time.sleep(1)
			msg = self.name + 'set num to' + str(num)
			print(msg)
			print(threading.currentThread(), threading.activeCount())
			mutex.release()


def test():
	for i in range(5):
		t = MyThread()
		print(threading.currentThread(), threading.activeCount())
		t.start()


if __name__ == '__main__':
	test()
