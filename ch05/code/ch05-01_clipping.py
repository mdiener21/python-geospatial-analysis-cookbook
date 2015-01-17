#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        ax.plot(x, y, color=color, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)


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


roads_london = shapefile.Reader(r"../geodata/roads_london_3857.shp")
# print roads_london.bbox
clip_area = shapefile.Reader(r"../geodata/clip_area_3857.shp")
clip_feature = clip_area.shape()
cf = asShape(clip_feature)
print cf.geom_type
#roads_clipped = shapefile.Writer(roads_london.shapeType)


roads_features = roads_london.shapeRecords()
roads_shply_list = []

for feature in roads_features:
    roads_london_shply = asShape(feature.shape.__geo_interface__)
    print roads_london_shply.geom_type
    its = roads_london_shply.intersection(cf)
    if its.geom_type == "LineString":
        print "yes linestring"
        roads_shply_list.append(its)
        # print roads_london_shply

# pprint(roads_shply_list[0].bounds)
# pprint(roads_shply_list[0].geom)
# pprint(roads_shply_list)
shapewriter2 = shapefile.Writer()
shapewriter2.field("field1")

for x in roads_shply_list:
    geoj = mapping(x)
    print x

# create empty pyshp shape
    record = shapefile._Shape()
    record.shapeType = 3
    record.points = geoj["coordinates"]
    record.parts = [0]

    shapewriter2._shapes.append(record)
    # add a list of attributes to go along with the shape
    shapewriter2.record(["empty record"])
    # save it
shapewriter2.save("test_shapelytopyshp.shp")


line = LineString([(0, 1), (3, 1), (0, 0)])
line2 = LineString([(0.5, 2.5), (3, 0)])
polygon = Polygon(Point(1.5, 1).buffer(1))

line_bounds = line.bounds
# print line.bounds

# coords_multilinestring = [((0, 0), (1, 1)), ((-1, 0), (1, 0))]
# my_multilinestring = MultiLineString(coords_multilinestring)
# my_lines = []


# figure 2 input line and polygon

fig = pyplot.figure(1, figsize=SIZE, dpi=90)

# ####### 2  Lines inside circle aka the CLIPPED lines
# #col,#row,#plotnumber
ax = fig.add_subplot(121)

patch1 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
ax.add_patch(patch1)
plot_line(ax, line)
plot_coords_line(ax, line)
plot_line(ax, line2, YELLOW)
plot_coords_line(ax, line2, YELLOW)

ax.set_title('input line and polygon')

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
ax = fig.add_subplot(122)

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
ax.set_title('line intersects polygon')

# define the area that plot will fit into
xrange = [-1, 4]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)

# draw the diagram and open it on screen
pyplot.show()

