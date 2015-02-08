### https://github.com/mlaloux/PyShp-as-Fiona--with-geo_interface-

#####  start  ###########################
### http://rexdouglass.com/fast-spatial-joins-in-python-with-a-spatial-index/
###############################
import shapefile
import shapely
# Load the a shapefile of polygons and convert it to shapely polygon objects
polygons_sf = shapefile.Reader("C:/PolygonShapeFile.shp")
polygon_shapes = polygons_sf.iterShapes()
polygon_points = [q.points for q in polygon_shapes]
from shapely.geometry import Polygon

polygons = [Polygon(q) for q in polygon_points]

#Load the a shapefile of points and convert it to shapely point objects
points_sf = shapefile.Reader("C:/PointShapeFile.shp")
point_shapes = points_sf.iterShapes()
from shapely.geometry import Point

point_coords = [q.points[0] for q in point_shapes]
points = [Point(q.points[0]) for q in point_shapes]

#Build a spatial index based on the bounding boxes of the polygons
from rtree import index

idx = index.Index()
count = -1
for q in polygon_shapes:
    count += 1
    idx.insert(count, q.bbox)

#Assign one or more matching polygons to each point
matches = []
for i in range(len(points)):  #Iterate through each point
    temp = None
    print "Point ", i
    #Iterate only through the bounding boxes which contain the point
    for j in idx.intersection(point_coords[i]):
        #Verify that point is within the polygon itself not just the bounding box
        if points[i].within(polygons[j]):
            print "Match found! ", j
            temp = j
            break
    matches.append(temp)  #Either the first match found, or None for no matches


######   END   ##########################
### http://rexdouglass.com/fast-spatial-joins-in-python-with-a-spatial-index/
###############################

######################  sape

#
#
# eroded = dilated.buffer(-0.3)
#
# # GeoJSON-like data works as well
#
# polygon = eroded.__geo_interface__
# >>> geo['type']
# 'Polygon'
# >>> geo['coordinates'][0][:2]
# ((0.50502525316941682, 0.78786796564403572), (0.5247963548222736, 0.8096820147509064))
# patch2b = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
# ax.add_patch(patch2b)


###########

#first feature of the shapefile
feature = shape.shapeRecords()[0]
first = feature.shape.__geo_interface__
print first  # (GeoJSON format)
# {'type': 'LineString', 'coordinates': ((0.0, 0.0), (25.0, 10.0), (50.0, 50.0))}


shapelytogeojson = shapely.geometry.mapping
geoj = shapelytogeojson(shapelygeom)

in_shapefile = shapefile.Reader(r'..\geodata\roads_london.shp')
clip_project_area = shapefile.Reader(r'..\geodata\clip_area.shp')
out_new_shapefile = shapefile.Writer(in_shapefile.shapeType)

out_new_shapefile.fields = list(in_shapefile.fields)
out_new_shapefile.records.extend(in_shapefile.records())

for s in in_shapefile.iterShapes():
    in_geom = s.shapeType()

clip_area = shapely.wkt.loads(geometry.ExportToWkt())

new_clipped_area = roads.intersection(clip_area)

# #########################
# ########################
import json
from shapely.geometry import shape

f = open('wijken.json', 'r')
js = json.load(f)
f.close()

for f in js['features']:
    s = shape(f['geometry'])

# #########################
# #########################
# http://gis.stackexchange.com/questions/52705/how-to-write-shapely-geometries-to-shapefiles
# DEFINE/COPY-PASTE THE SHAPELY-PYSHP CONVERSION FUNCTION
def shapely_to_pyshp(shapelygeom):
    # first convert shapely to geojson
    try:
        shapelytogeojson = shapely.geometry.mapping
    except:
        import shapely.geometry

        shapelytogeojson = shapely.geometry.mapping
    geoj = shapelytogeojson(shapelygeom)
    # create empty pyshp shape
    record = shapefile._Shape()
    # set shapetype
    if geoj["type"] == "Null":
        pyshptype = 0
    elif geoj["type"] == "Point":
        pyshptype = 1
    elif geoj["type"] == "LineString":
        pyshptype = 3
    elif geoj["type"] == "Polygon":
        pyshptype = 5
    elif geoj["type"] == "MultiPoint":
        pyshptype = 8
    elif geoj["type"] == "MultiLineString":
        pyshptype = 3
    elif geoj["type"] == "MultiPolygon":
        pyshptype = 5
    record.shapeType = pyshptype
    # set points and parts
    if geoj["type"] == "Point":
        record.points = geoj["coordinates"]
        record.parts = [0]
    elif geoj["type"] in ("MultiPoint", "Linestring"):
        record.points = geoj["coordinates"]
        record.parts = [0]
    elif geoj["type"] in ("Polygon"):
        record.points = geoj["coordinates"][0]
        record.parts = [0]
    elif geoj["type"] in ("MultiPolygon", "MultiLineString"):
        index = 0
        points = []
        parts = []
        for eachmulti in geoj["coordinates"]:
            points.extend(eachmulti[0])
            parts.append(index)
            index += len(eachmulti[0])
        record.points = points
        record.parts = parts
    return record

# WRITE TO SHAPEFILE USING PYSHP
shapewriter = shapefile.Writer()
shapewriter.field("field1")
# step1: convert shapely to pyshp using the function above
converted_shape = shapely_to_pyshp(TEST_SHAPELYSHAPE)
# step2: tell the writer to add the converted shape
shapewriter._shapes.append(converted_shape)
# add a list of attributes to go along with the shape
shapewriter.record(["empty record"])
# save it
shapewriter.save("test_shapelytopyshp.shp")

# ######################
# ######    end    ########
# #####################

# ########## code from book python geospatial development v2 page 138 ##########
# ## read in shapefile edit geom with shapely write to shapefile  ##############
# ##############################################################################

import os, os.path, shutil
from osgeo import ogr
import shapely.wkt
# Load the thai and myanmar polygons from the world borders
# dataset.
shapefile = ogr.Open("TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

roads = None
clip_area = None

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    if feature.GetField("ISO2") == "TH":
        geometry = feature.GetGeometryRef()
        roads = shapely.wkt.loads(geometry.ExportToWkt())
    elif feature.GetField("ISO2") == "MM":
        geometry = feature.GetGeometryRef()
        clip_area = shapely.wkt.loads(geometry.ExportToWkt())
# Calculate the common border.
new_clipped_area = roads.intersection(clip_area)

# Save the common border into a new shapefile.
if os.path.exists("common-border"):
    shutil.rmtree("common-border")
os.mkdir("common-border")
spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')
driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("common-border", "border.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer", spatialReference)
wkt = shapely.wkt.dumps(new_clipped_area)

feature = ogr.Feature(dstLayer.GetLayerDefn())
feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
dstLayer.CreateFeature(feature)
feature.Destroy()
dstFile.Destroy()

###########################################################################



import fiona
from shapely.geometry import shape, mapping
import rtree

bufSHP = 'data/h1_buf.shp'
intSHP = 'data/h1_buf_int_ct.shp'
ctSHP = 'data/nyct2010.shp'

with fiona.open(bufSHP, 'r') as layer1:
    with fiona.open(ctSHP, 'r') as layer2:
        # We copy schema and add the  new property for the new resulting shp
        schema = layer2.schema.copy()
        schema['properties']['uid'] = 'int:10'
        # We open a first empty shp to write new content from both others shp
        with fiona.open(intSHP, 'w', 'ESRI Shapefile', schema) as layer3:
            index = rtree.index.Index()
            for feat1 in layer1:
                fid = int(feat1['id'])
                geom1 = shape(feat1['geometry'])
                index.insert(fid, geom1.bounds)

            for feat2 in layer2:
                geom2 = shape(feat2['geometry'])
                for fid in list(index.intersection(geom2.bounds)):
                    if fid != int(feat2['id']):
                        feat1 = layer1[fid]
                        geom1 = shape(feat1['geometry'])
                        if geom1.intersects(geom2):
                            # We take attributes from ctSHP
                            props = feat2['properties']
                            # Then append the uid attribute we want from the other shp
                            props['uid'] = feat1['properties']['uid']
                            # Add the content to the right schema in the new shp
                            layer3.write({
                                'properties': props,
                                'geometry': mapping(geom1.intersection(geom2))
                            })

#first feature of the shapefile
feature = in_shapefile.shapeRecords()[0]
first = feature.shape.__geo_interface__
print first  # (GeoJSON format)
# {'type': 'LineString', 'coordinates': ((0.0, 0.0), (25.0, 10.0), (50.0, 50.0))}


# pyshp
import shapefile

shape = shapefile.Reader("my_shapefile.shp")
#first feature of the shapefile
feature = shape.shapeRecords()[0]
first = feature.shape.__geo_interface__
print first  # (GeoJSON format)
# {'type': 'LineString', 'coordinates': ((0.0, 0.0), (25.0, 10.0), (50.0, 50.0))}

# ogr
from osgeo import ogr

file = ogr.Open("my_shapefile.shp")
shape = file.GetLayer(0)
#first feature of the shapefile
feature = shape.GetFeature(0)
first = feature.ExportToJson()
print first  # (GeoJSON format)

from shapely.geometry import shape

shp_geom = shape(first['geometry'])  # or shp_geom = shape(first) with PyShp)
print shp_geom
# LINESTRING (0 0, 25 10, 50 50)
print type(shp_geom)
# <class 'shapely.geometry.linestring.LineString'>

from osgeo import ogr
from shapely.wkb import loads
from shapely.geometry import *
# first layer, a polygon shapefile
project_area = Polygon()

# open shapefile
source1 = ogr.Open("test1.shp")
layer1 = source1.GetLayer()
# combination of all the geometries of the layer in a single shapely object
for element in layer1:
    geom = loads(element.GetGeometryRef().ExportToWkb())
    project_area = project_area.union(geom)

# second layer, a polygon shapefile
roads = Polygon()
source2 = ogr.Open("test2.shp")
layer2 = source2.GetLayer()
for element in layer2:
    geom = loads(element.GetGeometryRef().ExportToWkb())
    roads = roads.union(geom)

# intersection between the two layers
print project_area.intersection(roads).wkt



#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyshp
import shapefile
import shapely
import pprint
import geojson

#from shapely import geometry
#from shapely.geometry import mapping, shape

# clip_area_shp = shapefile.Reader(r"..\geodata\clip_area.shp")
# roads_london_shp = shapefile.Reader(r"..\geodata\roads_london.shp")
# #f = roads_london.sh
#
# clip_area_shply = None
# roads_shply = None
#
# for geom in clip_area_shp.iterRecords():
#     clip_area_shply = shapely.wkt.loads(geom)
#
# for geom in roads_london_shp.iterRecords():
#     roads_shply = shapely.wkt.loads(geom)
#
# clipped_roads_shply = roads_shply.intersection(clip_area_shply)
#
# # export shapely result to shapefile
#
# clipped_roads_shp = shapefile.Writer()
# clipped_roads_shp.save(r'..\geodata\clipped_roads.shp')

####  start

### https://github.com/mlaloux/PyShp-as-Fiona--with-geo_interface-
###
from shapely.geometry import shape


def records(filename):
    # generator
    reader = shapefile.Reader(filename)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    for sr in reader.shapeRecords():
        geom = sr.shape.__geo_interface__
        atr = dict(zip(field_names, sr.record))
        yield dict(geometry=geom,properties=atr)




# polygon = eroded.__geo_interface__
#clip_area = records(r'..\geodata\clip_area_3857.shp')
road_lines = records(r'..\geodata\roads_london_3857.shp')

#pprint.pprint(clip_area.next())
pprint.pprint(road_lines.next())
# pprint.pprint(clip_area.next()['geometry']['coordinates'])
# print a.next()['properties']['DIP']


# a = records('point.shp')
# print shape( a.next()['geometry'])
####  end

###########################################################
#########################################################
####    working code

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


# http://stackoverflow.com/questions/25374459/find-holes-in-a-union-of-rectangles

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

for feature in roads_features:
    roads_london_shply = asShape(feature.shape.__geo_interface__)
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
#patch2 = PolygonPatch(clip_feature_shply, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)

# add polygon to plot
#ax.add_patch(patch2)

# run the intersection
#intersect_line = line.intersection(polygon)

# plot the lines and the line vertex to plot
plot_lines(ax, roads_shply_list, color='#3C3F41')
# plot_coords_lines(ax, intersect_line, color='#3C3F41')

# write title of second plot
ax.set_title('line intersects polygon')

# define the area that plot will fit into
xrange = [clip_feature_shply.bounds[0] - 100.0, clip_feature_shply.bounds[2] + 100.0]
yrange = [clip_feature_shply.bounds[1] - 100.0, clip_feature_shply.bounds[3] + 200.0]
import math
ax.set_xlim(xrange)
# ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_xticks(range(int(round(xrange))) + [int(xrange[-1.0])])

ax.set_ylim(yrange)
#ax.set_yticks(range(int(round(*yrange))) + [int(yrange[-1.0])])
ax.set_aspect(1)

#
# ax = fig.add_subplot(122)
#
# # create matplotlib patch
# patch2 = PolygonPatch(polygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=1)
#
# # add polygon to plot
# ax.add_patch(patch2)
#
# # run the intersection
# intersect_line = line.intersection(polygon)
#
# # plot the lines and the line vertex to plot
# plot_lines(ax, intersect_line, color='#3C3F41')
# plot_coords_lines(ax, intersect_line, color='#3C3F41')
#
# # write title of second plot
# ax.set_title('line intersects polygon')
#
# # define the area that plot will fit into
# xrange = [-1, 4]
# yrange = [-1, 3]
# ax.set_xlim(*xrange)
# ax.set_xticks(range(*xrange) + [xrange[-1]])
# ax.set_ylim(*yrange)
# ax.set_yticks(range(*yrange) + [yrange[-1]])
# ax.set_aspect(1)
# draw the diagram and open it on screen
pyplot.show()

