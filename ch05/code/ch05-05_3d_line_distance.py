#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

from shapely.geometry import LineString

x1 = 1
y1 = 2
z1 = 5
x2 = 2
y2 = 4
z2 = 8


def calc_3d_distance_2pts(x1, y1, z1, x2, y2, z2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return d


distance_3d = calc_3d_distance_2pts(x1, y1, z1, x2, y2, z2)
print distance_3d

# http://gis.stackexchange.com/questions/84512/get-the-vertices-on-a-linestring-either-side-of-a-point

def pairs(lst):
    for i in range(1, len(lst)):
        yield lst[i - 1], lst[i]

# import fiona
#
# with open('../geodata/bike_route.shp'):
line = LineString([(0, 0, 0), (1, 2, 0), (2, 2, 0), (2, 3, 0), (4, 2, 0), (5, 5, 0)])
list(line.coords)

start_distance = 0.0
new_dist = 0.0
for pair in pairs(list(line.coords)):
    print pair
    x1 = pair[0][0]
    x2 = pair[0][1]
    z1 = pair[0][2]
    y1 = pair[1][0]
    y2 = pair[1][1]
    z2 = pair[1][2]

    distance = calc_3d_distance_2pts(x1,y1,x2,y2,z1,z2)
    print distance
    new_dist = start_distance + distance
    new_dist = new_dist + distance
    #print new_dist

print new_dist

# num_vertex_in_line = len(line)
# distance = 0
# for vertex in line_geom:
#
#
# # on first pass value should be zero
#     # on second pass value should be zero + distance
#     dist_3d = calc_3d_distance_2pts(v1, v_next)
#
#     x = x + 1
#     # added each distance up
#
#     distance += dist_3d



# PostGIS 3D Distance and 2D Distance
query = """"
        SELECT ST_3DDistance(
                    ST_GeomFromEWKT('SRID=3857;POINT(1 2 5)'),
                    ST_GeomFromEWKT('SRID=3857;POINT(2 4 8)')
                ) As dist_3d,
                ST_Distance(
                    ST_GeomFromEWKT('SRID=3857;POINT(1 2)'),
                    ST_GeomFromEWKT('SRID=3857;POINT(2 4 8)')
                ) As dist_2d;
		"""