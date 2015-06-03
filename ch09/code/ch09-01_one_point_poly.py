#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# for every polygon in a polygon layer there can only be
# one point object located in each polygon
# the number of points per polygon can be defined by the user
import shapefile
from utils import shp_to_shply_multiply
from utils import shp_2_geojson_file
from utils import shp2_geojson_obj
from utils import create_shply_multigeom

from shapely.geometry import Point, MultiPolygon, MultiPoint
from shapely.geometry import Polygon

in_shp_poly = "../geodata/topo_polys.shp"
in_shp_point = "../geodata/topo_points.shp"

shp1_data = shp2_geojson_obj(in_shp_poly)
shp2_data = shp2_geojson_obj(in_shp_point)

shp1_polys = create_shply_multigeom(shp1_data, "MultiPolygon")
shp2_points = create_shply_multigeom(shp2_data, "MultiPoint")


shp_2_geojson_file('../geodata/topo_polys.shp', '../geodata/topo_ply.geojson')

shply_poly = shp_to_shply_multiply('../geodata/topo_polys.shp')

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

    pts_in_polys2 = []
    pts_touch_plys2 = []

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

        pts_in_polys2.append(pts_in_this_ply)
        pts_touch_plys2.append(pts_touch_this_ply)



    print pts_in_polys2[0]
    print "break....................."

    print pts_touch_plys2
    print "next####################"

    no_good = dict()
    all_good = True
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
        return no_good # [4,0,1]


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


print valid_point_in_poly(shp1_polys, shp2_points)
print "----------done test on MULTI -------------"

