#!/usr/bin/env python
# -*- coding: utf-8 -*-

# convert / import osm xml .osm file into a Shapefile
import subprocess
import os
import shutil

# specify output format
output_format = "ESRI Shapefile"

# complete path to input OSM xml file .osm
input_osm = '../geodata/OSM_san_francisco_westbluff.osm'

# Windows users can uncomment these two lines if needed
# ogr2ogr = r"c:/OSGeo4W/bin/ogr2ogr.exe"
# ogr_info = r"c:/OSGeo4W/bin/ogrinfo.exe"

# view what geometry types are available in our OSM file
subprocess.call([ogr_info, input_osm])

destination_dir = os.path.realpath('../geodata/temp')

if os.path.isdir(destination_dir):
    # remove output folder if it exists
    shutil.rmtree(destination_dir)
    print("removing existing directory : " + destination_dir)
    # create new output folder
    os.mkdir(destination_dir)
    print("creating new directory : " + destination_dir)

    # list of geometry types to convert to Shapefile
    geom_types = ["lines", "points", "multilinestrings", "multipolygons"]

    # create a new Shapefile for each geometry type
    for g_type in geom_types:

        subprocess.call([ogr2ogr,
               "-skipfailures", "-f", output_format,
                 destination_dir, input_osm,
                 "layer", g_type,
                 "--config","OSM_USE_CUSTOM_INDEXING", "NO"])
        print("done creating " + g_type)

# if you like to export to SPATIALITE from .osm
# subprocess.call([ogr2ogr, "-skipfailures", "-f",
#         "SQLITE", "-dsco", "SPATIALITE=YES",
#         "my2.sqlite", input_osm])


