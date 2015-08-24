#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import os
from shapely.geometry import shape, Point
import json

def pairs(lst):
    """
    yield iterator of two coordinates of linestring
    :param lst: list object
    :return: yield iterator of two coordinates
    """
    for i in range(1, len(lst)):
        yield lst[i - 1], lst[i]


def calc_3d_distance_2pts(x1, y1, z1, x2, y2, z2):
    """
    :input two point coordinates (x1,y1,z1),(x2,y2,2)
    :param x1: x coordinate first segment
    :param y1: y coordiante first segment
    :param z1: z height value first coordinate
    :param x2: x coordinate second segment
    :param y2: y coordinate second segment
    :param z2: z height value seconc coordinate
    :return: 3D distance between two input 3D coordinates
    """
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return d


def readin_json(jsonfile):
    """
    input: geojson or json file
    """
    with open(jsonfile) as json_data:
        d = json.load(json_data)
        return d


geoj_27563_file = os.path.realpath("../geodata/velowire_stage_16_27563_utf8.geojson")
print (geoj_27563_file)
# create python dict type from geojson file object
json_load = readin_json(geoj_27563_file)

# set start lengths
length_3d = 0.0
length_2d = 0.0

# go through each geometry in our linestring
for f in json_load['features']:
    # create shapely shape from geojson
    s = shape(f['geometry'])

    # calculate 2D total length
    length_2d = s.length

    # set start elevation
    elevation_gain = 0

    # go through each coordinate pair
    for vert_start, vert_end in pairs(s.coords):
        line_start = Point(vert_start)
        line_end = Point(vert_end)

        # create input coordinates
        x1 = line_start.coords[0][0]
        y1 = line_start.coords[0][1]
        z1 = line_start.coords[0][2]
        x2 = line_end.coords[0][0]
        y2 = line_end.coords[0][1]
        z2 = line_end.coords[0][2]

        # calculate 3d distance
        distance = calc_3d_distance_2pts(x1, y1, z1, x2, y2, z2)

        # sum distances from vertex to vertex
        length_3d += distance

        # calculate total elevation gain
        if z1 > z2:
            elevation_gain = ((z1 - z2) + elevation_gain )
            z2 = z1
        else:
            elevation_gain = elevation_gain  # no height change
            z2 = z1


print ("total elevation gain is: {gain} meters".format(gain=str(elevation_gain)))

# print coord_pair
distance_3d = str(length_3d / 1000)
distance_2d = str(length_2d / 1000)
dist_diff = str(length_3d - length_2d)

print ("3D line distance is: {dist3d} meters".format(dist3d=distance_3d))
print ("2D line distance is: {dist2d} meters".format(dist2d=distance_2d))
print ("3D-2D length difference: {diff} meters".format(diff=dist_diff))
