#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.geometry import asShape
import json
import os
from pyproj import Proj, transform

# define the pyproj CRS
# our output CRS
wgs84 = Proj("+init=EPSG:4326")
# output CRS
pseudo_mercator = Proj("+init=EPSG:3857")


def transform_point(in_point, in_crs, out_crs):
    """
    export a Shapely geom to GeoJSON Feature and
    transform to a new coordinate system with pyproj
    :param in_point: shapely geometry as point
    :param in_crs: pyproj crs definition
    :param out_crs:  pyproj output crs definition
    :return: GeoJSON transformed to out_crs
    """
    geojs_geom = in_point.__geo_interface__

    x1 = geojs_geom['coordinates'][0]
    y1 = geojs_geom['coordinates'][1]

    # transform the coordinate
    x, y = transform(in_crs, out_crs, x1, y1)

    # creat output new point
    new_point = dict(type='Feature', properties=dict(id=1))
    new_point['geometry'] = geojs_geom
    new_coord = (x, y)
    # add newly transformed coordinate
    new_point['geometry']['coordinates'] = new_coord

    return new_point


def transform_linestring(orig_geojs, in_crs, out_crs):
    """
    transform a GeoJSON linestring to
      a new coordinate system
    :param orig_geojs: input GeoJSON
    :param in_crs: original input crs
    :param out_crs: destination crs
    :return: a new GeoJSON
    """
    line_wgs84 = orig_geojs
    wgs84_coords = []
    # transfrom each coordinate
    for x, y in orig_geojs['geometry']['coordinates']:
        x1, y1 = transform(in_crs, out_crs, x, y)
        line_wgs84['geometry']['coordinates'] = x1, y1
        wgs84_coords.append([x1, y1])

    # create new GeoJSON
    new_wgs_geojs = dict(type='Feature', properties={})
    new_wgs_geojs['geometry'] = dict(type='LineString')
    new_wgs_geojs['geometry']['coordinates'] = wgs84_coords

    return new_wgs_geojs


# define output GeoJSON file
output_result = os.path.realpath("../geodata/ch05-03-geojson.js")

line_geojs = {"type": "Feature", "properties": {}, "geometry": {"type": "LineString", "coordinates": [[-13643703.800790818,5694252.85913249],[-13717083.34794459,6325316.964654908]]}}

# create shapely geometry from FeatureCollection
shply_line = asShape(line_geojs['geometry'])

# get the coordinates of each vertex in our line
line_original = list(shply_line.coords)
print line_original

# showing how to reverse a linestring
line_reversed = list(shply_line.coords)[::-1]
print line_reversed

# example of the same reversing function on a string for example
hello = 'hello world'
reverse_hello = hello[::-1]
print reverse_hello

# locating the point on a line based on distance from line start
# input in meters = to 360 Km from line start
point_on_line = shply_line.interpolate(360000)

# transform input linestring and new point
# to wgs84 for visualization on web map
wgs_line = transform_linestring(line_geojs, pseudo_mercator, wgs84)
wgs_point = transform_point(point_on_line, pseudo_mercator, wgs84)

# write to disk the results
with open(output_result, 'w') as js_file:
    js_file.write('var point_on_line = {0}'.format(json.dumps(wgs_point)))
    js_file.write('\n')
    js_file.write('var in_linestring = {0}'.format(json.dumps(wgs_line)))
