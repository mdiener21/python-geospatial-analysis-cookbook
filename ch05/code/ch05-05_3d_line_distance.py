#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from shapely.geometry import shape, Point
import json



def pairs(lst):
    for i in range(1, len(lst)):
        yield lst[i - 1], lst[i]


def calc_3d_distance_2pts(x1, y1, x2, y2, z1, z2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return d


def readin_json(jsonfile):
    with open(jsonfile) as json_data:
        d = json.load(json_data)
        return d


geoj_4326_file = "../geodata/velowire_stage_16_4326.geojson"
geoj_27563_file = "../geodata/velowire_stage_16_27563.geojson"

json_load = readin_json(geoj_27563_file)


distance_values = []
length_3d = 0.0
length_2d = None
for f in json_load['features']:
    s = shape(f['geometry'])
    geo = f['geometry']
    # print geo
    length_2d = s.length
    print s.coords[1]
    print s.coords[2]

    for vert_start, vert_end in pairs(s.coords):
        line_start = Point(vert_start)
        line_end = Point(vert_end)

        x1 = line_start.coords[0][0]
        x2 = line_end.coords[0][0]
        y1 = line_start.coords[0][1]
        y2 = line_end.coords[0][1]
        z1 = line_start.coords[0][2]
        z2 = line_end.coords[0][2]

        distance = calc_3d_distance_2pts(x1, y1, x2, y2, z1, z2)
        length_3d += distance


# print coord_pair
print "3D line distance is: " + str(length_3d / 1000)
print "2D line distance is: " + str(length_2d / 1000)
print "difference 2D and 3D is: " + str(length_3d - length_2d) + " meters"

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
query_gen_profile = """
WITH points3d AS
    (SELECT (ST_DumpPoints(geom)).geom AS geom,
            ST_StartPoint(geom) AS origin
     FROM geodata.velowire_stage_16_3d
     WHERE id = id)
SELECT ST_distance(origin, geom) AS x, ST_Z(geom) AS y,
St_3ddistance(origin,geom)-st_distance(origin,geom) as diff_dist
--st_length(geom)
FROM points3d;

"""