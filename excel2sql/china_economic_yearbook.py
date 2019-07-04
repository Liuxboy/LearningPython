#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2018/1/24 <br>
# Time: 17:31 <br>
# Desc:
import msoffcrypto

import xlrd


def open_excel(file_name):
	try:
		data = xlrd.open_workbook(file_name)
		return data
	except Exception as e:
		print(e)


# 根据索引获取Excel表格中的数据参数
def handle_excel_table(file_name):
	old_excel = open_excel(file_name)
	sheets = old_excel.sheets()
	for sheet in sheets:
		rows = sheet.nrows  # 行数
		cols = sheet.ncols  # 列数
		header = ""     # 头两行
		city = ""       # 省市
		index = []      # 指标行

		# 遍历所有行
		for row_num in range(0, rows):
			arow = sheet.row_values(row_num)
			# 头两行
			if row_num % 34 == 0:
				header = arow[0]
			if row_num % 34 == 1:
				city = arow[0]
			# 指标
			if (row_num % 34) > 1:
				_row = (row_num - 2) % 30
				index.insert(_row, arow[0])

		print(header)
		print(city)
		print(index)


def handle_protected_workbook(wb_filepath):
	try:
		xlrd.open_workbook(wb_filepath)
	except xlrd.biffh.XLRDError as e:
		if e.args[0] == "Workbook is encrypted":
			# Try and unencrypt workbook with magic password
			wb_msoffcrypto_file = msoffcrypto.OfficeFile(open(wb_filepath, 'rb'))
			try:
				# Yes, this is actually a thing
				# https://nakedsecurity.sophos.com/2013/04/11/password-excel-velvet-sweatshop/
				wb_msoffcrypto_file.load_key(password='VelvetSweatshop')
			except AssertionError as e:
				if e.args[0] == "Failed to verify password":
					# Encrypted with some other password
					raise  # or do something else
				else:
					# Some other error occurred
					raise
			except:
				# Some other error occurred
				raise
			else:
				# Magic Excel password worked
				assert wb_filepath.endswith('.xls')
				wb_unencrypted_filename = wb_filepath[:-(len('.xls'))] + '__unencrypted.xls'
				wb_msoffcrypto_file.decrypt(open(wb_unencrypted_filename, 'wb'))
				# --- Do something with the file ---
				# return true to indicate file was touched
				return True  # or do something else
		else:
			# some other xlrd error occurred.
			return False  # or do something else
	except:
		# some non-xlrd error occurred.
		return False  # or do something else


if __name__ == "__main__":
	#handle_protected_workbook('D:\Gitspace\LearningPython\excel2sql\county\999\上海.xls')
	handle_excel_table(r'D:\Gitspace\LearningPython\excel2sql\county\999\上海__unencrypted.xls')
