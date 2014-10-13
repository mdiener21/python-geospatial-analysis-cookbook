#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import subprocess
import os

# folder to hold output Shapefiles
destination_dir = os.path.dirname(os.path.realpath('..\geodata')) + "\\geodata\\temp"

# list of postGIS tables
postgis_tables_list = ["bikeways", "sportanl"]

# database connection parameters
db_schema = "active_schema=geodata"
db_connection = "PG:host=localhost port=5432 user=postgres \
        dbname=py_geoan_cb password=air " + db_schema

output_format = "ESRI Shapefile"

# check if destination directory exists
if os.path.isdir(destination_dir):
    for table in postgis_tables_list:
        subprocess.call(["ogr2ogr", "-f", output_format, destination_dir,
                         db_connection, table])
        print("running ogr2ogr on table: " + table)
else:
    print("oh no your destination directory" + destination_dir + "does not exist please create it then run again")

# commandline call without using python will look like this
# ogr2ogr -f "ESRI Shapefile" mydatadump \
# PG:"host=myhost user=myloginname dbname=mydbname password=mypassword" neighborhood parcels

