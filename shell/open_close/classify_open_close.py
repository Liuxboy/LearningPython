#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2018/1/24 <br>
# Time: 17:31 <br>
# Desc:

import xlrd
import xlwt


def open_excel(file_name):
	try:
		data = xlrd.open_workbook(file_name)
		return data
	except Exception as e:
		print(str(e))


# 根据索引获取Excel表格中的数据参数
def excel_table_byindex(file_name, by_index=0):
	old_excel = open_excel(file_name)
	sheet = old_excel.sheets()[by_index]
	rows = sheet.nrows  # 行数
	year_dates = []
	open_dates = []
	close_dates = []
	sql_file = open("2019_open_close_date.sql", "w", encoding="utf-8")
	sql_file.write("INSERT INTO ts_xs_close_date (`close_date`) VALUES \n")

	# 遍历全年
	for row_num in range(1, rows):
		arow = sheet.row_values(row_num)
		if arow:
			# 全年日期
			year_date = sheet.cell_value(row_num, 0)
			date = xlrd.xldate.xldate_as_datetime(year_date, 0)
			year_dates.append(date.strftime('%Y-%m-%d'))

			# 遍历节假日
			close_date = sheet.cell_value(row_num, 3)
			if close_date != "":
				date = xlrd.xldate.xldate_as_datetime(close_date, 0)
				close_dates.append(date.strftime('%Y-%m-%d'))

	# 筛选出开市日
	for day in year_dates:
		if day in close_dates:
			sql_file.write("('" + str(day) + "'),\n")
		else:
			open_dates.append(day)

	new_excel = xlwt.Workbook()
	new_sheet = new_excel.add_sheet('sheet 1')
	new_sheet.write(0, 0, '开市日期')

	sql_file.write("INSERT INTO ts_xs_open_date (`open_date`) VALUES \n")
	i = 1
	for day in open_dates:
		sql_file.write("('" + str(day) + "'),\n")
		new_sheet.write(i, 0, str(day))
		i += 1

	sql_file.close()
	# 另存为excel文件，并将文件命名
	new_excel.save('2019_open_date.xls')


if __name__ == "__main__":
	excel_table_byindex("2019_open_close_date.xlsx", 0)

