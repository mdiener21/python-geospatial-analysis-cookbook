#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# for every polygon in a polygon layer there can only be
# one point object located in each polygon
# the number of points per polygon can be defined by the user

from shapely.geometry import Point, MultiPolygon, MultiPoint
from shapely.geometry import Polygon

# construct a valid polygon (i.e. not self-intersecting) with a hole
ply_exterior = [(0, 0), (0, 10), (10, 10), (0, 10)]
ply_interior = [(2, 2), (2, 4), (4, 4), (4, 2)]
test_ply = Polygon(ply_exterior, [ply_interior])
ply1 = Polygon([(15, 15), (15, 20), (20, 20), (20, 15)])

polygon_box = Polygon([(0, 0), (0, 10), (10, 10), (0, 10)])

point_on_edge = Point(5, 10)
point_on_vertex = Point(10, 10)
point_inside = Point(6, 6)
point_outside = Point(20, 20)
point_in_hole = Point(3, 3)

pt_series = MultiPoint([(1, 1), (2, 2), (4, 4), (5, 5), (16, 16)])

print len(pt_series)
# if len(poly) > 1:
ply_series = MultiPolygon([polygon_box, ply1])
pts_in_polys = []
pts_in_polys_dic = {}
# check each polygon for number of points inside
for i, poly in enumerate(ply_series):

    pts_in_this_ply = []

    for pt in pt_series:
        if poly.contains(pt):
            pts_in_this_ply.append(pt)

    pts_in_polys.append(len(pts_in_this_ply))

    pts_in_polys_dic['id ' + str(i)] = len(pts_in_this_ply)

for res in pts_in_polys:
    if res == 1:
        print " YEAA  One point in Poly"

    elif res == 0:
        print " no points in poly"
    elif res > 1:
        print " oh no more than one point in polygon"
    else:
        print "done"


print len(ply_series)

print pts_in_polys
print "points in this poly"
print pts_in_this_ply
print pts_in_polys_dic
# polygons['num_points'] = len(something)


def valid_point_in_poly(poly, point):
    """
    Determine if every polygon contains max one point and that each
    point is not located on the EDGE or Vertex of the polygon
    :param point: Point data set
    :param poly: Polygon data set
    :return: True or False if False a dictionary containing polygon ids
    that contain no or multiple points
    """
    id = None
    total_pts = None

    good_result = {'result': 'all polygon have only one point inside'}
    bad_result = {'result': 'some polygons have more than one point inside', 'list_bad_polys': []}
    list_bad_polys = [{'poly_id': id, 'num_pts': total_pts},{'poly_id': id, 'num_pts': total_pts}]
    bad_result['list_bad_polys'] = list_bad_polys
    print bad_result
    # test if point is on the edge, vertex or inside
    # if yes all good else point is in hole or our outside or
    # point is on a vertex or on the edge
    if poly.touches(point):
        return False
    if poly.contains(point):
        return True
    return False

    # test a multipolygon with holes

# print test_ply.contains(point_inside)
# print test_ply.boundary
# print test_ply.bounds

print str(valid_point_in_poly(polygon_box, point_on_vertex)) + " BAD point on VERTEX"
print str(valid_point_in_poly(polygon_box, point_on_edge)) + " BAD point on EDGE"
print str(valid_point_in_poly(polygon_box, point_inside)) + " Good point on INSIDE"

print str(valid_point_in_poly(polygon_box, point_outside)) + " BAD point OUTSIDE polygon"
print str(valid_point_in_poly(point_in_hole, test_ply)) + " BAD point IN HOLE polygon"
