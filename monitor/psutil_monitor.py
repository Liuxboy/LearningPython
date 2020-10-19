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
import psutil
import time
from multiprocessing.dummy import Pool as TheadPool

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
    top_mem = None
    if mem.percent > 90.0:
        top_mem = get_top_process('memory_percent')
    return mem.total, mem.available, top_mem


def handle_swap():
    swap = psutil.swap_memory()
    return swap.total, swap.free


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


"""
CREATE TABLE monitor(
    create_time TIMESTAMP NOT NULL DEFAULT (strftime('%s','now')) PRIMARY KEY,
    cpu_pect DECIMAL(5,2),
    mem_used INT,
    mem_free INT,
    swap_used INT,
    swap_free INT,
    net_recv INT,
    net_sent INT,
    load_1m DECIMAL(5,2),
    load_5m DECIMAL(5,2),
    load_15m DECIMAL(5,2),
    disk_read_count INT,
    disk_writ_count INT,
    disk_read_byte INT,
    disk_writ_byte INT,
    top_cpu TEXT,
    top_mem TEXT,
    top_disk TEXT
);
"""


def insert_sqlite(data_list):
    """
    往sqlite里面插入统计信息
    :param data_list:
    :return:
    """
    if data_list:
        insert_sql = """
                INSERT INTO monitor(
                    create_time,
                    cpu_pect,
                    mem_used, mem_free,
                    swap_used, swap_free,
                    net_recv, net_sent,
                    load_1m, load_5m, load_15m,
                    disk_read_count, disk_writ_count, disk_read_byte, disk_writ_byte,
                    top_cpu, top_mem, top_disk
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """
        if data_list:
            conn = sqlite3.connect(sqlite_db)
            conn.text_factory = str
            cur = conn.cursor()
            cur.executemany(insert_sql, data_list)
            conn.commit()
            conn.close()


def schedule():
    pool = TheadPool(processes=3)
    interval_func_list = [handle_cpu, handle_mem, handle_swap]
    for i in range(60):
        result = []
        for func in interval_func_list:
           res = pool.apply_async(func, ())
        result.append(res.get())
        print(result)
    pool.close()
    pool.join()


def main():
    timestamp = time.time()
    hhmm = time.strftime("%H:%M", time.localtime(timestamp))
    cpu_pect = 0.0
    mem_used = 0
    mem_free = 0
    swap_used = 0
    swap_free = 0
    net_recv = 0
    net_sent = 0
    load_1m = 0.0
    load_5m = 0.0
    load_15m = 0.0
    disk_read_count = 0
    disk_writ_count = 0
    disk_read_byte = 0
    disk_writ_byte = 0
    top_cpu = []
    top_mem = []
    top_disk = None

    # 开始时
    disk_io = handle_disk_io()
    disk_read_count = disk_io[0]
    disk_writ_count = disk_io[1]
    disk_read_byte = disk_io[2]
    disk_writ_byte = disk_io[3]
    net_io = handle_net_io()
    net_recv = net_io[0]
    net_sent = net_io[1]
    # 中间间隔1s统计一次系统cpu、mem、swap
    loop_list = range(60)
    for i in loop_list:
        cpu = handle_cpu()
        cpu_pect += cpu[0]
        cpu[1] and top_cpu.append(cpu[1])

        mem = handle_mem()
        mem_used += (mem[0] - mem[1])
        mem_free += mem[1]
        mem[2] and top_mem.append(mem[2])

        swap = handle_swap()
        swap_used += (swap[0] - swap[1])
        swap_free += swap[1]
        time.sleep(1)
    # 结束时
    disk_io = handle_disk_io()
    disk_read_count = disk_io[0] - disk_read_count
    disk_writ_count = disk_io[1] - disk_writ_count
    disk_read_byte = disk_io[2] - disk_read_byte
    disk_writ_byte = disk_io[3] - disk_writ_byte
    net_io = handle_net_io()
    net_recv = net_io[0] - net_recv
    net_sent = net_io[1] - net_sent
    # cpu负载亦从最后一次记录里面获取
    load = handle_load()
    load_1m = load[0]
    load_5m = load[1]
    load_15m = load[2]
    # 每日9点检查一下磁盘空间
    if hhmm == '09:00':
        top_disk = handle_disk_usage()

    data_list = [(int(timestamp), round(cpu_pect/60.0, 2), mem_used//60, mem_free//60, swap_used//60, swap_free//60, net_recv,
                  net_sent, round(load_1m, 2), round(load_5m, 2), round(load_15m, 2), disk_read_count, disk_writ_count, disk_read_byte, 
                  disk_writ_byte, _list2jsonstr(top_cpu), _list2jsonstr(top_mem), top_disk)]
    insert_sqlite(data_list)


def _list2jsonstr(lt):
    if type(lt) == 'list' and lt:
        return json.dumps(lt)
    return None


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(end_time - start_time)
