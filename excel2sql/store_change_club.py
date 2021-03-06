#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/6/14 <br>
# Time: 17:31 <br>
# Desc:

import xlrd
import re
import datetime
import sys


def open_excel(file_name):
    try:
        data = xlrd.open_workbook(file_name)
        return data
    except Exception as e:
        print(str(e))


# 根据索引获取Excel表格中的数据参数:file：Excel文件路径，col_name_index：表头列名所在行，by_index：表的索引
def excel_table_byindex(file_name, col_name_index=0, by_index=0):
    data = open_excel(file_name)
    table = data.sheets()[by_index]
    rows = table.nrows  # 行数
    col_names = table.row_values(col_name_index)  # 表头
    data_list = []
    for row_num in range(1, rows):
        row = table.row_values(row_num)
        if row:
            app = {}
            for i in range(len(col_names)):
                if re.sub('\s', '', col_names[i]) == "转出客户编码":
                    app["src_club_no"] = row[i]
                elif re.sub('\s', '', col_names[i]) == "转入客户编码":
                    app["des_club_no"] = row[i]
                elif re.sub('\s', '', col_names[i]) == "门店代码必须为3开头的宙斯中的代码":
                    app["store_no"] = row[i]
                    # if re.sub('\s', '', col_names[i]) in '转出客户编码,转入客户编码,门店代码必须为3开头的宙斯中的代码':
                    #     app[col_names[i]] = row[i]
            data_list.append(app)
    return data_list


def write_sql(sql_file, src_club_no, des_club_no, store_no):
    desc = "-- 门店编码:%s, 转出商户编码:%s, 转入客户编码:%s\n" % (store_no, src_club_no, des_club_no)
    update_dep_sql = "UPDATE p_dep SET PARENT_NUM = '%s', CREATE_USER = (SELECT pd1.CREATE_USER FROM (SELECT * FROM p_dep) AS pd1 WHERE pd1.CODE = '%s'), UPDATE_USER = (SELECT pd2.CREATE_USER FROM (SELECT * FROM p_dep) AS pd2 WHERE pd2.CODE` = '%s') WHERE `CODE` = '%s';\n" % (
        des_club_no, des_club_no, des_club_no, store_no)
    update_role_sql = "UPDATE p_role SET COMPANY_NO = '%s' WHERE DEP_ID = '%s';\n" % (des_club_no, store_no)
    update_user_sql = "UPDATE p_user_role SET U_ID = (SELECT ID FROM p_user WHERE `NAME` = (SELECT CREATE_USER FROM p_dep WHERE `CODE` = '%s')) WHERE R_ID IN (SELECT ID FROM p_role WHERE dep_id = '%s');\n\n\n" % (
        des_club_no, store_no)

    sql_file.write(desc)
    sql_file.write(update_dep_sql)
    sql_file.write(update_role_sql)
    sql_file.write(update_user_sql)


def main(file_name):
    tables = excel_table_byindex(file_name)
    sql_file = open("store_change_club_%s.sql" % (datetime.date.today()), "w", encoding="utf-8")
    for row in tables:
        write_sql(sql_file, re.sub('\s|\.[0-9]+', '', str(row["src_club_no"])),
                  re.sub('\s|\.[0-9]+', '', str(row["des_club_no"])), re.sub('\s|\.[0-9]+', '', str(row["store_no"])))
    print("总共纪录数：", len(tables))
    sql_file.close()


if __name__ == "__main__":
    main(sys.argv[1])
