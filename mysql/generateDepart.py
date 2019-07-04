#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-1-18 <br>
# Time: 13:04 <br>
# Desc:

import pymysql


def query():
	# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
	db = pymysql.connect("localhost", "root", "root", "test")
	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()

	# SQL 查询语句
	sql = "SELECT * FROM ts_xd_cid_stock"

	try:
		# 执行SQL语句
		cursor.execute(sql)
		# 获取所有记录列表
		results = cursor.fetchall()
		for row in results:
			cid = row[0]
			stock_position = row[1]
			stock_optional = row[2]
			# 打印结果
			print("cid=%s, stock_position=%s, stock_optional=%s" % (cid, stock_position, stock_optional))
	except:
		print("Error: unable to fetch data")
	finally:
		# 关闭数据库连接
		db.close()


if __name__ == '__main__':
	query()
