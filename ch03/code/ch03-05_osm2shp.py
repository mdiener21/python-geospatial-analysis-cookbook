#!/usr/bin/env python
# -*- coding: utf-8 -*-


# convert / import osm xml .osm file into a Shapefile
import subprocess

# specify output format
output_format = "ESRI Shapefile"

# complete path to input OSM xml file .osm
input_osm = '../geodata/map.osm'


# complete path to input Shapefile
output_shp = '../geodata/shp'

ogr2ogr = r"c:/OSGeo4W/bin/ogr2ogr.exe"
ogr_info = r"c:/OSGeo4W/bin/ogrinfo.exe"

#option_point = "SHPT=POINT"
option_line = "SHPT=ARC"
# SHPT=POINT/ARC/POLYGON/MULTIPOINT/POINTZ/ARCZ/POLYGONZ/MULTIPOINTZ.
#multipolygons = "multipolygons"

subprocess.call([ogr_info, input_osm])

# call the subprocess function which fires ogr2ogr command line
#subprocess.call([ogr2ogr, "-lco", option_line, "-f", output_format, output_shp, input_osm])

subprocess.call([ogr2ogr, "-f", output_format, output_shp, input_osm, 'waypoints'])
#subprocess.call([ogr2ogr, output_shp, multipolygons])
#ogr2ogr cite_soleil_buildings cite_soleil_buildings.osm multipolygons

###
#\ch03\code>c:\OSGeo4W\bin\ogr2ogr.exe ..\geodata\4foo ..\geodata\map.osm multipolygons
# 1: points (Point)
# 2: lines (Line String)
# 3: multilinestrings (Multi Line String)
# 4: multipolygons (Multi Polygon)
# 5: other_relations (Geometry Collection)
