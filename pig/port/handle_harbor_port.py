#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2018/1/24 <br>
# Time: 17:31 <br>
# Desc:
import logging
import sys

import pymysql
import requests
from pymysql.cursors import DictCursor

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s-- %(funcName)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def mysql_exe(sql):
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    db = pymysql.connect(host="localhost", user="root", password="root", database="pig", cursorclass=DictCursor)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 更新语句
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return cursor.fetchall()
    except:
        # 发生错误时回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()
        cursor.close()


def get_urls():
    sql = """
            SELECT ID, URL 
            FROM pig.{}
            WHERE URL IS NOT NULL 
            AND RESPONSE_JSON IS NULL 
            AND UPDATE_TIME < now()
        """.format(port_type)
    return mysql_exe(sql)


def handle_port():
    headers = {
        "Accept-Encoding": "gzip, deflate, en",
        "Cookie": "__cfduid=da92a27d729da26b44d4baade8ab2df4e1583138869; SERVERID=app5",
        "Accept": "*/*",
        "User-Agent": "PostmanRuntime/7.23.0",
        "Cache-Control": "no-cache",
        "Host": "www.marinetraffic.com",
        "Postman-Token": "c33e745a-5184-45c3-b343-651b27163ca6"
    }
    urls = get_urls()
    if urls:
        for row in urls:
            _id = row['ID']
            _url = row['URL']
            logging.info("handle the id: %s", _id)
            response = requests.get(_url, headers=headers)
            result = response.text
            update_sql = "UPDATE pig.{} SET RESPONSE_JSON = '{}' WHERE ID = {}".format(port_type, result, _id)
            mysql_exe(update_sql)


def main():
    mysql_exe("UPDATE pig.{} SET RESPONSE_JSON = NULL WHERE UPDATE_TIME < DATE_FORMAT(now(), '%Y-%m-%d')".format(port_type))
    handle_port()


if __name__ == "__main__":
    port_type = sys.argv[1]
    try:
        main()
    except Exception as ex:
        logging.error("some errors has occurred! %s", ex, exc_info=True)
        handle_port()
    finally:
        ext = input("Please input any key to exit：")
        if ext:
            exit(0)
