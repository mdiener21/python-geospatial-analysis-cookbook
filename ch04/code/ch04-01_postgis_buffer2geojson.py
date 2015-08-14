#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection


# Database Connection Info
db_host = "localhost"
db_user = "pluto"
db_passwd = "stars"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, 
	port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

# the PostGIS buffer query
buffer_query = """SELECT ST_AsGeoJSON(ST_Transform(
			ST_Buffer(wkb_geometry, 100,'quad_segs=8'),4326)) 
			AS geom, name
            FROM geodata.schools"""

# execute the query
cur.execute(buffer_query)

# return all the rows, we expect more than one
dbRows = cur.fetchall()

# an empty list to hold each feature of our feature collection
new_geom_collection = []

# loop through each row in result query set and add to my feature collection
# assign name field to the GeoJSON properties
for each_poly in dbRows:
    geom = each_poly[0]
    name = each_poly[1]
    geoj_geom = loads(geom)
    myfeat = Feature(geometry=geoj_geom, properties={'name': name})
    new_geom_collection.append(myfeat)

# use the geojson module to create the final Feature Collection of features created from for loop above
my_geojson = FeatureCollection(new_geom_collection)

# define the output folder and GeoJSon file name
output_geojson_buf = "../geodata/out_buff_100m.geojson"


# save geojson to a file in our geodata folder
def write_geojson():
    fo = open(output_geojson_buf, "w")
    fo.write(json.dumps(my_geojson))
    fo.close()

# run the write function to actually create the GeoJSON file
write_geojson()

# close cursor
cur.close()

# close connection
conn.close()
