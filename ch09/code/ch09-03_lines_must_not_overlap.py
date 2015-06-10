#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import out_geoj

in_shp_line = "../geodata/topo_line.shp"
in_shp_overlap = "../geodata/topo_line_overlap.shp"

shp1_data = shp2_geojson_obj(in_shp_line)
shp2_data = shp2_geojson_obj(in_shp_overlap)

shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")
shp2_lines_overlap = create_shply_multigeom(shp2_data, "MultiLineString")

overlap_found = False

for line in shp1_lines:
    if line.equals(shp2_lines_overlap):
        print "equals"
        overlap_found = True
    if line.within(shp2_lines_overlap):
        print "within"
        overlap_found = True

# output the overlapping linestrings
if overlap_found:
    print "now exporting overlaps to GeoJSON"
    out_int = shp1_lines.intersection(shp2_lines_overlap)
    out_geoj(out_int, '../geodata/overlapping_lines.geojson')

    # create final linestring only list of overlapping lines
    # uses a pyhton list comprehension expression
    # only export the linestrings Shapely also creates  2 Points
    # where the linestrings cross and touch
    final = [feature for feature in out_int if feature.geom_type == "LineString"]

    # code if you do not want to use a list comprehension expresion
    # final = []
    # for f in out_int:
    #     if f.geom_type == "LineString":
    #         final.append(f)

    # export final list of geometries to GeoJSON
    out_geoj(final, '../geodata/final_overlaps.geojson')
else:
    print "hey no overlapping linestrings"