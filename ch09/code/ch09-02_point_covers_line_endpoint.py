#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import out_geoj
from shapely.geometry import Point, MultiPoint

in_shp_line = "../geodata/topo_line.shp"
in_shp_point = "../geodata/topo_points.shp"

# create our geojson like object from a Shapefile
shp1_data = shp2_geojson_obj(in_shp_line)
shp2_data = shp2_geojson_obj(in_shp_point)

# convert the geojson like object to shapely geometry
shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")
shp2_points = create_shply_multigeom(shp2_data, "MultiPoint")


def create_start_end_pts(lines):
    '''
    Generate a list of all start annd end nodes
    :param lines: a Shapely geometry LineString
    :return: Shapely multipoint object which includes
             all the start and end nodes
    '''
    list_end_nodes = []
    list_start_nodes = []

    for line in lines:
        coords = list(line.coords)

        line_start_point = Point(coords[0])
        line_end_point = Point(coords[-1])

        list_start_nodes.append(line_start_point)
        list_end_nodes.append(line_end_point)

    all_nodes = list_end_nodes + list_start_nodes

    return MultiPoint(all_nodes)


def check_points_cover_start_end(points, lines):
    '''

    :param points: Shapely point geometries
    :param lines:Shapely linestrings
    :return:
    '''

    all_start_end_nodes = create_start_end_pts(lines)

    bad_points = []
    good_points = []
    if len(points) > 1:
        for pt in points:
            if pt.touches(all_start_end_nodes):
                print "touches"
            if pt.disjoint(all_start_end_nodes):
                print "disjoint" # 2 nodes
                bad_points.append(pt)
            if pt.equals(all_start_end_nodes):
                print "equals"
            if pt.within(all_start_end_nodes):
                print "within" # all our nodes on start or end
            if pt.intersects(all_start_end_nodes):
                print "intersects"
                good_points.append(pt)
    else:
        if points.intersects(all_start_end_nodes):
            print "intersects"
            good_points.append(points)
        if points.disjoint(all_start_end_nodes):
            print "disjoint"
            good_points.append(points)


    if len(bad_points) > 1:
        print "oh no 1 or more points are NOT on a start or end node"
        out_geoj(bad_points, '../geodata/points_bad.geojson')
        out_geoj(good_points, '../geodata/points_good.geojson')

    elif len(bad_points) == 1:
        print "oh no your input single point is NOT on start or end node"

    else:
        print "super all points are located on a start or end node" \
              "NOTE point duplicates are NOT checked"


check_points_cover_start_end(shp2_points, shp1_lines)