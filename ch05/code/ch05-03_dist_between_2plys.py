#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shapely.ops import snap
from matplotlib import pyplot
from shapely.geometry import LineString, Point
from utils import SIZE, BLUE, RED, GREEN, GRAY
from utils import plot_coords_line
from utils import plot_line

line = LineString([(0.5, 0.5), (2.0, 1.5), (3.0, 0.5)])
point = Point(3, 1.8)
pt_snap_res = snap(point, line, 4)
shplySnapPoint = line.interpolate(line.project(point))

print "point"
print point
print "pt_snap_res"
print pt_snap_res
print "shplySnapPoint"
print shplySnapPoint


# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

# ###################################
# first plot
# display sample line and circle
# ###################################

# first figure upper left drawing
# 121 represents the number_rows, num_cols, subplot number
ax = fig.add_subplot(121)

# add line using our function above
plot_line(ax, line)

# draw the line nodes using our function
# plot_coords_line(ax, line)

new_line_wrong = LineString([point, pt_snap_res])
new_line_correct = LineString([point, shplySnapPoint])

plot_line(ax, new_line_wrong, '#000000', ls='--', linewidth=0.4, c=GRAY)
plot_line(ax, new_line_correct, '#666666', ls='--', linewidth=0.4, c=GRAY)

plot_coords_line(ax, point, BLUE, 'x', 'original-pt')
plot_coords_line(ax, pt_snap_res, RED, 'o', 'snap-res')
plot_coords_line(ax, shplySnapPoint, color=GREEN, symbol='o', label='good-snap', mew=1, ms=8)


# subplot title text
ax.set_title('Snap Point to Line')

# define axis ranges as list [x-min, x-max]
# added 1.5 units around object so not touching the sides
x_range = [line.bounds[0] - 1.0, line.bounds[2] + 1.5]

# y-range [y-min, y-max]
y_range = [line.bounds[1] - 1.0, line.bounds[3] + 1.0]

# set the x and y axis limits
ax.set_xlim(x_range)
ax.set_ylim(y_range)

# assing the aspect ratio
ax.set_aspect(1)

pyplot.show()