#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import Feature, Point, FeatureCollection


# Database Connection Info
db_host = "localhost"
db_user = "postgres"
db_passwd = "air"
db_database = "py_geoan_cb"
db_port = "5432"

conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

cur = conn.cursor()

buffer_query = """select ST_AsGeoJSON(ST_Buffer(wkb_geometry, 100)) as geom, name, country, altitude from geodata.highest_mountains where ogc_fid = 2; """

res = cur.execute(buffer_query)

dbRows = cur.fetchall()

new_geom_collection = []

for each_geom in dbRows:
    # my_feature = Feature(geometry=each_geom)
    geom = each_geom[0]
    name = each_geom[1]
    country = each_geom[2]
    altitude = each_geom[3]


    featureCollection = {"type": "FeatureCollection", "features": []}
    #currentPoiCat = {"featureCollection": featureCollection}


    #geomJson = json.loads(geom)
    item = {
        "type": "Feature",
        "properties":
            {
                "name": name,
                "country": country,
                "altitude": altitude
            },
        "geometry": geom
    }
    featureCollection['features'].append(item)
    #currentPoiCat['featureCollection']['features'].append(item)


# FeatureCollection([my_feature, my_other_feature])
#my_geojson = FeatureCollection(new_geom_collection) # doctest: +ELLIPSIS


# save geojson to file on disk
output_geojson_buf= "../geodata/out_buff_100m.geojson"

def write_geojson():
    fo = open(output_geojson_buf, "w")
    fo.write(json.dumps(featureCollection))
    fo.close()

# run the download and create new file to test, download the json file and compare to current json
write_geojson()

# close cursor
cur.close()

# We are using an InnoDB tables so we need to commit the transaction
conn.commit()

#close connection
conn.close()

