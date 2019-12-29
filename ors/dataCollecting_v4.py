# -*- coding: utf-8 -*-
import csv
import io
import json
import logging
import time
import sys
import os
import numpy as np
import pymysql
import requests

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='dataCollecting_v4.log',
                    level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s-- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

# 数据库配置
db_host = "localhost"
db_user = "root"
db_password = "root"
db_name = "ors"


# 执行sql语句
def execute(sql, args):
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    connection = pymysql.connect(db_host, db_user, db_password, db_name)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = connection.cursor()
    try:
        # 执行SQL语句
        if len(args) > 1:
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql, args)
        # 提交到数据库执行
        connection.commit()
    except Exception as exp:
        # 发生错误时回滚
        print(exp)
        connection.rollback()
    finally:
        # 关闭数据库连接
        connection.close()


# 批量插入坐标生成的json
def batch_insert_json(jsonlist, tab):
    total_count = len(jsonlist)
    limit = 10000
    for i in range(0, (total_count // limit) + 1):
        position = i * limit
        sublist = jsonlist[position:position + limit]
        sql = "INSERT INTO %s (`range`, `time`, `traffic`, `json`)" % tab
        sql += " VALUES (%s, %s, %s, %s)"
        execute(sql, sublist)


def get_coords(csvfile):
    coords = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for item in reader:
            _id = item[0]
            lon = item[1]
            lat = item[2]
            coords.append((lon, lat, _id))
    return coords


def handle_isochrones(time_interval=3, time_range=None, traffic_method="foot-walking", coords=None,
                      url="http://localhost:8081/ors/v2/isochrones/", json_path="./Default/pointID", tab=None):
    if coords is None:
        coords = []
    if time_range is None:
        time_range = [900, 1800, 3600]
    headers = {'Content-Type': "application/json"}
    features = []
    url += traffic_method
    json_list = []
    for coord in coords:
        _id = coord[2]
        params = {
            "locations": [[coord[0], coord[1]]],
            "range": time_range
        }
        response = requests.post(url, json=params, headers=headers)
        routes = response.json()
        if (not routes) or ('features' not in routes.keys()):
            logging.warning("\n请求坐标：%s,\n接口返回：%s" % (coord, routes))
            continue
        # 将geojson修改为esrijson
        for j in range(0, time_interval):
            feature_dict = {
                "attributes": {
                    "FID": 0,
                    "pointID": _id,
                    "OBJECTID": j,
                    "Time_Mins": time_range[j] / 60.0,
                    "Method": traffic_method,
                    "Lon": coord[0],
                    "Lat": coord[1]
                },
                "geometry": {
                    "rings": routes['features'][j]['geometry']['coordinates']
                }
            }
            features.append(feature_dict)
        dic = {
            "displayFieldName": "",
            "fieldAliases": {
                "FID": "FID",
                "pointID": "pointID",
                "OBJECTID": "OBJECTID",
                "time_Mins": "Time_Mins",
                "method": "Method",
                "Lon": "Lon",
                "Lat": "Lat"
            },
            "geometryType": "esriGeometryPolygon",
            "spatialReference": {
                "wkid": 4326,  # 代表WGS-1984
                "latestWkid": 4326
            },
            "fields": [
                {
                    "name": "FID",
                    "type": "esriFieldTypeOID",
                    "alias": "FID"
                },
                {
                    "name": "pointID",
                    "type": "esriFieldTypeInteger",
                    "alias": "pointID"
                },
                {
                    "name": "OBJECTID",
                    "type": "esriFieldTypeInteger",
                    "alias": "OBJECTID"
                },
                {
                    "name": "Time_Mins",
                    "type": "esriFieldTypeDouble",
                    "alias": "Time_Mins"
                },
                {
                    "name": "Method",
                    "type": "esriFieldTypeString",
                    "alias": "Method"
                },
                {
                    "name": "Lon",
                    "type": "esriFieldTypeDouble",
                    "alias": "Lon"
                },
                {
                    "name": "Lat",
                    "type": "esriFieldTypeDouble",
                    "alias": "Lat"
                }
            ],
            "features": features
        }
        features = []
        json_list.append([dis_range, time_range[0], traffic_method, json.dumps(dic, ensure_ascii=False)])
        print("生成" + json_path + str(_id) + '.json')
        # 1、生成json文件
        # 保存json
        # with io.open(json_path + str(_id) + '.json', 'w', encoding='utf-8') as json_file:
        #    json_file.write(np.unicode(json.dumps(dic, ensure_ascii=False, indent=2)))
    # 2、插入数据库
    batch_insert_json(json_list, tab)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        if not sys.argv[1]:
            print("Please input the related path of coordinate csv file!")
            exit(0)
        if not sys.argv[2]:
            print("Please input the related path of destination JSON directory!")
            exit(0)
    else:
        print("Please input the related path of coordinate csv file AND the related path of destination JSON directory")
        print(
            "Like：python dataCollecting_v3.py CityPointsCSV/Heidelberg_Points.csv Heidelberg_Points time_period traffic-method")
        exit(0)
    startTime = time.time()
    # 时间间隔
    timeinterval = 1
    # 时间步长
    timerange = [int(sys.argv[3])]
    # 交通方式
    trafficmethod = sys.argv[4]
    # 获取坐标
    # csv_file = './CityPointsCSV/Heidelberg_Points.csv'
    csv_file = sys.argv[1]
    if not os.path.exists(sys.argv[1]):
        print("Please the confirm coordinate csv file has exist")
        exit(0)
    coordset = get_coords(csv_file)
    # 自建openrouteservice服务地址
    requesturl = "http://192.168.37.122:8081/ors/v2/isochrones/"
    # 结果json路径
    # jsonpath = "./Heidelberg_Points"
    jsonpath = sys.argv[2] + "/pointID"
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    # 执行处理方法
    tab = "ors_indonesia_json"
    dis_range = "500m"
    handle_isochrones(timeinterval, timerange, trafficmethod, coordset, requesturl, jsonpath, tab)
    endTime = time.time()
    print("Has cost time：%s mins" % round(((endTime - startTime) / 60), 2))
