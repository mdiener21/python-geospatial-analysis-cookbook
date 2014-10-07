#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

# database options
db_schema = "SCHEMA=geodata"
overwrite_option = "OVERWRITE=YES"
geom_type = "MULTILINESTRING"
output_format = "PostgreSQL"

# database connection string
db_connection = "PG:host=localhost port=5432 \
	user=postgres dbname=py_geoan_cb password=secret"

# input shapefile
input_shp = "/home/mdiener/geodata/bikeways.shp"

# call ogr2ogr from python
subprocess.call(["ogr2ogr","-lco", db_schema, "-lco", overwrite_option, \
	"-nlt", geom_type, "-f", output_format, db_connection,  input_shp])
	
# -lco is the layer creation option
# -f is output format
# -nlt new layer type

