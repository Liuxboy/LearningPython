#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:

from random import randrange

from flask import Flask, render_template, jsonify

from pyecharts import options as opts
from pyecharts.charts import Bar, Line

app = Flask(__name__, static_folder="static", template_folder="templates")


def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
            .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


def line_base() -> Line:
    line = (
        Line()
            .add_xaxis(["{}".format(i) for i in range(10)])
            .add_yaxis(
            series_name="",
            y_axis=[randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line


@app.route("/")
def index():
    return render_template("app.html")


@app.route("/interval_fresh_all")
def interval_fresh_all():
    return render_template("interval_fresh_all.html")


@app.route("/interval_fresh_inc")
def interval_fresh_inc():
    return render_template("interval_fresh_inc.html")


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


idx = 9


@app.route("/lineDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": randrange(50, 80)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
