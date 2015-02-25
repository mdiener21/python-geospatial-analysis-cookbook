#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt

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