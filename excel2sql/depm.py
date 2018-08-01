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
			row_str = "("
			# 前4列
			for col in range(4):
				value = table.cell(row_num, col).value
				row_str += "'" + str(value) + "',"
			row_str += "now()),"
			data_list.append(row_str)
	return data_list


if __name__ == "__main__":
	tables = excel_table_byindex("depm.xlsx", 0, 1)
	sql_file = open("ts_xd_department.sql", "w", encoding="utf-8")
	sql_file.write(
		"INSERT INTO ts_xd_department (`depart_code`,`depart_name`,`branch_office_code`, `branch_office_name`,`create_time`) VALUES ")
	for row in tables:
		sql_file.write(str(row) + "\n")

	print("总共纪录数：", len(tables))
	sql_file.close()
