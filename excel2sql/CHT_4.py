#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2018/5/25 <br>
# Time: 17:31 <br>
# Desc:

import csv
import os
import sys
import time


csv.field_size_limit(500 * 1024 * 1024)


def handle_csv(csv_file_name, csv_re_file_name):
	reader = csv.reader(open(csv_file_name, 'r'))
	head_row = next(reader)  # 读取一行，下面的reader中已经没有该行了
	for row in reader:  # 按行处理csv文件
		# 行号从2开始
		col_0 = row[0]  # 第一列，不处理
		col_1 = row[1]  # 第二列
		col_2 = row[2]  # 第三列
		col_3 = row[3]  # 第四列
		col_4 = row[4]  # 第五列
		col_5 = row[5]  # 第六列
		col_6 = row[6]  # 第七列，不处理
		title_header = [head_row[1], head_row[2], head_row[3], head_row[4], head_row[5]]
		# 只处理2003summer、2003winter、2004summer、2004winter、b1
		summer_2003_data = col_1.lstrip("[").rstrip("]").split(",")  # 去掉[]，并以逗号分隔数据成数组
		winter_2003_data = col_2.lstrip("[").rstrip("]").split(",")  # 去掉[]，并以逗号分隔数据成数组
		summer_2004_data = col_3.lstrip("[").rstrip("]").split(",")  # 去掉[]，并以逗号分隔数据成数组
		winter_2004_data = col_4.lstrip("[").rstrip("]").split(",")  # 去掉[]，并以逗号分隔数据成数组
		b1_data = col_5.lstrip("[").rstrip("]").split(",")  # 去掉[]，并以逗号分隔数据成数组

		summer_2003_len = len(summer_2003_data)
		winter_2003_len = len(winter_2003_data)
		summer_2004_len = len(summer_2004_data)
		winter_2004_len = len(winter_2004_data)
		b1_len = len(b1_data)

		csv_re_file = open(csv_re_file_name, 'w', encoding='utf8', newline='')  # 打开一个文件
		csv_writer = csv.writer(csv_re_file)  # 创建一个writer
		csv_writer.writerow(title_header)

		for i in range(max(summer_2003_len, winter_2003_len, summer_2004_len, winter_2004_len, b1_len)):
			summer_2003_cell = ""
			winter_2003_cell = ""
			summer_2004_cell = ""
			winter_2004_cell = ""
			b1_cell = ""
			if i < summer_2003_len:
				summer_2003_cell = summer_2003_data[i].strip()
			if i < winter_2003_len:
				winter_2003_cell = winter_2003_data[i].strip()
			if i < summer_2004_len:
				summer_2004_cell = summer_2004_data[i].strip()
			if i < winter_2004_len:
				winter_2004_cell = winter_2004_data[i].strip()
			if i < b1_len:
				b1_cell = b1_data[i].strip()
			row_data = [summer_2003_cell, winter_2003_cell, summer_2004_cell, winter_2004_cell, b1_cell]
			csv_writer.writerow(row_data)  # 将该row写入csv文件，row中每个内容占一个单元格

		csv_re_file.close()  # 关闭该csv文件


def iterate_path(filepath):
	# 遍历filepath下所有文件，包括子目录
	paths = os.listdir(filepath)
	for fi in paths:
		fi_d = os.path.join(filepath, fi)
		if os.path.isdir(fi_d):  # 如果是目录，则继续遍历
			iterate_path(fi_d)
		else:  # 如果是文件，则处理该文件
			csv_file_name = os.path.join(filepath, fi_d)  # 处理前全路径文件名
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Handle the file: ", csv_file_name)
			csv_re_file_name = filepath + "\\" + fi.split(".")[0] + "_re.csv"  # 处理后全路径文件名
			csv_file = open(csv_re_file_name, 'w', encoding='utf8', newline='')  # 打开一个文件
			csv_writer = csv.writer(csv_file)  # 创建一个writer
			title_list = ['LST_Day_1km', 'b1']  # 创建结果文件的表头
			csv_writer.writerow(title_list)  # 将该row写入csv文件，row中每个内容占一个单元格
			csv_file.close()
			handle_csv(csv_file_name, csv_re_file_name)


def main(path):
	iterate_path(path)


if __name__ == "__main__":
	# path = "D:\Document\Google Earth\4"  # 文件目录
	# main(path)
	main(sys.argv[1])
