#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt
import shapely as Shapely
import shapefile

from shapely.geometry import mapping

GM = (sqrt(5)-1.0)/2.0
W = 8.0
H = W*GM
SIZE = (W, H)

BLUE = '#6699cc'
# GRAY = '#999999'
GRAY = '#00b700'

### HOW TO SAVE SHAPEFILE FROM SHAPELY GEOMETRY USING PYSHP

# IMPORT STUFF
import shapefile
import shapely.geometry

# CREATE YOUR SHAPELY TEST INPUT
TEST_SHAPELYSHAPE = shapely.geometry.Polygon([(133,822),(422,644),(223,445),(921,154)])

#########################################################
################## END OF USER INPUT ####################
#########################################################

# DEFINE/COPY-PASTE THE SHAPELY-PYSHP CONVERSION FUNCTION
def shapely_to_pyshp(shapelygeom):
    # first convert shapely to geojson
    try:
        shapelytogeojson = Shapely.geometry.mapping
    except:
        import Shapely.geometry
        shapelytogeojson = Shapely.geometry.mapping
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
    elif geoj["type"] in ("MultiPoint","Linestring"):
        record.points = geoj["coordinates"]
        record.parts = [0]
    elif geoj["type"] in ("Polygon"):
        record.points = geoj["coordinates"][0]
        record.parts = [0]
    elif geoj["type"] in ("MultiPolygon","MultiLineString"):
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