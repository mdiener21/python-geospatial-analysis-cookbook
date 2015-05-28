#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# for every polygon in a polygon layer there can only be
# one point object located in each polygon
# the number of points per polygon can be defined by the user

from shapely.geometry import Point, MultiPolygon, MultiPoint
from shapely.geometry import Polygon

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

    # check each polygon for number of points inside
    for i, poly in enumerate(polys):

        pts_in_this_ply = []
        pts_touch_this_ply = []

        if points.geom_type == 'Point':
            if poly.touches(points):
                pts_touch_this_ply.append({'single_point_error_touches': points.__geo_interface__})
            if poly.contains(points):
                pts_in_this_ply.append({'single_point_error_contains': points.__geo_interface__})

        else:
            for pt in points:
                if poly.touches(pt):
                    pts_touch_this_ply.append({'multipoint_errors_touches': pt.__geo_interface__, 'poly_id': i, 'point_coord': pt.__geo_interface__})

                if poly.contains(pt):
                    pts_in_this_ply.append({'multipoin_error_contains': pt.__geo_interface__})

        pts_in_polys.append(len(pts_in_this_ply)) #  print count of point errors
        pts_touch_plys.append(len(pts_touch_this_ply)) # print count of point errors

        # pts_in_polys.append(pts_in_this_ply)
        # pts_touch_plys.append(pts_touch_this_ply)

    man = dict()
    all_good = True
    for num, res in enumerate(pts_in_polys):

        if res == 1:
            man['poly num ' + str(num)] = "excellen only 1 point in poly"
        elif res > 1:
            man['poly num ' + str(num)] = str(res) + " points in this poly"
            all_good = False
        else:
            man['poly num ' + str(num)] = "No points in this poly"
            all_good = False

    if all_good:
        return all_good
    else:
        return man # [4,0,1]


#
# print valid_point_in_poly(ply_series, point_on_vertex)
# print valid_point_in_poly(ply_series, point_on_edge)
# print valid_point_in_poly(ply_series, point_inside)
# print valid_point_in_poly(ply_series, point_outside)
# print valid_point_in_poly(ply_series, point_in_hole)

print valid_point_in_poly(ply_series, pt_series_bad)
# man = dict()
# for num, res in enumerate(multi_test):
#     if res == 1:
#         continue  # man['poly num ' + str(num)] = "excellen only 1 point in poly"
#     elif res > 1:
#         man['poly num ' + str(num)] = str(res) + " points in this poly"
#     else:
#         man['poly num ' + str(num)] = "No points in this poly"
# print man
