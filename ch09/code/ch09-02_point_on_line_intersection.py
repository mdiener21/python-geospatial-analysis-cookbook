#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shapely.geometry import Point, MultiPoint
from shapely.geometry import MultiLineString, LineString

line = LineString([(0, 0), (1, 1), (2, 2), (3, 3)])
line_cross = LineString([(3, 0), (2, 1), (1, 2), (0, 3)])


point_on_edge = Point(0.5, 0.5)
point_on_vertex = Point(3, 3)
point_intersect = Point(1.5, 1.5)
point_inside = Point(2.5, 2.5)
point_outside = Point(10, 10)


pt_series = MultiPoint([(1, 1), (2, 2), (4, 4), (5, 5), (16, 16), (60, 60), (70, 70)])
line_series = MultiLineString([line, line_cross])

