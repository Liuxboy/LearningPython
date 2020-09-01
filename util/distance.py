#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc:


import numpy as np
import scipy.spatial.distance as dist

vec1 = np.array(["600030", "600032", "600033"])

vec2 = np.array(["600030", "600032"])

d = dist.pdist(np.array([vec1, vec2]), "jaccard")
print(d)
