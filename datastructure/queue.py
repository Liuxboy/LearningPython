#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-1-18 <br>
# Time: 13:47 <br>
# Desc:

import queue

q = queue.Queue(2)
print(q.empty())
q.put('a')
q.put('b')
print(q.empty())
print(q.full())
print(q.get())
print(q.get())
print(q.empty())
print(q.qsize())






