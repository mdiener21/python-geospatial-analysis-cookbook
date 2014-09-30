#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os

def run_shp2pg(input_shp):
	"""
	input_shp is full path to shapefile including file ending
	usage:  run_shp2pg('/home/geodata/myshape.shp')
	"""

	db_schema = "SCHEMA=geodata"
	db_connection = "PG:host=localhost port=5432 \

		user=postgres dbname=py_cb password=air"
	output_format = "PostgreSQL"
	geom_type = "MULTILINESTRING"
	#input_shp = "/home/mdiener/geodata/bikeways.shp"
	overwrite_option = "OVERWRITE=YES"
	subprocess.call(["ogr2ogr","-lco", db_schema, "-lco", overwrite_option, \
		"-nlt", geom_type, "-f", output_format, db_connection,  input_shp])

shapefile_dir = "/home/mdiener/geodata"

shapefile_list = []

for file in os.listdir(shapefile_dir):
    if file.endswith(".shp"):
        # apped join path to file name to outpout "/home/mdiener/geodata/myshape.shp"
        full_shapefile_path = os.path.join(shapefile_dir, file)
        shapefile_list.append(full_shapefile_path)

# loop over list of Shapefiles running our import function
for each_shapefile in shapefile_list:
	run_shp2pg(each_shapefile)
	print ("importing Shapefile: " + each_shapefile)