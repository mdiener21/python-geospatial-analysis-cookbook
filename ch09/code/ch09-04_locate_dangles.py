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
mul = MultiPoint([s1,s2,e1])

print s1.disjoint(e1)

mypt = None

a = [1,1,1,1,2,2,2,2,3,3,4,5,5]
from itertools import groupby
[len(list(group)) for key, group in groupby(a)]

# for point in mul:
#     point = point.equals()
#     if point.equals(point):
#         print "its equal"

if not s1.equals(s2):
    print "NOT s1 != s2"
else:
    print "true s1 =s2"


# import itertools
# for a, b in itertools.combinations(mul, 2):
#     compare(a, b)


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

d = {} # creates an empty dictionary the first time

def find_duplicates(val):
    d[val] = d.setdefault(val, -1) + 1
    return d[val]


# remove duplicates
from collections import OrderedDict
list(OrderedDict.fromkeys('abracadabra'))
# ['a', 'b', 'r', 'c', 'd']

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

    all_nodes = list_end_nodes + list_start_nodes

    print len(all_nodes)




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
    not_dangle_master = []
    yes_dangle_master = []
    #for node in all_nodes:

    for start_pt in list_start_nodes:

        # if start_pt.equals(start_pt):
        # print "yes start = start"
        # print start_pt.wkt
        not_dangle = []
        yes_dangle = []

        for end_pt in list_end_nodes:

            if start_pt.equals(end_pt):
                #print "NOT a dangle"
                not_dangle.append(start_pt)

            if start_pt.disjoint(end_pt):
                #print "possible dangle !! look out"
                # if start_pt.wkt == end_pt.wkt:
                # print "yes start pt = end pt"

                # print start_pt.wkt
                # if end_pt.equals(start_pt):
                #     print "yes end = start"
                #     print end_pt.wkt
                # if end_pt.equals(end_pt):
                #     print "yes end = end"
                # else:
                #     print "hmm"
                dangles.append(yes_dangle)
        not_dangle_master.append(not_dangle)
        yes_dangle_master.append(yes_dangle)
    return yes_dangle_master


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


out_geoj(final, '../geodata/yes_dangles.geojson')
