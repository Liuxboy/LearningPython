#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:

from pyecharts.charts import Bar
from pyecharts.render import make_snapshot, snapshot


def build_bar():
    bar = Bar()
    bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    bar.render("pycharts_bar.html")


def build_bar_by_chain():
    bar = (
        Bar()
        .ChartItem
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    )
    bar.render("pycharts_bar_by_chain.html")


def build_bar_to_pic():
    bar = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    )
    make_snapshot(snapshot, bar.render(), "pycharts_bar_to_pic.png")


if __name__ == '__main__':
    build_bar()
    build_bar_by_chain()
    build_bar_to_pic()
