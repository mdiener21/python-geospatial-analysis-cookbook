#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/qgis/QGIS/blob/e5fb5a6ad90b4656e66cf256be3345005c627400/src/plugins/topology/topolTest.cpp
import shapefile
from utils import shp_to_shply_multiply
from utils import shp_2_geojson_file
from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import shp2_shply_geom
from utils import out_geoj
from shapely.geometry import Point, MultiPoint
from shapely.geometry import MultiLineString, LineString
import shapefile

in_shp_dangles = "../geodata/topo_dangles.shp"

shp1_data = shp2_geojson_obj(in_shp_dangles)

shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")

s1 = Point(1,1)
s2 = Point(1,1)
e1 = Point(2,2)
e2 = Point(-1,-1)
s3 = Point(-1,-1)
e3 = Point(-2,-2)

if not s1.equals(s2):
    print "NOT s1 != s2"
else:
    print "true s1 =s2"


def find_dangles(lines):
    '''
     Dangles are edges which have one or both ends which
     are not incident on another edge endpoint
    :return: Line start or end points that dangle
    '''

    # find start and end nodes
    # if start node = end_node
    #     yes they join
    # if end_node = start_node
    #     yes they join
    #
    list_end_nodes = []
    list_start_nodes = []
    for line in lines:
        coords = list(line.coords)

        line_start_point = Point(coords[0])
        line_end_point = Point(coords[-1])

        list_start_nodes.append(line_start_point)
        list_end_nodes.append(line_end_point)

    # print list_end_nodes
    # print list_start_nodes


    # for en in list_end_nodes:
    #     print en.wkt
    #
    # print "now start nodes"
    # for sn in list_start_nodes:
    #     print sn.wkt
    #
    # print "now together start and end"
    #
    # print list_start_nodes + list_end_nodes

    # for val in list_start_nodes:
    #     if val in list_end_nodes:
    #         print True
    # print False
    f = []
    dangles = []
    for start_pt in list_start_nodes:

        # if start_pt.equals(start_pt):
        # print "yes start = start"
        # print start_pt.wkt
        not_dangle = []
        yes_dangle = []
        start_pt1 = start_pt

        if not start_pt1.intersects(start_pt):
            print "not intersect"

            for end_pt in list_end_nodes:
                if start_pt.intersects(end_pt):
                    # if start_pt.wkt == end_pt.wkt:
                    # print "yes start pt = end pt"
                    yes_dangle.append(start_pt)
                    # print start_pt.wkt
                    # if end_pt.equals(start_pt):
                    #     print "yes end = start"
                    #     print end_pt.wkt
                    # if end_pt.equals(end_pt):
                    #     print "yes end = end"
                    # else:
                    #     print "hmm"
            dangles.append(yes_dangle)
        else:
            print "intersect"
    return dangles


print "output"
list_not_dangles = find_dangles(shp1_lines)
print list_not_dangles

final = []
for x in list_not_dangles:
    for x2 in x:
        final.append(x2)
        print x2

# for x in list_not_dangles:
#     final.append(x)


out_geoj(final, '../geodata/dangles.geojson')
