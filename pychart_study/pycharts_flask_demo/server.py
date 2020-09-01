#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:

from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
import pyecharts.globals
from pyecharts import options as opts
from pyecharts.charts import Bar

app = Flask(__name__, static_folder="templates")

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
pyecharts.globals.CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))
pyecharts.globals._WarningControl.ShowWarning = False


def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


@app.route("/")
def index():
    c = bar_base()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9000)
