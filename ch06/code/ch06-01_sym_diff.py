#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from os.path import realpath
from shapely.geometry import MultiPolygon
from shapely.geometry import asShape
from shapely.wkt import dumps


# define our files input and output locations
input_fairways = realpath("../geodata/pebble-beach-fairways-3857.geojson")
input_greens = realpath("../geodata/pebble-beach-greens-3857.geojson")
output_wkt_sym_diff = realpath("ol3/data/ch06-01_results_sym_diff.js")


# open and load our geojson files as python dictionary
with open(input_fairways) as fairways:
    fairways_data = json.load(fairways)

with open(input_greens) as greens:
    greens_data = json.load(greens)

# create storage list for our new shapely objects
fairways_multiply = []
green_multply = []

# create shapely geometry objects for fairways
for feature in fairways_data['features']:
    shape = asShape(feature['geometry'])
    fairways_multiply.append(shape)

# create shapely geometry objects for greens
for green in greens_data['features']:
    green_shape = asShape(green['geometry'])
    green_multply.append(green_shape)

# create shapely MultiPolygon objects for input analysis
fairway_plys = MultiPolygon(fairways_multiply)
greens_plys = MultiPolygon(green_multply)

# run the symmetric difference function creating a new Multipolygon
result = fairway_plys.symmetric_difference(greens_plys)

# write the results out to well known text (wkt) with shapely dump
def write_wkt(filepath, features):
    with open(filepath, "w") as f:
        # create a js variable called ply_data used in html
        # Shapely dumps geometry out to WKT
        f.write("var ply_data = '" + dumps(features) + "'")

# write to our output js file the new polygon as wkt
write_wkt(output_wkt_sym_diff, result)
