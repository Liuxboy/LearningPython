#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2018/1/24 <br>
# Time: 17:31 <br>
# Desc:

import xlrd


def open_excel(file_name):
	try:
		data = xlrd.open_workbook(file_name)
		return data
	except Exception as e:
		print(str(e))


# 根据索引获取Excel表格中的数据参数
def excel_table_byindex(file_name, col_name_index=0, by_index=0):
	data = open_excel(file_name)
	table = data.sheets()[by_index]
	rows = table.nrows  # 行数
	col_names = table.row_values(col_name_index)  # 表头
	data_list = []
	# 遍历行
	for row_num in range(0, rows):
		arow = table.row_values(row_num)
		if arow:
			# 遍历列
			row_str = ''
			# 字符串所在列
			# char_col = [0, 1, 3, 38, 40, 42, 43, 44, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]
			for col in range(len(col_names)):
				value = table.cell(row_num, col).value
				# if col in char_col:
				# 	row_str += "'" + str(value) + "', "
				# else:
				row_str += "`" + str(value) + "`, '|', "
			data_list.append(row_str)
	return data_list


if __name__ == "__main__":
	tables = excel_table_byindex("simple.xlsx")
	sql_file = open("ts_xs_annual_bill.sql", "w", encoding="utf-8")
	sql_file.write("INSERT INTO ts_xs_annual_account ()")
	for row in tables:
		sql_file.write(str(row) + "\n")

	print("总共纪录数：", len(tables))
	sql_file.close()
