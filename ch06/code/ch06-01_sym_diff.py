#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from shapely.geometry import MultiPolygon
from shapely.geometry import asShape
from shapely.wkt import dumps

######################
from matplotlib import pyplot
from descartes import PolygonPatch
from utils import SIZE
from utils import set_plot_bounds
####################################

# define our files input and output locations
output_wkt_sym_diff = "../geodata/results_sym_diff.js"
input_fairways = "../geodata/pebble-beach-fairways-3857.geojson"
input_greens = "../geodata/pebble-beach-greens-3857.geojson"

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
# write_wkt(output_wkt_sym_diff,result)


#####################################
#      plot with Matplotlib
#  display symmetric difference
# ###################################

# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

ax = fig.add_subplot(111)

# draw each MultiPolygon green
for poly in result:
    patch3 = PolygonPatch(poly, fc='green',
                          alpha=0.5, zorder=2)
    ax.add_patch(patch3)

ax.set_title('sym diff work')

# define the area that plot will fit into
x_range = set_plot_bounds(result, 50)['xrange']
y_range = set_plot_bounds(result, 50)['yrange']

ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_aspect(1)

pyplot.show()

