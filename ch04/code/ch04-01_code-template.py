#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
import geojson
from geojson import Feature, Polygon, Point, FeatureCollection


# Database Connection Info
db_host = "localhost"
db_user = "postgres"
db_passwd = "air"
db_database = "py_geoan_cb"
db_port = "5432"

conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

cur = conn.cursor()

buffer_query = """select ST_AsGeoJSON(ST_Transform(ST_Buffer(wkb_geometry, 100),4326)) as geom, name
               from geodata.schools"""

# SELECT ST_Transform(ST_GeomFromText('POLYGON((7))',2249),4326) As wgs_geom

res = cur.execute(buffer_query)

dbRows = cur.fetchall()

new_geom_collection = []

for each_poly in dbRows:
    geom = each_poly[0]
    geoj = geojson.loads(geom)
    myfeat = Feature(geometry=geoj)
    new_geom_collection.append(myfeat)

foo = FeatureCollection(new_geom_collection)

# for each_geom in dbRows:
#     # my_feature = Feature(geometry=each_geom)
#     geom = each_geom[0]
#     name = each_geom[1]
#     country = each_geom[2]
#     altitude = each_geom[3]
#
#     featureCollection = {"type": "FeatureCollection", "features": []}
#     # currentPoiCat = {"featureCollection": featureCollection}
#
#
#     #geomJson = json.loads(geom)
#     item = {
#         "type": "Feature",
#         "properties":
#             {
#                 "name": name,
#                 "country": country,
#                 "altitude": altitude
#             },
#         "geometry": geom
#     }
#     featureCollection['features'].append(item)
#     #currentPoiCat['featureCollection']['features'].append(item)

#new_geom_collection.append(featureCollection)
# FeatureCollection([my_feature, my_other_feature])
# my_geojson = FeatureCollection(new_geom_collection) # doctest: +ELLIPSIS


# save geojson to file on disk
output_geojson_buf = "../geodata/out_buff_100m.geojson"


def write_geojson():
    fo = open(output_geojson_buf, "w")
    fo.write(json.dumps(foo))
    fo.close()

# run the download and create new file to test, download the json file and compare to current json
write_geojson()

# close cursor
cur.close()

#close connection
conn.close()

