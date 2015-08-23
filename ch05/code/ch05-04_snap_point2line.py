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
    out_pt = dict(type='Feature', properties=dict(id=1))
    out_pt['geometry'] = geojs_geom
    new_coord = (x, y)
    # add newly transformed coordinate
    out_pt['geometry']['coordinates'] = new_coord

    return out_pt


def transform_geom(orig_geojs, in_crs, out_crs):
    """
    transform a GeoJSON linestring or Point to
      a new coordinate system
    :param orig_geojs: input GeoJSON
    :param in_crs: original input crs
    :param out_crs: destination crs
    :return: a new GeoJSON
    """

    wgs84_coords = []
    # transfrom each coordinate
    if orig_geojs['geometry']['type'] == "LineString":
        for x, y in orig_geojs['geometry']['coordinates']:
            x1, y1 = transform(in_crs, out_crs, x, y)
            orig_geojs['geometry']['coordinates'] = x1, y1
            wgs84_coords.append([x1, y1])
        # create new GeoJSON
        new_wgs_geojs = dict(type='Feature', properties={})
        new_wgs_geojs['geometry'] = dict(type='LineString')
        new_wgs_geojs['geometry']['coordinates'] = wgs84_coords

        return new_wgs_geojs

    elif orig_geojs['geometry']['type'] == "Point":

        x = orig_geojs['geometry']['coordinates'][0]
        y = orig_geojs['geometry']['coordinates'][1]
        x1, y1 = transform(in_crs, out_crs, x, y)
        orig_geojs['geometry']['coordinates'] = x1, y1
        coord = x1, y1
        wgs84_coords.append(coord)

        new_wgs_geojs = dict(type='Feature', properties={})
        new_wgs_geojs['geometry'] = dict(type='Point')
        new_wgs_geojs['geometry']['coordinates'] = wgs84_coords

        return new_wgs_geojs
    else:
        print("sorry this geometry type is not supported")

# define output GeoJSON file
output_result = os.path.realpath("../geodata/ch05-04-geojson.js")

line = {"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[-49.21875,19.145168196205297],[-38.49609375,32.24997445586331],[-27.0703125,22.105998799750576]]}}
point = {"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-33.57421875,32.54681317351514]}}

new_line = transform_geom(line, wgs84, pseudo_mercator)
new_point = transform_geom(point, wgs84, pseudo_mercator)


shply_line = asShape(new_line['geometry'])
shply_point = asShape(new_point['geometry'])

# perform interpolation and project point to line
pt_interpolate = shply_line.interpolate(shply_line.project(shply_point))

# print coordinates and distance to console
print ("origin point coordinate")
print (point)

print ("interpolted point location")
print (pt_interpolate)

print "distance from origin to interploate point"
print (shply_point.distance(pt_interpolate))

# convert new point to wgs84 GeoJSON
snapped_pt = transform_point(pt_interpolate, pseudo_mercator, wgs84)

# our original line and point are transformed
# so here they are again in original coords
# to plot on our map
line_orig = {"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[-49.21875,19.145168196205297],[-38.49609375,32.24997445586331],[-27.0703125,22.105998799750576]]}}
point_orig = {"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-33.57421875,32.54681317351514]}}

# write to disk the results
with open(output_result, 'w') as js_file:
    js_file.write('var input_pt = {0}'.format(json.dumps(snapped_pt)))
    js_file.write('\n')
    js_file.write('var orig_pt = {0}'.format(json.dumps(point_orig)))
    js_file.write('\n')
    js_file.write('var line = {0}'.format(json.dumps(line_orig)))
