#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile
import geojson
import os
# used to import dictionary data to shapely
from shapely.geometry import asShape
from shapely.geometry import mapping

# open roads Shapefile that we want to clip with pyshp
roads_london = shapefile.Reader(r"../geodata/roads_london_3857.shp")

# open circle polygon with pyshp
clip_area = shapefile.Reader(r"../geodata/clip_area_3857.shp")

# access the geometry of the clip area circle
clip_feature = clip_area.shape()

# convert pyshp object to shapely
clip_shply = asShape(clip_feature)

# create a list of all roads features and attributes
roads_features = roads_london.shapeRecords()

# variables to hold new geometry
roads_clip_list = []
roads_shply = []

# run through each geometry, convert to shapely geom and intersect
for feature in roads_features:
    roads_london_shply = asShape(feature.shape.__geo_interface__)
    roads_shply.append(roads_london_shply)
    roads_intersect = roads_london_shply.intersection(clip_shply)

    # only export linestrings, shapely also created points
    if roads_intersect.geom_type == "LineString":
        roads_clip_list.append(roads_intersect)

# open writer to write our new shapefile too
pyshp_writer = shapefile.Writer()

# create new field
pyshp_writer.field("name")

# convert our shapely geometry back to pyshp, record for record
for feature in roads_clip_list:
    geojson = mapping(feature)

    # create empty pyshp shape
    record = shapefile._Shape()

    # shapeType 3 is linestring
    record.shapeType = 3
    record.points = geojson["coordinates"]
    record.parts = [0]

    pyshp_writer._shapes.append(record)
    # add a list of attributes to go along with the shape
    pyshp_writer.record(["empty record"])

# save to disk
pyshp_writer.save(r"../geodata/roads_clipped2.shp")
