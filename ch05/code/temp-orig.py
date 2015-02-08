#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pprint import pprint

from matplotlib import pyplot
import shapefile
from shapely.geometry import Polygon, LineString, Point
from descartes import PolygonPatch
from shapely.geometry import asShape  # used to import dictionary data to shapely
from shapely.geometry import mapping
from figures import SIZE


# COLOR = {
# True:  '#6699cc',
#     False: '#ffcc33'
#     }

GRAY = '#00b700'
BLUE = '#6699cc'
YELLOW = '#ffe680'

# def v_color(ob):
#     return COLOR[ob.is_simple]
#


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


def plot_bounds(ax, ob):
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))
    ax.plot(x, y, 'o', color='#000000', zorder=1)


def set_plot_bounds(object):  # (minx, miny, maxx, maxy
    bounds = object.bounds
    x_min = bounds[0]
    y_min = bounds[1]
    x_max = bounds[2]
    y_max = bounds[3]

    return bounds

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

# print clip_feature_shply.geom_type


roads_features = roads_london.shapeRecords()
roads_shply_list = []

orig_roads_shply = []

for feature in roads_features:
    roads_london_shply = asShape(feature.shape.__geo_interface__)
    orig_roads_shply.append(roads_london_shply)
    #print roads_london_shply.geom_type
    its = roads_london_shply.intersection(clip_feature_shply)
    if its.geom_type == "LineString":
        #print "yes linestring"
        roads_shply_list.append(its)
        # print roads_london_shply

# pprint(roads_shply_list[0].bounds)
# pprint(roads_shply_list[0].geom)
# pprint(roads_shply_list)
shapewriter2 = shapefile.Writer()
shapewriter2.field("name")

for x in roads_shply_list:
    geoj = mapping(x)
    #print x

# create empty pyshp shape
    record = shapefile._Shape()
    record.shapeType = 3
    record.points = geoj["coordinates"]
    record.parts = [0]

    shapewriter2._shapes.append(record)
    # add a list of attributes to go along with the shape
    shapewriter2.record(["empty record"])
    # save it
shapewriter2.save(r"../geodata/roads_clipped.shp")


line = LineString([(0, 1), (3, 1), (0, 0)])

polygon = Polygon(Point(1.5, 1).buffer(1))

line_bounds = line.bounds
# print line.bounds

# coords_multilinestring = [((0, 0), (1, 1)), ((-1, 0), (1, 0))]
# my_multilinestring = MultiLineString(coords_multilinestring)
# my_lines = []


# figure 2 input line and polygon

fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")


fig.subplots_adjust(hspace=.5)

# ####### 2  Lines inside circle aka the CLIPPED lines
# #col,#row,#plotnumber
ax = fig.add_subplot(221)

patch1 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
ax.add_patch(patch1)
plot_line(ax, line)
plot_coords_line(ax, line)


ax.set_title('Input line and circle')

xrange = [line.bounds[0] - 1.0, line.bounds[2] + 1.0]
yrange = [line.bounds[1] - 1.0, line.bounds[3] + 2.0]
# ax.set_xlim(*xrange)
ax.set_xlim(xrange)
# ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(yrange)
# ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)


# ###################################
# ##   second plot
# ###################################
ax = fig.add_subplot(224)


# create matplotlib patch
#patch2 = PolygonPatch(clip_feature_shply, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)

# add polygon to plot
#ax.add_patch(patch2)

# run the intersection
#intersect_line = line.intersection(polygon)

# plot the lines and the line vertex to plot
plot_lines(ax, roads_shply_list, color='#3C3F41')
# plot_coords_lines(ax, intersect_line, color='#3C3F41')

# write title of second plot
ax.set_title('Roads intersect circle')

# define the area that plot will fit into
xrange = [clip_feature_shply.bounds[0] - 200.0, clip_feature_shply.bounds[2] + 200.0]
yrange = [clip_feature_shply.bounds[1] - 200.0, clip_feature_shply.bounds[3] + 200.0]
import math
ax.set_xlim(xrange)
# ax.set_xticks(range(*xrange) + [xrange[-1]])
#ax.set_xticks(range(int(round(xrange))) + [int(xrange[-1.0])])

ax.set_ylim(yrange)
#ax.set_yticks(range(int(round(*yrange))) + [int(yrange[-1.0])])
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
xrange = [-1, 4]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)


ax = fig.add_subplot(222)



# run the intersection
#intersect_line = line.intersection(polygon)

# plot the lines and the line vertex to plot
plot_lines(ax, orig_roads_shply, color='#3C3F41')
# plot_coords_lines(ax, intersect_line, color='#3C3F41')

# create matplotlib patch
patch2 = PolygonPatch(clip_feature_shply, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)

# add polygon to plot
ax.add_patch(patch2)
# write title of second plot
ax.set_title('Input roads and circle')

# define the area that plot will fit into
xrange = [clip_feature_shply.bounds[0] - 600.0, clip_feature_shply.bounds[2] + 600.0]
yrange = [clip_feature_shply.bounds[1] - 600.0, clip_feature_shply.bounds[3] + 600.0]
ax.set_xlim(*xrange)
#ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
#ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)
ax.set_xticklabels([])
ax.set_yticklabels([])
pyplot.show()

