#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import subprocess
import os

# folder to hold output Shapefiles
destination_dir = os.path.realpath('../geodata/temp')

# list of postGIS tables
postgis_tables_list = ["bikeways", "highest_mountains"]

# database connection parameters
db_connection = """PG:host=localhost port=5432 user=pluto
        dbname=py_geoan_cb password=stars active_schema=geodata"""

output_format = "ESRI Shapefile"

# check if destination directory exists
if not os.path.isdir(destination_dir):
    os.mkdir(destination_dir)
    for table in postgis_tables_list:
        subprocess.call(["ogr2ogr", "-f", output_format, destination_dir,
                         db_connection, table])
        print("running ogr2ogr on table: " + table)
else:
    print("oh no your destination directory " + destination_dir +
          " already exist please remove it then run again")

# commandline call without using python will look like this
# ogr2ogr -f "ESRI Shapefile" mydatadump \
# PG:"host=myhost user=myloginname dbname=mydbname password=mypassword" neighborhood parcels
