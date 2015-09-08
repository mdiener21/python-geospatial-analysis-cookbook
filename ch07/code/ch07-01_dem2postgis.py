#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import psycopg2

db_host = "localhost"
db_user = "pluto"
db_passwd = "secret"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user,
                        port=db_port, password=db_passwd,
                        database=db_database)

# create a cursor
cur = conn.cursor()

# input USGS ASCII DEM (and CDED)
input_dem = "../geodata/dem_3857.dem"

# create an sql file for loading into the PostGIS database raster
# command line with options
# -c create new table
# -I option will create a spatial GiST index on the raster column
# -C will apply raster constraints
# -M vacuum analyse the raster table


command = 'raster2pgsql -c -C -I -M ' + input_dem + ' geodata.dem_3857'

# write the output to a file
temp_sql_file = "temp_sql.sql"

# open, create new file to write sql statements into
with open(temp_sql_file, 'wb') as f:
    try:
        result = subprocess.call(command, stdout=f, shell=True)
        if result != 0:
            raise Exception('error code %d' % result)

    except Exception as e:
        print e

# open the file full of insert statements created by raster2pgsql
with open(temp_sql_file, 'r') as r:
    # run through and execute each line inside the temp sql file
    for sql_insert in r:
        cur.execute(sql_insert)

print "please open QGIS >= 2.8.x and view your loaded DEM data"