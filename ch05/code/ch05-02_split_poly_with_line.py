#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import pyplot
from descartes import PolygonPatch
from shapely.ops import polygonize
from shapely.geometry import Polygon, LineString, Point

from utils import SIZE, BLUE
from utils import plot_coords_line
from utils import plot_line
from utils import set_plot_bounds


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

# our demonstration geometries to see the details
line = LineString([(0, 1), (3, 1), (0, 0)])
polygon = Polygon(Point(1.5, 1).buffer(1))

# use of descartes to create polygon in matplotlib
patch1 = PolygonPatch(polygon, fc=BLUE,
                      ec=BLUE, alpha=0.5, zorder=1)

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


#####################################
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
        patch3 = PolygonPatch(poly, fc='purple',
                              alpha=0.5, zorder=2)
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