#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-09-08 <br>
# Time: 10:17 <br>
# Desc: 统计本机性能,基于psutil(https://psutil.readthedocs.io/en/latest/)
# 并同时支持python2和python3
import json
import sqlite3
import time
from threading import Timer

import psutil

# 查询逻辑cpu数量
logical_cpu = psutil.cpu_count()
sqlite_db = '/home/monitor.db'


def handle_cpu():
    cpu_percent = psutil.cpu_percent()
    top_cpu = None
    if cpu_percent > 10.0:
        top_cpu = get_top_process('cpu_percent')
    return cpu_percent, top_cpu


def handle_mem():
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    top_mem = None
    if mem_percent > 90.0:
        top_mem = get_top_process('memory_percent')
    return mem_percent, top_mem


def handle_swap():
    swap = psutil.swap_memory()
    swap_percent = swap.percent
    return swap_percent


def handle_load():
    load = psutil.getloadavg()
    _1m_avg = load[0]
    _5m_avg = load[1]
    _15m_avg = load[2]
    top_cpu = None
    if _1m_avg > logical_cpu:
        top_cpu = get_top_process('cpu_percent')
    return _1m_avg, _5m_avg, _15m_avg, top_cpu


def handle_disk_io():
    disk_counter = psutil.disk_io_counters()
    read_count = disk_counter.read_count
    write_count = disk_counter.write_count
    read_bytes = disk_counter.read_bytes
    write_bytes = disk_counter.write_bytes
    return read_count, write_count, read_bytes, write_bytes


def handle_net_io():
    net_counter = psutil.net_io_counters()
    recv_bytes = net_counter.bytes_recv
    send_bytes = net_counter.bytes_sent
    return recv_bytes, send_bytes


def handle_disk_usage():
    disk_usage_list = []
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        device = partition[1]
        partition_disk_usage = psutil.disk_usage(device)
        total = partition_disk_usage.total
        used = partition_disk_usage.used
        disk_usage_list.append({
            "device": device,
            "total": total,
            "used": used,
        })
    return json.dumps(disk_usage_list, ensure_ascii=False)


def get_top_process(top_percent):
    process_list = [(p.pid, p.info['username'], p.info['cpu_percent'], p.info['memory_percent'],
                     p.info['memory_info'].vms, p.info['memory_info'].rss, p.info['status'],
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.info['create_time'])), p.info['exe'])
                    for p in
                    sorted(psutil.process_iter(['username', 'cpu_percent', 'memory_percent', 'memory_info', 'status',
                                                'create_time', 'exe']),
                           key=lambda p: p.info[top_percent],
                           reverse=True)][0:5]
    process_json_list = []
    for item in process_list:
        process_json_list.append({
            "PID": item[0],
            "USER": item[1],
            "%CPU": item[2],
            "%MEM": item[3],
            "VSZ": item[4],
            "RSS": item[5],
            "STAT": item[6],
            "START": item[7],
            "COMMAND": item[8]
        })
    return json.dumps(process_json_list, ensure_ascii=False)


def insert_sqlite(data_list):
    """
    往sqlite里面插入统计信息
    :param data_list:
    :return:
    """
    if data_list:
        insert_sql = """
                INSERT INTO psutil_monitor(
                    create_time, cpu_pect, mem_pect, swp_pect,
                    load_1m, load_5m, load_15m,
                    net_recv, net_sent,
                    disk_read_count, disk_writ_count, disk_read_byte, disk_writ_byte,
                    top_cpu, top_mem, top_disk
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """
        if data_list:
            conn = sqlite3.connect(sqlite_db)
            conn.text_factory = str
            cur = conn.cursor()
            cur.executemany(insert_sql, data_list)
            conn.commit()
            conn.close()


def __list2jsonstr(lt):
    if type(lt) == 'list' and lt:
        return json.dumps(lt)
    return None


def main():
    # 每个5秒执行一次，非阻塞
    t = Timer(5, main)
    t.start()
    timestamp = time.time()
    print(int(timestamp))
    cpu = handle_cpu()
    cpu_pect = cpu[0]
    top_cpu = cpu[1]

    mem = handle_mem()
    mem_pect = mem[0]
    top_mem = mem[1]

    swp_pect = handle_swap()

    load = handle_load()
    load_1m = load[0]
    load_5m = load[1]
    load_15m = load[2]

    disk_io = handle_disk_io()
    disk_read_count = disk_io[0]
    disk_writ_count = disk_io[1]
    disk_read_byte = disk_io[2]
    disk_writ_byte = disk_io[3]

    net_io = handle_net_io()
    net_recv = net_io[0]
    net_sent = net_io[1]
    # 每日9点检查一下磁盘空间
    top_disk = None
    hhmm = time.strftime("%H:%M", time.localtime(timestamp))
    if hhmm == '09:00':
        top_disk = handle_disk_usage()

    data_list = [(int(timestamp), round(cpu_pect, 2), round(mem_pect, 2), round(swp_pect, 2),
                  round(load_1m, 2), round(load_5m, 2), round(load_15m, 2),
                  net_recv, net_sent,
                  disk_read_count, disk_writ_count, disk_read_byte, disk_writ_byte, __list2jsonstr(top_cpu),
                  __list2jsonstr(top_mem), top_disk)]
    insert_sqlite(data_list)


if __name__ == "__main__":
    main()
