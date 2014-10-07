#!/usr/bin/env python
# -*- coding: utf-8 -*-

# convert / import osm xml .osm file into a Shapefile
import subprocess

# specify output format
output_format = "ESRI Shapefile"

# complete path to input OSM xml file .osm
input_osm = '../geodata/OSM_san_francisco_westbluff.osm'

# path to a new folder to hold the Shapefiles (must not exist)
output_shp_folder = '../geodata/shp'

# Windows users can uncomment these two lines if needed
# ogr2ogr = r"c:/OSGeo4W/bin/ogr2ogr.exe"
# ogr_info = r"c:/OSGeo4W/bin/ogrinfo.exe"

# view what geometry types are available in our OSM file
subprocess.call([ogr_info, input_osm])

# call the subprocess function which fires ogr2ogr command line
subprocess.call([ogr2ogr, "-f", output_format, output_shp_folder, input_osm])