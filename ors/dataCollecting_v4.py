# -*- coding: utf-8 -*-
import csv
import io
import json
import logging
import os
import sys
import time

import numpy as np
import requests


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


def handle_isochrones(time_interval=3, time_range=None, traffic_method="foot-walking", coords=None,
                      url="http://localhost:8080/ors/v2/isochrones/", json_path="./Default/pointID"):
    if coords is None:
        coords = []
    if time_range is None:
        time_range = [900, 1800, 3600]
    headers = {'Content-Type': "application/json"}
    features = []
    url += traffic_method
    for coord in coords:
        coord_id = coord[2]
        params = {
            "locations": [[coord[0], coord[1]]],
            "range": time_range
        }
        response = requests.post(url, json=params, headers=headers)
        routes = response.json()
        if (not routes) or ('features' not in routes.keys()):
            print("\n请求坐标：%s,\n接口返回：%s" % (coord, routes))
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
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--处理坐标id:%s, 时间范围:%s, 交通方式:%s" % (
            coord_id, time_range[0], traffic_method))
        # 保存json
        with io.open(json_path + str(coord_id) + '.json', 'w', encoding='utf-8') as json_file:
            json_file.write(np.unicode(json.dumps(dic, ensure_ascii=False, indent=2)))
        features = []


if __name__ == "__main__":
    if len(sys.argv) >= 5:
        if not sys.argv[1]:
            print("Please input the related path of coordinate csv file!")
            exit(0)
        if not sys.argv[2]:
            print("Please input the related path of destination JSON directory!")
            exit(0)
    else:
        print("Please input the related path of coordinate csv file AND the related path of destination JSON directory")
        print(
            "Like：python dataCollecting_v3.py CityPointsCSV/Heidelberg_Points.csv Heidelberg_Points time_period traffic-method start_position(default 0)")
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
    requesturl = "http://localhost:8081/ors/v2/isochrones/"
    # 结果json路径
    # jsonpath = "./Heidelberg_Points"
    jsonpath = sys.argv[2] + "/pointID"
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    # 5、如果有第5个参数，则说明需要重断点接着跑，没有，则跑全部
    start_id = 0
    if len(sys.argv) == 6:
        start_id = int(sys.argv[5])
        coordset = coordset[start_id:]
    # 分批执行处理方法,1000个坐标插一次数据库
    total_count = len(coordset)
    limit = 1000
    for i in range(0, (total_count // limit) + 1):
        start_position = i * limit
        end_position = min(total_count, start_position + limit)
        sub_coord_list = coordset[start_position: end_position]
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--第%s次处理坐标范围:[%s, %s)" % (i, start_id + start_position, start_id + end_position))
        handle_isochrones(timeinterval, timerange, trafficmethod, coordset, requesturl, jsonpath)

    endTime = time.time()
    print("Has cost time：%s mins" % round((endTime - startTime) / 60, 2))
