#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import fiona
from shapely.geometry import shape

filename = '../geodata/bike-route-austria.shp'

def pairs(lst):
    for i in range(1, len(lst)):
        yield lst[i - 1], lst[i]


def calc_3d_distance_2pts(x1, y1, x2, y2, z1, z2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return d


from shapely.geometry import LineString
line_3d_distance = 0.0

with fiona.open(filename, 'r') as layer1:
    for feat1 in layer1:
        fid = int(feat1['id'])
        geom1 = shape(feat1['geometry'])
        print geom1.coords[1]
        for pair in pairs(list(geom1.coords)):
            x1 = pair[0][0]
            x2 = pair[0][1]
            z1 = pair[0][2]
            y1 = pair[1][0]
            y2 = pair[1][1]
            z2 = pair[1][2]

            distance = calc_3d_distance_2pts(x1,y1,x2,y2,z1,z2)
            #print distance
            line_3d_distance += distance
print line_3d_distance
        # index.insert(fid, geom1.bounds)
    # with fiona.open(intSHP, 'w', 'ESRI Shapefile', schema) as layer3:
    #     layer3.write({ 'properties': props,
    #                     'geometry': mapping(geom1.intersection(geom2))
    #                  })


#distance_3d = calc_3d_distance_2pts(x1, y1, z1, x2, y2, z2)
#print distance_3d

# http://gis.stackexchange.com/questions/84512/get-the-vertices-on-a-linestring-either-side-of-a-point


# import fiona
#
# with open('../geodata/bike_route.shp'):
# line = LineString([(0, 0, 0), (1, 2, 0), (2, 2, 0), (2, 3, 0), (4, 2, 0), (5, 5, 0)])
line = LineString([(1,2,5),(2,4,8)])
#list(line.coords)

#print line.length

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
    #print distance
    new_dist += distance
    #new_dist = new_dist + distance
    #print new_dist

print new_dist

print calc_3d_distance_2pts(1,2,2,4,5,8)
print line.length

def getSum(l):
    sum = 0
    skip = False
    for i in l:
         if i == 13:
             skip = True
             continue
         if skip:
             skip = False
             continue
         sum += i
    return sum

foo = [1, 13, 13, 2, 3]
#print "foo"
#print getSum(foo)
#print "x"

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