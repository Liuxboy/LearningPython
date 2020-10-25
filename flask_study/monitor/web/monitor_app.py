#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc: 展示各机器收集的性能指标

import os
import signal

from flask import Flask, render_template, jsonify, request

from pyecharts.charts import Line, Gauge
import pyecharts.options as opts
import time
import psutil
import sqlite3

app = Flask(__name__, static_folder="templates")
sqlite_db = '/home/monitor.db'

net_io_dict = {'net_io_time': [], 'net_io_sent': [],
               'net_io_recv': [], 'pre_sent': 0, 'pre_recv': 0, 'len': -1}
disk_dict = {'disk_time': [], 'write_bytes': [], 'read_bytes': [],
             'pre_write_bytes': 0, 'pre_read_bytes': 0, 'len': -1}


def query_sqlite(sql, args=None):
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    try:
        cursor.execute(sql, args)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def cpu(start_time=None, end_time=None):
    if not start_time:
        start_time = 0
    if not end_time:
        end_time = int(time.time())

    sql = """
            SELECT tmp.ctime, round(SUM(tmp.cpu_pect) / COUNT(1), 2)
            FROM (
                SELECT strftime('%H:%M', create_time, 'unixepoch', 'localtime') AS ctime, cpu_pect
                FROM psutil_monitor
                WHERE create_time >= ? AND create_time <= ?
            ) AS tmp
            GROUP BY tmp.ctime;
        """
    result = query_sqlite(sql, (start_time, end_time))
    cpu_percent_dict = {}
    if result:
        for row in result:
            create_time = row[0]
            cpu_percent = row[1]
            cpu_percent_dict[create_time] = cpu_percent
    return cpu_percent_dict


def cpu_line() -> Line:
    now = time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    cpu_percent_dict = cpu()
    cpu_percent_line = (
        Line()
            .add_xaxis(list(cpu_percent_dict.keys()))
            .add_yaxis('', list(cpu_percent_dict.values()),
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True
                       )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title=now + "CPU使用率", pos_left="center"),
            yaxis_opts=opts.AxisOpts(min_=0, max_=100, split_number=10, type_="value", name='%')
        )
    )
    return cpu_percent_line


def memory(start_time=None, end_time=None):
    if not start_time:
        start_time = 0
    if not end_time:
        end_time = int(time.time())

    sql = """
            SELECT tmp.ctime, ROUND(SUM(tmp.mem_pect) / COUNT(1), 2), ROUND(SUM(tmp.swp_pect) / COUNT(1), 2)
            FROM (
                SELECT strftime('%H:%M', create_time, 'unixepoch', 'localtime') AS ctime, mem_pect, swp_pect
                FROM psutil_monitor
                WHERE create_time >= ? AND create_time <= ?
            ) AS tmp
            GROUP BY tmp.ctime;
        """
    result = query_sqlite(sql, (start_time, end_time))
    mem_percent_dict = {}
    swp_percent_dict = {}
    if result:
        for row in result:
            create_time = row[0]
            mem_pect = row[1]
            swp_pect = row[2]
            mem_percent_dict[create_time] = mem_pect
            swp_percent_dict[create_time] = swp_pect
    return mem_percent_dict, swp_percent_dict


def memory_line() -> Line:
    now = time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    mem = memory()
    mem_percent_dict = mem[0]
    swp_percent_dict = mem[1]
    memory_percent_line = (
        Line()
            .add_xaxis(list(mem_percent_dict.keys()))
            .add_yaxis('内存占用率', list(mem_percent_dict.values()),
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True
                       )
            .add_yaxis('交换区暂用率', list(swp_percent_dict.values()),
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True
                       )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title=now + "内存使用率", pos_left="center"),
            yaxis_opts=opts.AxisOpts(min_=0, max_=100, split_number=10, type_="value", name='%'),
            legend_opts=opts.LegendOpts(pos_left="left")
        )
    )
    return 0, 0, 0, 0, 0, 0, memory_percent_line


def load(start_time=None, end_time=None):
    if not start_time:
        start_time = 0
    if not end_time:
        end_time = int(time.time())

    sql = """
            SELECT tmp.ctime, 
                ROUND(SUM(tmp.load_1m) / COUNT(1), 2), 
                ROUND(SUM(tmp.load_5m) / COUNT(1), 2), 
                ROUND(SUM(tmp.load_15m) / COUNT(1), 2)
            FROM (
                SELECT strftime('%H:%M', create_time, 'unixepoch', 'localtime') AS ctime, load_1m, load_5m, load_15m
                FROM psutil_monitor
                WHERE create_time >= ? AND create_time <= ?
            ) AS tmp
            GROUP BY tmp.ctime;
        """

    result = query_sqlite(sql, (start_time, end_time))
    load_1m_dict = {}
    load_5m_dict = {}
    load_15m_dict = {}
    if result:
        for row in result:
            create_time = row[0]
            load_1m = row[1]
            load_5m = row[2]
            load_15m = row[3]
            load_1m_dict[create_time] = load_1m
            load_5m_dict[create_time] = load_5m
            load_15m_dict[create_time] = load_15m
    return load_1m_dict, load_5m_dict, load_15m_dict


def load_line() -> Line:
    now = time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    lod = load()
    load_1m_dict = lod[0]
    load_5m_dict = lod[1]
    load_15m_dict = lod[2]
    load_line = (
        Line()
            .add_xaxis(list(load_1m_dict.keys()))
            .add_yaxis('最近1分钟负载', list(load_1m_dict.values()),
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True
                       )
            .add_yaxis('最近5分钟负载', list(load_5m_dict.values()),
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True
                       )
            .add_yaxis('最近15分钟负载', list(load_15m_dict.values()),
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                       label_opts=opts.LabelOpts(is_show=False),
                       is_smooth=True
                       )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title=now + "负载", pos_left="center"),
            yaxis_opts=opts.AxisOpts(min_=0.0, max_=5.0, split_number=10, type_="value", name=''),
            legend_opts=opts.LegendOpts(pos_left="left")
        )
    )
    return load_line


def disk_io(start_time=None, end_time=None):
    if not start_time:
        start_time = 0
    if not end_time:
        end_time = int(time.time())

    sql = """
            SELECT tmp.ctime, 
                ROUND(SUM(tmp.disk_read_count) / COUNT(1), 2), 
                ROUND(SUM(tmp.disk_writ_count) / COUNT(1), 2), 
                ROUND(SUM(tmp.disk_read_byte) / COUNT(1), 2),
                ROUND(SUM(tmp.disk_writ_byte) / COUNT(1), 2)
            FROM (
                SELECT strftime('%H:%M', create_time, 'unixepoch', 'localtime') AS ctime, 
                    disk_read_count, disk_writ_count, disk_read_byte, disk_writ_byte
                FROM psutil_monitor
                WHERE create_time >= ? AND create_time <= ?
            ) AS tmp
            GROUP BY tmp.ctime;
        """
    result = query_sqlite(sql, (start_time, end_time))
    disk_read_count_dict = {}
    disk_writ_count_dict = {}
    disk_read_byte_dict = {}
    disk_writ_byte_dict = {}
    if result:
        for i in range(len(result)):
            if i == 0:
                row = result[0]
                create_time = row[0]
                disk_read_count_dict[create_time] = 0
                disk_writ_count_dict[create_time] = 0
                disk_read_byte_dict[create_time] = 0
                disk_writ_byte_dict[create_time] = 0
            else:
                pre_row = result[i - 1]
                pre_disk_read_count = pre_row[1]
                pre_disk_writ_count = pre_row[2]
                pre_disk_read_byte = pre_row[3]
                pre_disk_writ_byte = pre_row[4]

                row = result[i]
                create_time = row[0]
                disk_read_count = row[1]
                disk_writ_count = row[2]
                disk_read_byte = row[3]
                disk_writ_byte = row[4]

                disk_read_count_dict[create_time] = disk_read_count - pre_disk_read_count
                disk_writ_count_dict[create_time] = disk_writ_count - pre_disk_writ_count
                disk_read_byte_dict[create_time] = disk_read_byte - pre_disk_read_byte
                disk_writ_byte_dict[create_time] = disk_writ_byte - pre_disk_writ_byte
    return disk_read_count_dict, disk_writ_count_dict, disk_read_byte_dict, disk_writ_byte_dict


def disk_io_line() -> Line:
    disk_read_count_dict, disk_writ_count_dict, disk_read_byte_dict, disk_writ_byte_dict = disk_io()
    c = (
        Line(init_opts=opts.InitOpts(width="1680px", height="1000px"))
            .add_xaxis(list(disk_read_count_dict.keys()))
            .add_yaxis(
            series_name="读取次数",
            yaxis_index=0,
            y_axis=list(disk_read_count_dict.values()),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='RED'),
            linestyle_opts=opts.LineStyleOpts(color='RED'),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
            .add_yaxis(
            series_name="写入次数",
            y_axis=list(disk_writ_count_dict.values()),
            yaxis_index=0,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='BLUE'),
            linestyle_opts=opts.LineStyleOpts(color='BLUE'),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
            .add_yaxis(
            series_name="读取字节数",
            yaxis_index=1,
            y_axis=list(disk_read_byte_dict.values()),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='GREEN'),
            linestyle_opts=opts.LineStyleOpts(color='GREEN'),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
            .add_yaxis(
            series_name="写入字节数",
            y_axis=list(disk_writ_byte_dict.values()),
            yaxis_index=1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='#FF00FF'),
            linestyle_opts=opts.LineStyleOpts(color='#FF00FF'),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name_location="start",
                type_="value",
                is_inverse=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name='KB/分'
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="磁盘IO",
                pos_left="center",
                pos_top="top",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(type_="value", name='次/分'),
        )
            .set_series_opts(
            axisline_opts=opts.AxisLineOpts(),
        )
    )
    return 200, 121, 78, c


def net_io(start_time=None, end_time=None):
    if not start_time:
        start_time = 0
    if not end_time:
        end_time = int(time.time())
    sql = """
            SELECT tmp.ctime, 
                ROUND(SUM(tmp.net_sent) / COUNT(1), 2),
                ROUND(SUM(tmp.net_recv) / COUNT(1), 2)
            FROM (
                SELECT strftime('%H:%M', create_time, 'unixepoch', 'localtime') AS ctime, net_sent, net_recv
                FROM psutil_monitor
                WHERE create_time >= ? AND create_time <= ?
            ) AS tmp
            GROUP BY tmp.ctime;
        """
    result = query_sqlite(sql, (start_time, end_time))
    net_sent_byte_dict = {}
    net_recv_byte_dict = {}
    if result:
        for i in range(len(result)):
            if i == 0:
                row = result[0]
                create_time = row[0]
                net_sent_byte_dict[create_time] = 0
                net_recv_byte_dict[create_time] = 0
            else:
                pre_row = result[i - 1]
                pre_net_sent_byte = pre_row[1]
                pre_net_recv_byte = pre_row[2]

                row = result[i]
                create_time = row[0]
                net_sent_byte = row[1]
                net_recv_byte = row[2]

                net_sent_byte_dict[create_time] = (net_sent_byte - pre_net_sent_byte) // 1024
                net_recv_byte_dict[create_time] = (net_recv_byte - pre_net_recv_byte) // 1024
    return net_sent_byte_dict, net_recv_byte_dict


def net_io_line() -> Line:
    net_sent_byte_dict, net_recv_byte_dict = net_io()
    c = (
        Line()
            .add_xaxis(list(net_sent_byte_dict.keys()))
            .add_yaxis(
            series_name="发送字节数",
            y_axis=list(net_sent_byte_dict.values()),
            yaxis_index=0,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='BLUE'),
            linestyle_opts=opts.LineStyleOpts(color='BLUE'),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
            .add_yaxis(
            series_name="接受字节数",
            y_axis=list(net_recv_byte_dict.values()),
            yaxis_index=1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='RED'),
            linestyle_opts=opts.LineStyleOpts(color='RED'),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name_location="start",
                type_="value",
                is_inverse=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name='KB/分'
            )
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title="网卡IO", pos_left="center"),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
            yaxis_opts=opts.AxisOpts(type_="value", name='KB/分'),
            legend_opts=opts.LegendOpts(pos_left="left")
        )
            .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    return c


def process():
    result = []
    process_list = []
    pid = psutil.pids()
    for k, i in enumerate(pid):
        try:
            proc = psutil.Process(i)
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc.create_time()))
            process_list.append((str(i), proc.name(), proc.cpu_percent(), proc.memory_percent(), ctime, proc.status()))
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
        except SystemError:
            pass
        process_list.sort(key=process_sort, reverse=True)
    for i in process_list:
        result.append({'PID': i[0], 'name': i[1], 'cpu': i[2], 'mem': "%.2f%%" % i[3], 'ctime': i[4], 'status': i[5].upper()})
    return jsonify({'list': result[0:10]})


def process_sort(elem):
    return elem[3]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cpu")
def get_cpu_chart():
    cpu = cpu_line()
    return jsonify({'cpu_percent_line': cpu.dump_options_with_quotes()})


@app.route("/load")
def get_load_chart():
    load = load_line()
    return jsonify({'load_line': load.dump_options_with_quotes()})


@app.route("/memory")
def get_memory_chart():
    mtotal, mused, mfree, stotal, sused, sfree, mem = memory_line()
    return jsonify({'mtotal': mtotal, 'mused': mused, 'mfree': mfree, 'stotal': stotal, 'sused': sused, 'sfree': sfree,
                    'mem_percent_line': mem.dump_options_with_quotes()})


@app.route("/disk")
def get_disk_chart():
    total, used, free, c = disk_io_line()
    return jsonify({'total': total, 'used': used, 'free': free, 'line': c.dump_options_with_quotes()})


@app.route("/netio")
def get_net_io_chart():
    c = net_io_line()
    return c.dump_options_with_quotes()


@app.route("/process")
def get_process_tab():
    c = process()
    return c

#
# @app.route("/delprocess")
# def del_process():
#     pid = request.args.get("pid")
#     os.kill(int(pid), signal.SIGKILL)
#     return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = True
