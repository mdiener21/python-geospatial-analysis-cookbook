#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.ops import snap
from matplotlib import pyplot
from shapely.geometry import LineString, Point
from utils import SIZE, BLUE, RED, GREEN, GRAY
from utils import plot_coords_line
from utils import plot_line

# import fiona
#
# # open our shapefile
# with fiona.open('../geodata/someshape.shp', mode='r') as source_shp:

line = LineString([(0.5, 0.5), (2.0, 1.5), (3.0, 0.5)])
h = line.coords
print h
reverse_line = 'hello world'[::-1]
print reverse_line
point = Point(3, 1.8)
pt_snap_res = snap(point, line, 4)
#
shplySnapPoint = line.interpolate(1.4)
print shplySnapPoint