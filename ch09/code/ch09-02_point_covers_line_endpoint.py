#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import out_geoj
from shapely.geometry import Point, MultiPoint

in_shp_line = "../geodata/topo_line.shp"
in_shp_point = "../geodata/topo_points.shp"

shp1_data = shp2_geojson_obj(in_shp_line)
shp2_data = shp2_geojson_obj(in_shp_point)

shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")
shp2_points = create_shply_multigeom(shp2_data, "MultiPoint")


def create_start_end_pts(lines):
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

    :param points:
    :param lines:
    :return:
    '''

    all_start_end_nodes = create_start_end_pts(lines)

    bad_points = []
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


    out_geoj(bad_points, '../geodata/points_not_on_start_end.geojson')


check_points_cover_start_end(shp2_points, shp1_lines)