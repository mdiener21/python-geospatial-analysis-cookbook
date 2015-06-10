#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import out_geoj
from shapely.geometry import Point

in_shp_dangles = "../geodata/topo_dangles.shp"
shp1_data = shp2_geojson_obj(in_shp_dangles)
shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")


def find_dangles(lines):
    """
    Locate all dangles
    :param lines: list of Shapely LineStrings or MultiLineStrings
    :return: list of dangles
    """
    list_dangles = []
    for i, line in enumerate(lines):
        # each line gets a number
        # go through each line added first to second
        # then second to third and so on
        shply_lines = lines[:i] + lines[i+1:]
        # 0 is start point and -1 is end point
        # run through
        for start_end in [0, -1]:
            # convert line to point
            node = Point(line.coords[start_end])
            # Return True if any element of the iterable is true.
            # https://docs.python.org/2/library/functions.html#any
            # python boolean evaluation comparison
            if any(node.touches(next_line) for next_line in shply_lines):
                continue
            else:
                list_dangles.append(node)
    return list_dangles

# convert our Shapely MultiLineString to list
list_lines = [line for line in shp1_lines]

# find those dangles
result_dangles = find_dangles(list_lines)

# return our results
if len(result_dangles) >= 1:
    print "yes we found some dangles exporting to GeoJSON"
    out_geoj(result_dangles, '../geodata/dangles.geojson')
else:
    print "no dangles found"
