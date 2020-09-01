#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-6-8 <br>
# Time: 10:59 <br>
# Desc:
from flask import Flask, request

app = Flask(__name__)


@app.route("/hello", methods=['GET', 'POST'])
def get_post():
    if request.method == 'POST':
        request.data
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
