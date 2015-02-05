#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shapely.ops import snap
from matplotlib import pyplot
from shapely.geometry import LineString, Point
from utils import SIZE, BLUE, RED, GREEN, GRAY
from utils import plot_coords_line
from utils import plot_line

# input origin line an point
line = LineString([(0.5, 0.5), (2.0, 1.5), (3.0, 0.5)])
point = Point(3, 1.8)

# point location using shapely snap
pt_snap_res = snap(point, line, 1.1)

# nearest point using linear referencing
# with interpolation and project
pt_interpolate = line.interpolate(line.project(point))

# print coordinates and distance to console
print "origin point coordinate"
print point

print "pt_snap_res coordinate"
print pt_snap_res

print "shplySnapPoint"
print pt_interpolate

print "distance from origin to snap point"
print point.distance(pt_snap_res)

print "distance from origin to interploate point"
print point.distance(pt_interpolate)


# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

# ###################################
# plot display sample line and point
# ###################################

# 121 represents the number_rows, num_cols, subplot number
ax = fig.add_subplot(121)

# add line using our utils function
plot_line(ax, line)

# draw a line from origin point to nearest points
line_to_snap_pt = LineString([point, pt_snap_res])
line_to_interplate_pt = LineString([point, pt_interpolate])

# plot the grey dashed line
plot_line(ax, line_to_snap_pt, '#000000', ls='--',
          linewidth=0.4, c=GRAY)
plot_line(ax, line_to_interplate_pt, '#666666', ls='--',
          linewidth=0.4, c=GRAY)

# plot our input origin point and resulting points
plot_coords_line(ax, point, BLUE, 'x', 'original-pt')
plot_coords_line(ax, pt_snap_res, RED, 'o', 'snap-res')
plot_coords_line(ax, pt_interpolate, color=GREEN, symbol='o',
                 label='good-snap', mew=1, ms=8)

# subplot title text
ax.set_title('Snap Point to Line')

# define axis ranges as list [x-min, x-max]
x_range = [line.bounds[0] - 1.0, line.bounds[2] + 1.5]

# y-range [y-min, y-max]
y_range = [line.bounds[1] - 1.0, line.bounds[3] + 1.0]

# set the x and y axis limits
ax.set_xlim(x_range)
ax.set_ylim(y_range)

# assing the aspect ratio
ax.set_aspect(1)

pyplot.show()