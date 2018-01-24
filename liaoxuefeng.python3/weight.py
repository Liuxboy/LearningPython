#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Package: ${PACKAGE_NAME} <br>
# Author: liuchundong <br>
# Date: 2017/2/20 <br>
# Time: 16:59 <br>
# Desc:

weight = input('请输入你的体重：')
height = input('请输入你的身高：')
w = int(weight)
h = float(height)
BMI = float(w / (h * h))
if BMI > 32:
    print('您的BMI指数；', '%.1f' % BMI)
    print('严重肥胖')
elif BMI > 28:
    print('您的BMI指数；', '%.1f' % BMI)
    print('肥胖')
elif BMI > 25:
    print('您的BMI指数；', '%.1f' % BMI)
    print('过重')
elif BMI > 18.5:
    print('您的BMI指数；', '%.1f' % BMI)
    print('正常')
else:
    print('您的BMI指数；', '%.1f' % BMI)
    print('过轻')
