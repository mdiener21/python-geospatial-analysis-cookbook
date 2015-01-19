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
def plot_coords_line(ax, ob, color='#00b700'):
    x, y = ob.xy
    ax.plot(x, y, 'o', color=color, zorder=1)


def plot_coords_lines(ax, ob, color='#999999'):
    for linestring in ob:
        x, y = linestring.xy
        ax.plot(x, y, 'o', color=color, zorder=2)


def plot_line(ax, ob, color='#00b700'):
    x, y = ob.xy
    ax.plot(x, y, color=color, linewidth=3, zorder=1)


def plot_lines(ax, ob, color='#00b700'):
    for line in ob:
        x, y = line.xy
        ax.plot(x, y, color=color, alpha=0.4, linewidth=1, solid_capstyle='round', zorder=2)


def set_plot_bounds(obj, offset=1.0):
    """
    Creates the limits for x and y axis plot

    :param obj: input shapely geometry
    :param offset: amount of space around edge of features
    :return: dictionary of x-range and y-range values for
    """
    bounds = obj.bounds
    x_min = bounds[0]
    y_min = bounds[1]
    x_max = bounds[2]
    y_max = bounds[3]
    xrange = [x_min - offset, x_max + offset]
    yrange = [y_min - offset, y_max + offset]

    return {'xrange': xrange, 'yrange': yrange}

# open road lines that we want to clip
roads_london = shapefile.Reader(r"../geodata/roads_london_3857.shp")
roads_london_bbox = roads_london.bbox
# print roads_london.bbox

# open shapefile with pyshp
clip_area = shapefile.Reader(r"../geodata/clip_area_3857.shp")

# access the geometry of the clip area
clip_feature = clip_area.shape()

# convert pyshp object to shapely
clip_feature_shply = asShape(clip_feature)

roads_features = roads_london.shapeRecords()
roads_shply_list = []
orig_roads_shply = []

for feature in roads_features:
    roads_london_shply = asShape(feature.shape.__geo_interface__)
    orig_roads_shply.append(roads_london_shply)
    its = roads_london_shply.intersection(clip_feature_shply)
    if its.geom_type == "LineString":
        roads_shply_list.append(its)

shapewriter2 = shapefile.Writer()
shapewriter2.field("name")

for x in roads_shply_list:
    geoj = mapping(x)

    # create empty pyshp shape
    record = shapefile._Shape()
    record.shapeType = 3
    record.points = geoj["coordinates"]
    record.parts = [0]

    shapewriter2._shapes.append(record)
    # add a list of attributes to go along with the shape
    shapewriter2.record(["empty record"])

shapewriter2.save(r"../geodata/roads_clipped.shp")
line = LineString([(0, 1), (3, 1), (0, 0)])
polygon = Polygon(Point(1.5, 1).buffer(1))


# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

# ####### 2  Lines inside circle aka the CLIPPED lines
# #col,#row,#plotnumber
ax = fig.add_subplot(221)

patch1 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
ax.add_patch(patch1)
plot_line(ax, line)
plot_coords_line(ax, line)

ax.set_title('Input line and circle')

xrange = set_plot_bounds(polygon, 1.5)['xrange']
yrange = set_plot_bounds(polygon, 1)['yrange']

ax.set_xlim(xrange)
ax.set_ylim(yrange)
ax.set_aspect(1)


# ###################################
# ##   second plot
# ###################################
ax = fig.add_subplot(224)

# plot the lines and the line vertex to plot
plot_lines(ax, roads_shply_list, color='#3C3F41')

# write title of second plot
ax.set_title('Roads intersect circle')

# define the area that plot will fit into
xrange = [clip_feature_shply.bounds[0] - 200.0, clip_feature_shply.bounds[2] + 200.0]
yrange = [clip_feature_shply.bounds[1] - 200.0, clip_feature_shply.bounds[3] + 200.0]

ax.set_xlim(xrange)
ax.set_ylim(yrange)
ax.set_aspect(1)

ax.set_xticklabels([])
ax.set_yticklabels([])

ax = fig.add_subplot(223)

# create matplotlib patch
patch2 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)

# add polygon to plot
ax.add_patch(patch2)

# run the intersection
intersect_line = line.intersection(polygon)

# plot the lines and the line vertex to plot
plot_lines(ax, intersect_line, color='#3C3F41')
plot_coords_lines(ax, intersect_line, color='#3C3F41')

# write title of second plot
ax.set_title('Line intersects circle')

# define the area that plot will fit into
xrange = set_plot_bounds(polygon, 1.5)['xrange']
yrange = set_plot_bounds(polygon, 1)['yrange']

ax.set_xlim(*xrange)
ax.set_ylim(*yrange)

ax.set_aspect(1)

# create the second plot located at
ax = fig.add_subplot(222)

# draw our original imput lines and circle
plot_lines(ax, orig_roads_shply, color='#3C3F41')
patch2 = PolygonPatch(clip_feature_shply, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)

# add polygon to plot
ax.add_patch(patch2)

# write title of second plot
ax.set_title('Input roads and circle')

# define the area that plot will fit into
xrange = set_plot_bounds(clip_feature_shply, 600)['xrange']
yrange = set_plot_bounds(clip_feature_shply, 600)['yrange']

ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

ax.set_xticklabels([])
ax.set_yticklabels([])

pyplot.show()