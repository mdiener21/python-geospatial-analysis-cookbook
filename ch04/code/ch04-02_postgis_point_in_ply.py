#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import psycopg2
from geojson import loads, Feature, FeatureCollection


# Database Connection Info
db_host = "localhost"
db_user = "pluto"
db_passwd = "stars"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

# uncomment if needed
# cur.execute("Drop table if exists geodata.bikepath_100m_buff;")

# query to create a new polygon 100m around the bikepath
new_bike_buff_100m = """ CREATE TABLE geodata.bikepath_100m_buff 
    AS SELECT name, 
    ST_Buffer(wkb_geometry, 100) AS geom
    FROM geodata.bikeways; """
# run the query
cur.execute(new_bike_buff_100m)

# commit query to database
conn.commit()

# query to select schools inside the polygon and output geojson
is_inside_query = """ SELECT s.name AS name, 
    ST_AsGeoJSON(ST_Transform(s.wkb_geometry,4326)) AS geom
    FROM geodata.schools AS s,
    geodata.bikepath_100m_buff AS bp
        WHERE ST_WITHIN(s.wkb_geometry, bp.geom); """

# execute the query
cur.execute(is_inside_query)

# return all the rows, we expect more than one
db_rows = cur.fetchall()

# an empty list to hold each feature of our feature collection
new_geom_collection = []


def export2geojson(query_result):
    """
    loop through each row in result query set and add to my feature collection
    assign name field to the GeoJSON properties
    :param query_result: pg query set of geometries
    :return: new geojson file
    """

    for row in db_rows:
        name = row[0]
        geom = row[1]
        geoj_geom = loads(geom)
        myfeat = Feature(geometry=geoj_geom, 
                    properties={'name': name})
        new_geom_collection.append(myfeat)

    # use the geojson module to create the final Feature
    # Collection of features created from for loop above
    my_geojson = FeatureCollection(new_geom_collection)

    # define the output folder and GeoJSon file name
    output_geojson_buf = "../geodata/out_schools_in_100m.geojson"

    # save geojson to a file in our geodata folder
    def write_geojson():
        fo = open(output_geojson_buf, "w")
        fo.write(json.dumps(my_geojson))
        fo.close()

    # run the write function to actually create the GeoJSON file
    write_geojson()


export2geojson(db_rows)