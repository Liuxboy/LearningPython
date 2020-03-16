# -*- coding: utf-8 -*-
import csv
import json
import os
import sys
import time
import numpy as np
import pymysql
import requests

# 数据库配置
db_host = "192.168.37.101"
db_user = "root"
db_password = "root"
db_name = "ors"
limit = 1000


# 执行sql语句
def execute(sql, args=None):
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name,
                                 charset="utf8")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = connection.cursor()
    try:
        # 执行SQL语句
        if args and len(args) > 1:
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql, args)
        # 提交到数据库执行
        connection.commit()
        return cursor.fetchall()
    except Exception as exp:
        # 发生错误时回滚
        print(exp)
        connection.rollback()
    finally:
        # 关闭数据库连接
        cursor.close()
        connection.close()


# 批量插入生成的结果json
def batch_insert_json(jsonlist, tab):
    total_count = len(jsonlist)
    for j in range(0, (total_count // limit) + 1):
        position = j * limit
        sublist = jsonlist[position:position + limit]
        sql = "INSERT INTO %s (`coord_id`, `distance_range`, `time_period`, `traffic_way`, `result_json`)" % tab
        sql += " VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE result_json = VALUES(result_json)"
        if sublist:
            execute(sql, sublist)


# 创建json表
def create_tab(region):
    tab_name = "ors_%s_json" % region
    create_tab_sql = """
        CREATE TABLE %s (
          `coord_id` int(11) NOT NULL COMMENT '坐标ID',
          `distance_range` varchar(5) NOT NULL COMMENT '距离范围:500m,1km',
          `time_period` smallint(5) NOT NULL COMMENT '时间间隔(s):900,1800,3600',
          `traffic_way` varchar(20) NOT NULL DEFAULT '' COMMENT '交通方式:foot-walking,driving-car,driving-hgv,cycling-regular',
          `result_json` varchar(2000) DEFAULT NULL COMMENT '结果json',
          PRIMARY KEY (`coord_id`,`distance_range`,`time_period`,`traffic_way`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """ % tab_name
    exist_tab_sql = """
        SELECT t.table_name FROM information_schema.TABLES t 
        WHERE t.TABLE_SCHEMA ="ors" and t.TABLE_NAME ='%s';
    """ % tab_name
    if not execute(exist_tab_sql):
        execute(create_tab_sql)
    return tab_name


# 读取坐标文件
def get_coords(csvfile):
    coords = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for item in reader:
            lon = item[1]
            lat = item[2]
            coord_id = item[0]
            coords.append((lon, lat, coord_id))
    return coords


# 处理方法
def handle_isochrones(time_interval=3, time_range=None, traffic_method="foot-walking", coords=None,
                      url="http://localhost:8081/ors/v2/isochrones/", tab=None, dis_range='500m'):
    if coords is None:
        coords = []
    if time_range is None:
        time_range = [900, 1800, 3600]
    headers = {'Content-Type': "application/json"}
    features = []
    url += traffic_method
    json_list = []
    for coord in coords:
        coord_id = coord[2]
        params = {
            "locations": [[coord[0], coord[1]]],
            "range": time_range
        }
        response = requests.post(url, json=params, headers=headers)
        routes = response.json()
        if (not routes) or ('features' not in routes.keys()):
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--Request coord_id：%s,Response：%s" % (
                coord[2], routes))
            continue
        # 将geojson修改为esrijson
        for j in range(0, time_interval):
            feature_dict = {
                "attributes": {
                    "FID": 0,
                    "pointID": coord_id,
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
        json_list.append([coord_id, dis_range, time_range[0], traffic_method, json.dumps(dic, ensure_ascii=False)])
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--处理坐标id:%s, 距离范围:%s, 时间范围:%s, 交通方式:%s" % (
            coord_id, dis_range, time_range[0], traffic_method))
        # 1、保存json
        # with os.io.open(json_path + str(coord_id) + '.json', 'w', encoding='utf-8') as json_file:
        #     json_file.write(np.unicode(json.dumps(dic, ensure_ascii=False, indent=2)))
        # features = []
    # 2、插入数据库
    batch_insert_json(json_list, tab)


if __name__ == "__main__":
    if len(sys.argv) >= 5:
        if not sys.argv[1]:
            print("Please input the related path of coordinate csv file!")
            exit(0)
    else:
        print(
            "Please input the related path of coordinate csv file, the port, the time period, the traffic way, and the start coord_id")
        print(
            "Like：sudo python dataCollecting_v4.py Indonesia_Clip_Points_WGS_500.csv port time_period traffic_way start_coord_id(default 0)")
        exit(0)
    startTime = time.time()
    # 1、第一个参数：坐标文件路径
    # csv_file = 'Indonesia_Clip_Points_WGS_500.csv'
    csv_file = sys.argv[1]
    if not os.path.exists(sys.argv[1]):
        print("Please the confirm coordinate csv file has exist")
        exit(0)
    coordset = get_coords(csv_file)
    (filepath, tempfilename) = os.path.split(csv_file)
    (shotname, extension) = os.path.splitext(tempfilename)
    # 1.1坐标文件第一个单词为数据表名
    tablename = create_tab(shotname.split('_')[0])  # Indonesia
    # 1.2坐标文件最后一个单词为距离范围
    disrange = str(shotname.split('_')[-1]) + "m"  # 500m
    # 2、第二个参数：端口
    port = sys.argv[2]
    # 3、第三个参数：时间步长
    timerange = [int(sys.argv[3])]
    # 4、第四个参数：交通方式
    trafficmethod = sys.argv[4]
    # 5、如果有第5个参数，则说明需要重断点接着跑，没有，则跑全部
    if len(sys.argv) == 6:
        start_id = int(sys.argv[5])
        coordset = coordset[start_id:]
    # 自建openrouteservice服务地址
    requesturl = "http://192.168.37.122:%s/ors/v2/isochrones/" % port
    # 分批执行处理方法,1000个坐标插一次数据库
    total_count = len(coordset)
    for i in range(0, (total_count // limit) + 1):
        start_position = i * limit
        end_position = min(total_count, start_position + limit)
        sub_coord_list = coordset[start_position: end_position]
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--本批次处理坐标范围:[%s, %s)" % (start_position, end_position))
        handle_isochrones(1, timerange, trafficmethod, sub_coord_list, requesturl, tablename, disrange)

    endTime = time.time()
    print("Has cost time：%s mins" % round(((endTime - startTime) / 60), 2))
