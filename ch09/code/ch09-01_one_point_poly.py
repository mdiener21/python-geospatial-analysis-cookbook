#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# for every polygon in a polygon layer there can only be
# one point object located in each polygon
# the number of points per polygon can be defined by the user
from utils import shp_to_shply_multiply
from utils import shp_2_geojson_file
from utils import shp2_geojson_obj
from utils import create_shply_multigeom

from shapely.geometry import Point, MultiPolygon, MultiPoint
from shapely.geometry import Polygon
import json

in_shp_poly = "../geodata/topo_polys.shp"
in_shp_point = "../geodata/topo_points.shp"

ply_geojs_obj = shp2_geojson_obj(in_shp_poly)
pt_geojs_obj = shp2_geojson_obj(in_shp_point)

shply_polys = create_shply_multigeom(ply_geojs_obj, "MultiPolygon")
shply_points = create_shply_multigeom(pt_geojs_obj, "MultiPoint")

ply1 = Polygon([(0, 0), (0, 10), (10, 10), (0, 10)])
ply2 = Polygon([(30,30),(30,40), (40, 40), (40, 30)])
ply3 = Polygon([(15, 15), (15, 20), (20, 20), (20, 15)])

point_on_edge = Point(5, 10)
point_on_vertex = Point(10, 10)
point_inside = Point(6, 6)
point_outside = Point(20, 20)
point_in_hole = Point(3, 3)

pt_series_bad = MultiPoint([(0, 0), (1, 1), (2, 2), (4, 4), (5, 5), (16, 16)])
pt_series_good = MultiPoint([(5, 5), (35, 35), (16, 16)])
ply_series = MultiPolygon([ply1, ply2, ply3])


def valid_point_in_poly(polys, points):
    """
    Determine if every polygon contains max one point and that each
    point is not located on the EDGE or Vertex of the polygon
    :param point: Point data set
    :param poly: Polygon data set
    :return: True or False if False a dictionary containing polygon ids
    that contain no or multiple points
    """
    pts_in_polys = []
    pts_touch_plys = []

    pts_plys_geom = []
    pts_touch_geom = []

    # check each polygon for number of points inside
    for i, poly in enumerate(polys):

        pts_in_this_ply = []
        pts_touch_this_ply = []

        # deal with a single point object
        if points.geom_type == 'Point':
            if poly.touches(points):
                pts_touch_this_ply.append({'single_point_error_touches': points.__geo_interface__})

            if poly.contains(points):
                pts_in_this_ply.append({'single_point_inside': points.__geo_interface__})

        # handle multiple points
        else:
            for pt in points:
                if poly.touches(pt):
                    pts_touch_this_ply.append({'multipoint_errors_touches': pt.__geo_interface__, 'poly_id': i, 'point_coord': pt.__geo_interface__})

                if poly.contains(pt):
                    pts_in_this_ply.append({'multipoint_contains': pt.__geo_interface__})

        pts_in_polys.append(len(pts_in_this_ply)) #  print count of point errors
        pts_touch_plys.append(len(pts_touch_this_ply)) # print count of point errors

        # create list of point geometry errors
        pts_plys_geom.append(pts_in_this_ply)
        pts_touch_geom.append(pts_touch_this_ply)

    # identify if we have more than one point per polygon or
    # identify if no points are inside a polygon
    no_good = dict()
    all_good = True

    # loop over list containing the number of pts per polygon
    # each item in list is an integer representing the number
    # of points located inside a particular polygon [4,1,0]
    # represents 4 points in polygon 1, 1 point in poly 2, and
    # 0 points in polygon 3
    for num, res in enumerate(pts_in_polys):

        if res == 1:
            # this polygon is good and only has one point inside
            # no points on the edge or on the vertex of polygon
            continue
            # no_good['poly num ' + str(num)] = "excellen only 1 point in poly"
        elif res > 1:
            # we have more than one point either inside, on edge
            # or vertex of a polygon
            no_good['poly num ' + str(num)] = str(res) + " points in this poly"
            all_good = False
        else:
            # last case no points in this polygon
            no_good['poly num ' + str(num)] = "No points in this poly"
            all_good = False

    if all_good:
        return all_good
    else:
        bad_list = []
        for pt in pts_plys_geom:
            fgeom = {}
            for res in pt:
                if 'multipoint_contains' in res:
                    hui = res['multipoint_contains']
                    print hui
                    fgeom['geom'] = hui
            bad_list.append(fgeom)
        return bad_list
        #return no_good,pts_in_polys2 # [4,0,1]


print valid_point_in_poly(ply_series, point_on_vertex)
print "----------done test on VERTEX -------------"

print valid_point_in_poly(ply_series, point_on_edge)
print "----------done test on EDGE -------------"

print valid_point_in_poly(ply_series, point_inside)
print "----------done test on INSIDE -------------"

print valid_point_in_poly(ply_series, point_outside)
print "----------done test on OUTSIDE -------------"

print valid_point_in_poly(ply_series, point_in_hole)
print "----------done test on HOLE -------------"


valid_res = valid_point_in_poly(shply_polys, shply_points)

final_list = []
for res in valid_res:
    if 'geom' in res:
        geom = res['geom']
        final_list.append(geom)

final_gj = {"type": "GeometryCollection","geometries":final_list}
print json.dumps(final_gj)


