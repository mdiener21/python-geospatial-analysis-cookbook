#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

x1 = 1
y1 = 2
z1 = 5
x2 = 2
y2 = 4
z2 = 8

def calc_3d_distance_2pts(x1,y1,z1, x2,y2, z2):
    d = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    return d

distance_3d = calc_3d_distance_2pts(x1,y1,z1, x2,y2, z2)
print distance_3d