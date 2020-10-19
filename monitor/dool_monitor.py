#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-09-08 <br>
# Time: 10:17 <br>
# Desc: 统计本机性能, Base on dstat(https://github.com/dstat-real/dstat),该命令集合了vmstat、iostat、netstat、nfsstat和ifstat这些命令的工具，
# 是一个全能系统信息统计工具。但由于RedHat挟持了DSTAT这个名字，所以项目停更，由Dool(https://github.com/scottchiefbaker/dool)接替，
# 并同时支持python2和python3

import subprocess
import sqlite3
import re as regx
import paramiko

get_processor = subprocess.Popen("cat /proc/cpuinfo| grep 'processor'| wc -l", shell=True, stdout=subprocess.PIPE)
out = get_processor.stdout.readline()
processors = out.strip() or 1
ips = ['localhost']
sqlite_db = '/home/project/monitor/sys_monitor.db'


def convert_byte(number):
    """
    转换字节数
    :param number:
    :return:
    """
    num = number[0:-1]
    unit = number[-1:]
    byte_dic = {'B': 1,
                'k': 1 << 10,
                'M': 1 << 20,
                'G': 1 << 30,
                'T': 1 << 40,
                'P': 1 << 50,
                'E': 1 << 60
                }
    return float(num) * byte_dic[unit]


def handle_stat_line(line):
    """
    处理具体统计的单行数据，header已经去掉
      epoch   |usr sys idl wai stl| used  free  buff  cach| used  free| recv  send| 1m   5m  15m | read  writ| used  free: used  free
    1599561923|  0   0 100   0   0| 254M  834M 2108k  697M|   0  2048M|   0     0 |   0 0.01 0.05|  30k   26k|11.7G 5460M: 192M  822M
    1599561924|  0   0 100   0   0| 254M  834M 2108k  697M|   0  2048M|9776b   30k|   0 0.01 0.05|   0     0 |11.7G 5460M: 192M  822M
    1599561925|  0   0 100   0   0| 254M  834M 2108k  697M|   0  2048M|2656b 6992b|   0 0.01 0.05|   0     0 |11.7G 5460M: 192M  822M
    1599561926|  0   0 100   0   0| 254M  834M 2108k  697M|   0  2048M| 480b 6032b|   0 0.01 0.05|   0     0 |11.7G 5460M: 192M  822M
    1599561927|  0   0 100   0   0| 254M  834M 2108k  697M|   0  2048M|8928b 9392b|   0 0.01 0.05|   0     0 |11.7G 5460M: 192M  822M
    :param line:
    :return:
    """
    item = list(filter(None, regx.split(r'\s+|\|', line)))  # 过滤掉|和空格，并转换成list
    epoch = item[0]
    # cpu usage
    usr = item[1]
    sys = item[2]
    idl = item[3]
    # wai = item[4]
    # stl = item[5]
    top_cpu = cal_cpu(idl)
    # mem usage
    m_used = item[6]
    m_free = item[7]
    m_buff = item[8]
    m_cach = item[9]
    top_mem = cal_mem(m_used, m_free, m_buff, m_cach)
    # swap usage
    s_used = item[10]
    s_free = item[11]
    # net i/o
    recv = item[12]
    send = item[13]
    # load
    _1m = item[14]
    _5m = item[15]
    _15m = item[16]
    top_load = cal_load(_1m)
    # disk i/o
    read = item[17]
    writ = item[18]
    # disk freespace
    cal_disk_space(item[19:])
    new_row = (epoch,
               usr, sys, idl,
               m_used, m_free, m_buff, m_cach,
               s_used, s_free,
               recv, send,
               _1m, _5m, _15m,
               read, writ,
               top_cpu, top_mem, top_load
               )
    return new_row


def dool_stat_local():
    """
    处理本地机器的dool统计信息
    :return:
    """
    p = subprocess.Popen("/usr/bin/dool -Tcmsnld --freespace 1 5 | grep '|'", shell=True,
                         stdout=subprocess.PIPE, encoding="utf-8")
    i = 1
    stat_info_list = []
    for line in iter(p.stdout.readline, ''):
        if not line:
            break
        # 根据[dool -Tcmsnld --freespace 1 5 | grep '|'] 命令得出的结果去掉第一行不解析
        if i == 1:
            i += 1
            continue
        stat_info_list.append(handle_stat_line(line))
    insert_sqlite(stat_info_list)


def dool_stat_remote(_hostname, _username, _password):
    command = "/usr/bin/dool -Tcmsnld --freespace 1 5 | grep '|'"
    ssh_client = paramiko.SSHClient()
    try:
        # 允许连接不在know_hosts文件中的主机。
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=_hostname, username=_username, password=_password)
        stdin, stdout, stderr = ssh_client.exec_command(command=command)
        # 标准错误
        if stderr.readlines():
            print(stderr.readlines())  # 标准错误
        stat_info_list = []
        i = 1
        # 标准输出
        for line in iter(stdout.readline, ''):
            if not line:
                break
            # 根据[dool -Tcmsnld --freespace 1 5 | grep '|'] 命令得出的结果去掉第一行不解析
            if i == 1:
                i += 1
                continue
            stat_info_list.append(handle_stat_line(line))
        insert_sqlite(stat_info_list)
    except Exception as e:
        print('ssh %s@%s: %s' % (_username, _hostname, e))
        ssh_client.close()
    finally:
        ssh_client.close()


def cal_cpu(idl):
    """
    >dool -c
    --total-cpu-usage--
    usr sys idl wai stl
      0   0 100   0   0
      0   0  99   1   0
    :param idl:
    :return: usr, sys, wai, stl, top_cpu
    """
    usage_ratio = 100 - int(idl)
    top_cpu = None
    # cpu利用率超过10%，提取cup利用率top5，并报警:-)
    if usage_ratio > 10:
        cpu_usage_top_process = subprocess.Popen("ps aux | head -1; ps aux | sort -rnk 3 | head -n 5", shell=True,
                                                 stdout=subprocess.PIPE, encoding="utf-8")
        top_cpu = cpu_usage_top_process.stdout.read()
        trigger_warning(cpu_usage=usage_ratio)
    return top_cpu


def cal_mem(m_used, m_free, m_buff, m_cach):
    """
    计算根据dool 内存数据计算 free 命令对应的真实内存使用率
    >dool -m
    ------memory-usage-----
    used  free  buff  cach
    3899M 9760M  358M 1199M
    >free -m
                 total       used       free     shared    buffers     cached
    Mem:         15919       6147       9772          0        356       1194
    -/+ buffers/cache:       4595      11323
    Swap:         8031       1734       6297
    :param m_used:
    :param m_free:
    :param m_buff:
    :param m_cach:
    :return:
    """
    used = convert_byte(m_used)
    free = convert_byte(m_free)
    buff = convert_byte(m_buff)
    cach = convert_byte(m_cach)
    # (-buffers/cache) used内存数：第一部分Mem行中的 used – buffers – cached
    # 这是真实的内存消耗数据。
    real_used = float(used) - float(buff) - float(cach)
    # (+buffers/cache) free内存数: 第一部分Mem行中的 free + buffers + cached
    # 这是可挪用的内存数，是系统当前实际可用内存
    real_free = float(free) + float(buff) + float(cach)
    usage_ratio = real_used / (real_free + real_used)
    top_mem = None
    # 内存使用率超过90%，提取占用内存top5进程，并报警:-)
    if usage_ratio > 0.9:
        mem_usage_top_process = subprocess.Popen("ps aux | head -1; ps aux | sort -rnk 4 | head -n 5", shell=True,
                                                 stdout=subprocess.PIPE, encoding="utf-8")
        top_mem = mem_usage_top_process.stdout.read()
        trigger_warning(mem_usage=usage_ratio)
    return top_mem


def cal_load(_1m):
    """
    计算负载是否超标，一般情况，按一个核近一分钟平均负载不超过1.0为宜
    :param _1m:
    :return:
    """
    # 最近一分钟内负载超过逻辑处理器数，提取R、D、Z状态的进程，并报警:-)
    top_load = None
    if float(_1m) > int(processors):
        r_d_z_processes = subprocess.Popen("ps aux | grep -E 'R|D|Z' | grep -v 'S' | grep -v 'grep'", shell=True,
                                           stdout=subprocess.PIPE, encoding="utf-8")
        top_load = r_d_z_processes.stdout.read()
        trigger_warning(top_loads=top_load)
    return top_load


def cal_disk_space(disk_space_arr):
    """
    -----/---------/boot----
    | used  free used  free
    |11.7G 5461M 192M  822M
    |11.7G 5461M 192M  822M
    |11.7G 5461M 192M  822M
    |11.7G 5461M 192M  822M
    计算磁盘空间，有盘使用空间超过80%，报警
    :param disk_space_arr:
    :return:
    """
    i = 1
    for item in disk_space_arr:
        # 偶数项时，为某盘的free项，则前一项为该盘的used
        if i & 1 == 0:
            free = convert_byte(item)
            used = convert_byte(disk_space_arr[i - 1])
            i += 1
            usage_ratio = used / (used + free)
            if usage_ratio > 80.0:
                trigger_warning(disk_space=usage_ratio)


def trigger_warning(cpu_usage=None, mem_usage=None, top_loads=None, disk_space=None):
    # TODO
    pass


def insert_sqlite(data_list):
    """
    往sqlite里面插入统计信息
    :param data_list:
    :return:
    """
    if data_list:
        insert_sql = """
                INSERT INTO sys_stat(
                    stat_timestamp,
                    cpu_usr, cpu_sys, cpu_idl,
                    mem_used, mem_free, mem_buff, mem_cach,
                    swap_used, swap_free,
                    net_recv, net_send,
                    load_1m, load_5m, load_15m,
                    dsk_read, dsk_writ,
                    top_cpu, top_mem, top_load
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """
        if data_list:
            conn = sqlite3.connect(sqlite_db)
            conn.text_factory = str
            cur = conn.cursor()
            cur.executemany(insert_sql, data_list)
            conn.commit()
            conn.close()


def main():
    """
    本脚本只负责统计本机信息的cpu、mem、net、load以及对应的top进程。
    dool具体命令，请到对应机器上，执行dool -h
    :return:
    """
    for ip in ips:
        if ip == "localhost":
            dool_stat_local()
        else:
            dool_stat_remote(ip, 'root', 'liuxboy520')


if __name__ == "__main__":
    main()
