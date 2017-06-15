#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/5/17 <br>
# Time: 14:50 <br>
# Desc: 

names = ['Michael', 'Tom', 'Jim']
scores = [60, 70, 80]

d = {'Michael': '95', 'Bob': 75, 'Tracy': 85}
print(d['Michael'])
d['Michael'] = 100
print(d)
# d['Tom'] #KeyError: 'Tom'
print(d)
if 'Tom' in d:
    print(d.get('Tom'))
else:
    print(d.get('Tracy'))

print(d.get('Tom', 100))


