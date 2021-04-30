#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2018/1/24 <br>
# Time: 17:31 <br>
# Desc:
import logging
import random
import sqlite3
import time
import datetime

import requests

sqlite_db = "port.sqlite3"


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _execute_many(sql, args=()):
    conn = sqlite3.connect(sqlite_db)
    conn.text_factory = str
    conn.row_factory = _dict_factory
    cur = conn.cursor()
    try:
        cur.executemany(sql, args)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def _execute(sql, args=()):
    conn = sqlite3.connect(sqlite_db)
    conn.text_factory = str
    conn.row_factory = _dict_factory
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
        conn.commit()
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_port(port_type):
    sql = "SELECT ID, PORT_ID, PORT FROM %s WHERE PORT_ID IS NOT NULL" % port_type
    return _execute(sql)


def handle_recent_vessels(port_type):
    headers = {
        "Accept-Encoding": "gzip, deflate, en",
        "Cookie": "__cfduid=da92a27d729da26b44d4baade8ab2df4e1583138869; SERVERID=app5",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Cache-Control": "no-cache",
        "Host": "www.marinetraffic.com"
    }
    vessels_url = "https://www.marinetraffic.com/en/ais/getchart/portsCharts/%s/recent_vessels"
    ports = get_port(port_type)
    if ports:
        for item in ports:
            _id = item['ID']
            port_id = item['PORT_ID']
            if not port_id:
                continue
            port = item['PORT']
            print("handle the recent vessels id: {}, port id: {}, port name: {}".format(_id, port_id, port))
            _url = vessels_url % port_id
            time.sleep(random.random() * 3)  # 随机sleep 0-3 秒
            response = requests.get(_url, headers=headers)
            result = response.text
            insert_sql = "INSERT INTO port_recent_vessels (PORT_ID, PORT_NAME, VESSELS) VALUES (?, ?, ?)"
            _execute(insert_sql, (port_id, port, result))


def handle_arrivals_departures(port_type, start_date, end_date):
    ports = get_port(port_type)
    if ports:
        for item in ports:
            _id = item['ID']
            port_id = item['PORT_ID']
            port = item['PORT']
            if not port_id:
                continue
            port = item['PORT']
            time.sleep(random.random() * 3)  # 随机sleep 0-3 秒
            handle_port_arrivals_departures(_id, port_id, port, start_date, end_date)


def handle_port_arrivals_departures(_id, port_id, port, start_date, end_date):
    url = "https://www.marinetraffic.com/en/reports/?asset_type=arrivals_departures&columns=shipname,move_type,port_type,port_name,ata_atd,origin_port_name,leg_start_port,intransit,mmsi,imo,origin_port_atd,ship_type,dwt,fleet&port_in={}&ata_atd_between={},{}"
    headers = {
        "Accept-Encoding": "gzip, deflate, en",
        "Cookie": "__cfduid=da92a27d729da26b44d4baade8ab2df4e1583138869; SERVERID=app5",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Cache-Control": "no-cache",
        "Host": "www.marinetraffic.com"
    }
    arrivals_departures_url = url.format(port_id, start_date, end_date)
    response = requests.get(arrivals_departures_url, headers=headers)
    result_json = response.json()
    if result_json:
        total_count = result_json['totalCount']
        print("handle the arrivals departures {} - {}, id: {}, port id: {}, port name: {}".format(start_date, end_date,
                                                                                                  _id, port_id, port))
        data = result_json['data']
        if data:
            insert_list = []
            for item in data:
                SHIP_ID = item['SHIP_ID']
                SHIP_NAME = item['SHIPNAME']
                PORT_ID = item['PORT_ID']
                PORT_NAME = item['PORT_NAME']
                CENTERX = item['CENTERX']
                CENTERY = item['CENTERY']
                COUNTRY_CODE = item['CENTERY']
                IMO = item['IMO']
                TIMESTAMP_UTC = item['TIMESTAMP_UTC']
                PORT_TYPE_NAME = item['PORT_TYPE_NAME']
                FROM_NOANCH_ID = item['FROM_NOANCH_ID']
                FROM_NOANCH_NAME = item['FROM_NOANCH_NAME']
                FROM_PORT_ID = item['FROM_PORT_ID']
                FROM_PORT_NAME = item['FROM_PORT_NAME']
                FROM_NOANCH_TIMESTAMP = item['FROM_NOANCH_TIMESTAMP']
                TYPE_SUMMARY = item['TYPE_SUMMARY']
                TYPE_COLOR = item['TYPE_COLOR']
                DWT = item['DWT']
                TIMEZONE = item['TIMEZONE']
                MOVE_TYPE_NAME = item['MOVE_TYPE_NAME']
                MMSI = item['MMSI']
                INTRANSIT_NAME = item['INTRANSIT_NAME']
                COLLECTION_NAME = item['COLLECTION_NAME']
                row = (SHIP_ID, SHIP_NAME, PORT_ID, PORT_NAME, CENTERX, CENTERY, COUNTRY_CODE, IMO, TIMESTAMP_UTC,
                       PORT_TYPE_NAME,
                       FROM_NOANCH_NAME, FROM_NOANCH_ID, FROM_PORT_ID, FROM_PORT_NAME, FROM_NOANCH_TIMESTAMP,
                       TYPE_SUMMARY,
                       TYPE_COLOR, DWT, TIMEZONE, MOVE_TYPE_NAME, MMSI, INTRANSIT_NAME, COLLECTION_NAME)
                insert_list.append(row)

            insert_sql = """
                INSERT INTO port_arrivals_departures(SHIP_ID, SHIP_NAME, PORT_ID, PORT_NAME, CENTERX, CENTERY, COUNTRY_CODE, IMO, 
                    TIMESTAMP_UTC, PORT_TYPE_NAME, FROM_NOANCH_NAME, FROM_NOANCH_ID, FROM_PORT_ID, FROM_PORT_NAME, 
                    FROM_NOANCH_TIMESTAMP, TYPE_SUMMARY, TYPE_COLOR, DWT, TIMEZONE, MOVE_TYPE_NAME, MMSI, INTRANSIT_NAME, 
                    COLLECTION_NAME) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            _execute_many(insert_sql, insert_list)


def main():
    # 两类数据：国内、国外
    port_types = ['port_china', 'port_world']
    occur_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    for port_type in port_types:
        print("handle the port type: %s" % port_type)
        handle_recent_vessels(port_type)
        handle_arrivals_departures(port_type, occur_date, occur_date)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logging.error("some errors has occurred! %s", ex, exc_info=True)
    finally:
        exit(0)
