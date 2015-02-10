#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.geometry import LineString, Point

line = LineString([(0.5, 0.5), (2.0, 1.5), (3.0, 0.5)])

line_original = list(line.coords)
print line_original

line_reversed = list(line.coords)[::-1]
print line_reversed

point_on_line = line.interpolate(1.4)
print point_on_line