#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-1-19 <br>
# Time: 13:43 <br>
# Desc:

import gevent, time
from gevent import monkey

import pymysql

gevent.monkey.patch_socket()

total = 1000


def testinsertonupdate(num):
	start = time.time()

	def goodquery(sql, i):
		db = pymysql.connect(host='localhost', user='root', passwd='root', db='test', autocommit=True)
		cursor = db.cursor()
		cnt = int(total / num)
		sql = sql.format(thread_id=i)
		for i in range(cnt):
			cursor.execute(sql)
		cursor.close()
		db.close()

	sql = 'INSERT INTO `testa` VALUES (1,1) ON DUPLICATE KEY UPDATE num=num+1;'
	jobs = [gevent.spawn(goodquery, sql, i) for i in range(num)]
	gevent.joinall(jobs)
	res = time.time() - start
	return res


if __name__ == '__main__':
	print("开始时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	sample = [1, 125]
	#sample = [1, 2, 5, 10, 20, 50, 100, 125, 200]
	x = [testinsertonupdate(x) for x in sample]
	print(x)
	print("结束时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
