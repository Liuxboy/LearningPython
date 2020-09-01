#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-6-8 <br>
# Time: 10:59 <br>
# Desc:

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username


@app.route('/post/<int:post_id>/')
def show_post_id(post_id):
    return 'Post post_id = %d' % post_id


@app.route('/post/<float:post_price>/')
def show_post_price(post_price):
    return 'Post post_price = %f' % post_price


@app.route('/post/<path:post_path>/')
def show_post_path(post_path):
    return 'Post post_path = %s' % post_path


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
