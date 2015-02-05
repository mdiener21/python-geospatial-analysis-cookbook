#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt

import shapefile
from shapely.geometry import asShape
from shapely.geometry import mapping


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
    if len(shply_obj_list) > 1:
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
    else:
        geojson = mapping(shply_obj_list[0])
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


# calculate the size of our matplotlib output
GM = (sqrt(5) - 1.0) / 2.0
W = 8.0
H = W * GM
SIZE = (W, H)

# colors for our plots as hex
GRAY = '#B2B3B7'
BLUE = '#6699cc'
YELLOW = '#ffe680'
RED = '#FF1813'
GREEN = '#24CD17'


# functions slightly modified from Sean Gilles http://toblerity.org/shapely/
# used for drawing our results using matplotlib

# matplotlib makers http://matplotlib.org/api/markers_api.html
def plot_coords_line(axis, object, color='#00b700',
                     symbol='o', label="text", mew=1, ms=7):
    """
    mew = marker edge width in points
    ms = marke size in points

    """
    x, y = object.xy
    axis.plot(x, y, symbol, label=label, color=color,
              mew=mew, ms=ms, zorder=1)


def plot_coords_lines(axis, object, color='#999999'):
    for linestring in object:
        x, y = linestring.xy
        axis.plot(x, y, 'o', color=color, zorder=2)


def plot_line(axis, object, color='#00b700', ls='-',
              linewidth=2, c='g'):
    """
    ls is the line style options :[ '-' | '--' | '-.' | ':' | 'steps' | ...]
    """
    x, y = object.xy
    axis.plot(x, y, color=color, linewidth=linewidth, ls=ls, c=c, zorder=1)


def plot_lines(axis, object, color='#00b700'):
    for line in object:
        x, y = line.xy
        axis.plot(x, y, color=color, alpha=0.4, linewidth=1,
                  solid_capstyle='round', zorder=2)


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