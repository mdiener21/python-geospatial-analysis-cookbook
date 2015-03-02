#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import shapefile
from geojson import loads, Feature, FeatureCollection

# open roads Shapefile that we want to clip with pyshp
from shapely.geometry import asShape, Point
from shapely.geometry import mapping
from shapely.ops import polygonize

in_ply_1 = shapefile.Reader("../geodata/temp1-ply.shp")

# open circle polygon with pyshp
in_ply_2 = shapefile.Reader("../geodata/temp2-ply.shp")

# access the geometry of the clip area circle
in_ply_2_shape = in_ply_2.shape()
in_ply_1_shape = in_ply_1.shape()

# convert pyshp object to shapely
in_ply_2_shply = asShape(in_ply_2_shape)
in_ply_1_shply = asShape(in_ply_1_shape)
out_boundaries = in_ply_1_shply.boundary.union(in_ply_2_shply.boundary)


out_shply = polygonize(out_boundaries)


new_cut_ply = []
for feature in out_shply:
#print out_shply
    foo = feature.__geo_interface__

    myfeat = Feature(geometry=foo, properties={'name': "mojo"})
    new_cut_ply.append(feature)
print myfeat


output_union = "../geodata/output_union.geojson"

def write_geojson():
    with open(output_union, "w") as f:
        f.write(json.dumps(myfeat))

write_geojson()


#print foo
# create a list of all roads features and attributes
# in_ply_1_records = in_ply_1.shapeRecords()
# in_ply_2_records = in_ply_2.shapeRecords()

# variables to hold new geometry
# roads_clip_list = []
# roads_shply = []

# run through each geometry, convert to shapely geom and intersect
# for feature in in_ply_1_records:
#     roads_london_shply = asShape(feature.shape.__geo_interface__)
#     roads_shply.append(roads_london_shply)
#     roads_intersect = roads_london_shply.union(in_ply_2_shply)
#
#     # only export linestrings, shapely also created points
#     if roads_intersect.geom_type == "Polygon":
#         roads_clip_list.append(roads_intersect)

# # open writer to write our new shapefile too
# out_ply_union = shapefile.Writer()
#
# # create new field
# out_ply_union.field("name")

# convert our shapely geometry back to pyshp, record for record
# for feature in out_shply:
#     geojson = mapping(feature)
#
#     # create empty pyshp shape
#     record = shapefile._Shape()
#
#     # shapeType 8 is MultiPolygon
#     record.shapeType = 8
#     record.points = geojson["coordinates"]
#     record.parts = [0]
#
#     out_ply_union._shapes.append(record)
#     # add a list of attributes to go along with the shape
#     out_ply_union.record(["empty record"])

# save to disk
# out_ply_union.save(r"../geodata/temp_union.shp")