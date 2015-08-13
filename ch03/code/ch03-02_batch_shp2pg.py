#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import ogr


def discover_geom_name(ogr_type):
    """

    :param ogr_type: ogr GetGeomType()
    :return: string geometry type name
    """
    return {ogr.wkbUnknown            : "UNKNOWN",
            ogr.wkbPoint              : "POINT",
            ogr.wkbLineString         : "LINESTRING",
            ogr.wkbPolygon            : "POLYGON",
            ogr.wkbMultiPoint         : "MULTIPOINT",
            ogr.wkbMultiLineString    : "MULTILINESTRING",
            ogr.wkbMultiPolygon       : "MULTIPOLYGON",
            ogr.wkbGeometryCollection : "GEOMETRYCOLLECTION",
            ogr.wkbNone               : "NONE",
            ogr.wkbLinearRing         : "LINEARRING"}.get(ogr_type)

def run_shp2pg(input_shp):
    """
    input_shp is full path to shapefile including file ending
    usage:  run_shp2pg('/home/geodata/myshape.shp')
    """

    db_schema = "SCHEMA=geodata"
    db_connection = """PG:host=localhost port=5432
                    user=pluto dbname=py_geoan_cb password=stars"""
    output_format = "PostgreSQL"
    overwrite_option = "OVERWRITE=YES"
    shp_dataset = shp_driver.Open(input_shp)
    layer = shp_dataset.GetLayer(0)
    geometry_type = layer.GetLayerDefn().GetGeomType()
    geometry_name = discover_geom_name(geometry_type)
    print (geometry_name)

    subprocess.call(["ogr2ogr", "-lco", db_schema, "-lco", overwrite_option,
                     "-nlt", geometry_name, "-skipfailures",
                     "-f", output_format, db_connection, input_shp])

# directory full of shapefiles
shapefile_dir = os.path.realpath('../geodata')

# define the ogr spatial driver type
shp_driver = ogr.GetDriverByName('ESRI Shapefile')

# empty list to hold names of all shapefils in directory
shapefile_list = []

for shp_file in os.listdir(shapefile_dir):
    if shp_file.endswith(".shp"):
        # apped join path to file name to outpout "../geodata/myshape.shp"
        full_shapefile_path = os.path.join(shapefile_dir, shp_file)
        shapefile_list.append(full_shapefile_path)

# loop over list of Shapefiles running our import function
for each_shapefile in shapefile_list:
    run_shp2pg(each_shapefile)
    print ("importing Shapefile: " + each_shapefile)
