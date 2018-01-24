#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/5/16 <br>
# Time: 18:33 <br>
# Desc:

r = range(10)
print(list(r))

r = range(1, 10)
print(list(r))

r = range(1, 10, 2)
print(list(r))

r = range(1, 10)
v = range(1, 10, 1)
print(r == v)

r = range(0)
v = range(2, 1, 3)
print(r == v)

r = range(0, 3, 2)
v = range(0, 4, 2)
print(r != v)
