#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile
from utils import shp_to_shply_multiply
from utils import shp_2_geojson_file
from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import out_geoj
from shapely.geometry import Point, MultiPoint
from shapely.geometry import MultiLineString, LineString

in_shp_line = "../geodata/topo_line.shp"
in_shp_point = "../geodata/topo_points.shp"

shp1_data = shp2_geojson_obj(in_shp_line)
shp2_data = shp2_geojson_obj(in_shp_point)

shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")
shp2_points = create_shply_multigeom(shp2_data, "MultiPoint")


line = LineString([(0, 0), (1, 1), (2, 2), (3, 3)])
line_cross = LineString([(3, 0), (2, 1), (1, 2), (0, 3)])


point_on_edge = Point(0.5, 0.5)
point_on_vertex = Point(3, 3)
point_on_end = Point(3, 3)
point_on_start = Point(0, 0)
point_intersect = Point(1.5, 1.5)
point_inside = Point(2.5, 2.5)
point_outside = Point(10, 10)


pt_series = MultiPoint([(1, 1), (2, 2), (4, 4), (5, 5), (16, 16), (60, 60), (70, 70)])
line_series = MultiLineString([line, line_cross])

print line
coords = list(line.coords)
print coords

get_start_line_coord = Point(coords[0])
get_end_line_coord = Point(coords[-1])


print get_start_line_coord
print get_end_line_coord


def covered_by_endpoint(points, lines, ret_errors=True):
    final_not_covered = []
    final_set = []

    for pt in points:

        set_pts_covered = []
        set_pts_not_covered = []

        for line in lines:

            coords = list(line.coords)
            # print coords

            get_start_line_coord = Point(coords[0])
            get_end_line_coord = Point(coords[-1])

            if pt.equals(get_start_line_coord):
                #print "point on start of line"
                set_pts_covered.append(pt)

            elif pt.equals(get_end_line_coord):
                #print "point on end of line"
                set_pts_covered.append(pt)

            # else:
            #     set_pts_not_covered.append(pt)

        final_set.append(set_pts_covered)
        if pt.within(lines):
            final_not_covered.append(pt)
        elif pt.disjoint(lines):
            final_not_covered.append(pt)

    if ret_errors:
        return final_not_covered
    else:
        return final_set

empty = []

if empty:
    print "True"
else:
    print "False it is empty"
res = covered_by_endpoint(shp2_points, shp1_lines, True)
print res


print "testing"
out_j = []
print out_j
for r in res:
    if r:  # if list empty
        for x in r:
            # print all points that are GOOD
            out_j.append(x)
    # else:
    #     print r

out_geoj(out_j, '../geodata/badpoints.geojson')



#myMulti = MultiPoint(res)

#print myMulti