#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt

import shapefile
from matplotlib import pyplot
from descartes import PolygonPatch
from shapely.ops import polygonize
from shapely.geometry import Polygon, LineString, Point
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


roads_input_shp = r"../geodata/roads_london_3857.shp"
clip_area = r"../geodata/clip_area_3857.shp"


def shape_to_shply(shp_path):
    shape_reader = shapefile.Reader(shp_path)
    features = shape_reader.shapeRecords()

    if shape_reader.numRecords > 1:
        shply_list = []
        for feature in features:
            shply_obj = asShape(feature.shape.__geo_interface__)
            shply_list.append(shply_obj)

        # print shply_list
        return shply_list
    else:
        shply_object = shape_reader.shape()
        print "only one record"
        print shply_object
        return shply_object


def shply_to_shape(shply_obj_list, out_path):
    """
    outpath looks like this out_path = r"../geodata/split_up_poly_circle.shp"
    :param shply_obj_list:
    :param out_path:
    :return:
    """

    pyshp_writer = shapefile.Writer()
    pyshp_writer.field("name")
    for feature in shply_obj_list:
        geojson = mapping(feature)

        # create empty pyshp shape
        record = shapefile._Shape()

        # shapeType 3 is Mulitlinestring
        # shapeType 8 is Multipolygon
        # shapeType 5 is Polygon
        record.shapeType = 5
        record.points = geojson["coordinates"][0]
        record.parts = [0]

        pyshp_writer._shapes.append(record)
        # add a list of attributes to go along with the shape
        pyshp_writer.record(["empty record"])

    pyshp_writer.save(out_path)


# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

# ###################################
# first plot
#  display sample line and circle
# ###################################

# first figure upper left drawing
# 222 represents the number_rows, num_cols, subplot number
ax = fig.add_subplot(121)

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


# ###################################
#             second plot
#  display sample intersection
# ###################################

ax = fig.add_subplot(122)

# convert circle polygon to linestring of circle boundary
cirle_as_line = polygon.boundary

# combine new boundary lines with the input set of lines
result_union_lines = cirle_as_line.union(line)

# re-create polygons from unioned lines
new_polygons = polygonize(result_union_lines)

# stores the final split up polygons
new_cut_ply = []

# identify which new polygon we want to keep
for poly in new_polygons:
    # check if new poly is inside original otherwise ignore it
    if poly.centroid.within(polygon):
        # center_pt = poly.centroid
        # ax.plot(center_pt.x, center_pt.y, 'o', color='#999999')
        print "creating new split polygon"
        patch3 = PolygonPatch(poly, fc='purple', alpha=0.5, zorder=2)
        ax.add_patch(patch3)
        # add only polygons that overlap original for export
        new_cut_ply.append(poly)
    else:
        # draw centroid of new polygon NOT inside original polygon
        # center_pt = poly.centroid
        # ax.plot(center_pt.x, center_pt.y, 'o', color='#FF1813')
        print "This polygon is outside of the input features"


# write title of second plot
ax.set_title('Line intersects circle')

# define the area that plot will fit into
x_range = set_plot_bounds(polygon, 1.5)['xrange']
y_range = set_plot_bounds(polygon, 1)['yrange']

ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_aspect(1)

pyplot.show()

# full path to where we will store the shapefile
split_poly_output = r"../geodata/split_up_poly_circle.shp"

# execute our conversion from Shapely to Shapefile
shply_to_shape(new_cut_ply, split_poly_output)
