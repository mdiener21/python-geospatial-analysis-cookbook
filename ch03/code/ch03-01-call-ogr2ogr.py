#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

db_schema = "SCHEMA=geodata"
pg_epsg = "900913"

db_connection = "PG:host=localhost port=5432 \
	user=postgres dbname=py_cb password=secret"

output_format = "PostgreSQL"
geom_type = "MULTILINESTRING"
input_shp = "/home/mdiener/geodata/bikeways.shp"
overwrite_option = "OVERWRITE=YES"

subprocess.call(["ogr2ogr","-lco", db_schema, "-lco", overwrite_option, \
	"-nlt", geom_type, "-f", output_format, db_connection,  input_shp])
	
# -lco is the layer creation option
# -f is output format
# -nlt new layer type

