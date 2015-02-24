#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shapely.geometry import Point, MultiPolygon, Polygon
from shapely.geometry import asShape, mapping
from shapely.wkt import dumps

from geojson import FeatureCollection
from geojson import loads, Feature, FeatureCollection
######################
from matplotlib import pyplot
from descartes import PolygonPatch
from shapely.ops import polygonize
from shapely.geometry import Polygon, LineString, Point

from utils import SIZE, BLUE
from utils import plot_coords_line
from utils import plot_line
from utils import set_plot_bounds



#####################
p1 = Polygon([(6,6),(6,7),(7,7),(7,6)])
# p1 = Point(1,1).buffer(1)
p2 = Point(3,3).buffer(1)
p3 = Point(6,6).buffer(1)
p4 = Point(5,12).buffer(1)
p5 = Point(8,12).buffer(1)
square_1 = Polygon([(0,0), (0,8), (8,8), (8,0)])
square_2 = Polygon([(0,10), (0,15), (15,15), (15,10)])

mp1 = MultiPolygon([p2,p3,p4,p5])
mp2 = MultiPolygon([square_1,square_2])

holes = mp2.symmetric_difference(mp1)


#####################################
#             second plot
#  display sample intersection
# ###################################

# setup matplotlib figure that will display the results
fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")

# add a little more space around subplots
fig.subplots_adjust(hspace=.5)

ax = fig.add_subplot(122)

# stores the final split up polygons
new_cut_ply = []

# identify which new polygon we want to keep
for poly in holes:
    # check if new poly is inside original otherwise ignore it

    print "creating new split polygon"
    patch3 = PolygonPatch(poly, fc='purple',
                          alpha=0.5, zorder=2)
    ax.add_patch(patch3)
    # add only polygons that overlap original for export
    new_cut_ply.append(poly)

# patch4 = PolygonPatch(p2, fc='purple',
#                       alpha=0.5, zorder=2)
#
# patch5 = PolygonPatch(p3, fc='purple',
#                       alpha=0.5, zorder=2)
# patch6 = PolygonPatch(p4, fc='purple',
#                       alpha=0.5, zorder=2)
# patch7 = PolygonPatch(p5, fc='purple',
#                       alpha=0.5, zorder=2)
# ax.add_patch(patch4)
# ax.add_patch(patch5)
# ax.add_patch(patch6)
# ax.add_patch(patch7)
# write title of second plot
ax.set_title('sym diff work')

# define the area that plot will fit into
x_range = set_plot_bounds(mp2, 5)['xrange']
y_range = set_plot_bounds(mp2, 5)['yrange']

ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_aspect(1)

pyplot.show()

