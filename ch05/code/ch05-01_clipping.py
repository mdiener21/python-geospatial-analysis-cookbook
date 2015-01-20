#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

import shapefile
from matplotlib import pyplot
from descartes import PolygonPatch
from shapely.geometry import Polygon, LineString, Point

# used to import dictionary data to shapely
from shapely.geometry import asShape
from shapely.geometry import mapping

# calculate the size of our matplotlib output
GM = (sqrt(5) - 1.0) / 2.0
W = 8.0
H = W * GM
SIZE = (W, H)

# colors for our plots as hex
GRAY = '#00b700'
BLUE = '#6699cc'
YELLOW = '#ffe680'


# functions slightly modified from Sean Gilles http://toblerity.org/shapely/
# used for drawing our results using matplotlib

def plot_coords_line(axis, object, color='#00b700'):
    x, y = object.xy
    ax.plot(x, y, 'o', color=color, zorder=1)


def plot_coords_lines(axis, object, color='#999999'):
    for linestring in object:
        x, y = linestring.xy
        ax.plot(x, y, 'o', color=color, zorder=2)


def plot_line(axis, object, color='#00b700'):
    x, y = object.xy
    ax.plot(x, y, color=color, linewidth=3, zorder=1)


def plot_lines(axis, object, color='#00b700'):
    for line in object:
        x, y = line.xy
        ax.plot(x, y, color=color, alpha=0.4, linewidth=1, solid_capstyle='round', zorder=2)


def set_plot_bounds(object, offset=1.0):
    """
    Creates the limits for x and y axis plot

    :param object: input shapely geometry
    :param offset: amount of space around edge of features
    :return: dictionary of x-range and y-range values for
    """
    bounds = object.bounds
    x_min = bounds[0]
    y_min = bounds[1]
    x_max = bounds[2]
    y_max = bounds[3]
    x_range = [x_min - offset, x_max + offset]
    y_range = [y_min - offset, y_max + offset]

    return {'xrange': x_range, 'yrange': y_range}

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
pyshp_writer.save(r"../geodata/roads_clipped.shp")

# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

# ###################################
#             first plot
#  display sample line and circle
# ###################################

# first figure upper left drawing
# 222 represents the number_rows, num_cols, subplot number
ax = fig.add_subplot(221)

# our demonstration geometries to see the details
line = LineString([(0, 1), (3, 1), (0, 0)])
polygon = Polygon(Point(1.5, 1).buffer(1))

# use of descartes to create polygon in matplotlib
# input circle and color fill and outline in blue with transparancy
patch1 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)

# add circle to axis in figure
ax.add_patch(patch1)

# add line using our function above
plot_line(ax, line)

# draw the line nodes using our function
plot_coords_line(ax, line)

# subplot title text
ax.set_title('Input line and circle')

# define axis ranges as list [x-min, x-max]
# added 1.5 units around object so not touching the sides
x_range = [polygon.bounds[0] - 1.5, polygon.bounds[2] + 1.5]

# y-range [y-min, y-max]
y_range = [polygon.bounds[1] - 1.0, polygon.bounds[3] + 1.0]

# set the x and y axis limits
ax.set_xlim(x_range)
ax.set_ylim(y_range)

# assing the aspect ratio
ax.set_aspect(1)

# ##########################################
#             second plot
#    display original input circle and roads
# ##########################################

ax = fig.add_subplot(222)

# draw our original input road lines and circle
plot_lines(ax, roads_shply, color='#3C3F41')

patch2 = PolygonPatch(clip_shply, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
ax.add_patch(patch2)

# write title of second plot
ax.set_title('Input roads and circle')

# define the area that plot will fit into plus 600m space around
x_range = set_plot_bounds(clip_shply, 600)['xrange']
y_range = set_plot_bounds(clip_shply, 600)['yrange']

ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_aspect(1)

# remove the x,y axis labels by setting empty list
ax.set_xticklabels([])
ax.set_yticklabels([])

# ###################################
#             third plot
#  display sample intersection
# ###################################

ax = fig.add_subplot(223)

patch2 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
ax.add_patch(patch2)

# run the intersection detail view
intersect_line = line.intersection(polygon)

# plot the lines and the line vertex to plot
plot_lines(ax, intersect_line, color='#3C3F41')
plot_coords_lines(ax, intersect_line, color='#3C3F41')

# write title of second plot
ax.set_title('Line intersects circle')

# define the area that plot will fit into
x_range = set_plot_bounds(polygon, 1.5)['xrange']
y_range = set_plot_bounds(polygon, 1)['yrange']

ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_aspect(1)

# ###################################
#             fourth plot
#  showing results of clipped roads
# ###################################

ax = fig.add_subplot(224)

# plot the lines and the line vertex to plot
plot_lines(ax, roads_clip_list, color='#3C3F41')

# write title of second plot
ax.set_title('Roads intersect circle')

# define the area that plot will fit into
x_range = set_plot_bounds(clip_shply, 200)['xrange']
y_range = set_plot_bounds(clip_shply, 200)['yrange']

ax.set_xlim(x_range)
ax.set_ylim(y_range)
ax.set_aspect(1)

# remove the x,y axis labels by setting empty list
ax.set_xticklabels([])
ax.set_yticklabels([])

# draw the plots to the screen
pyplot.show()