#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection


# Database Connection Info
db_host = "localhost"
db_user = "postgres"
db_passwd = "air"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

# select all schools that are within 100m from a bike path

# buffer all bike paths

# >>> SQL = "INSERT INTO authors (name) VALUES (%s);" # Note: no quotes
# >>> data = ("O'Reilly", )
# >>> cur.execute(SQL, data) # Note: no % oper

# a single query
# select all schools that are within 100m from bike path using ST_DWITHIN(geom a, geom b, distance)
# select s.name, b.name, b.type from geodata.schools as s, geodata.bikeways as b
# 	where st_Dwithin(s.wkb_geometry, b.wkb_geometry,100)
# 	order by type desc;

# buffer_bike_query = """ SELECT ST_Buffer(wkb_geometry, 100) as bike_buf_geom from geodata.bikeways; """
cur.execute("Drop table if exists geodata.bikepath_100m_buff;")

new_bike_buff_100m = """ CREATE TABLE geodata.bikepath_100m_buff as
                      SELECT
                          name, ST_Buffer(wkb_geometry, 100) as geom
                      FROM
                          geodata.bikeways;

                  """

cur.execute(new_bike_buff_100m)

conn.commit()

is_inside_query = """ SELECT s.name as name, ST_AsGeoJSON(ST_Transform(s.wkb_geometry,4326)) as geom
                      FROM
                          geodata.schools AS s,
                          geodata.bikepath_100m_buff as b
                      WHERE
                          ST_WITHIN(s.wkb_geometry, b.geom);

                  """


# execute the query
cur.execute(is_inside_query)

# return all the rows, we expect more than one
dbRows = cur.fetchall()

# an empty list to hold each feature of our feature collection
new_geom_collection = []

def export2geojson(query_result):
    # loop through each row in result query set and add to my feature collection
    # assign name field to the GeoJSON properties
    for row in dbRows:
        name = row[0]
        geom = row[1]
        geoj_geom = loads(geom)
        myfeat = Feature(geometry=geoj_geom, properties={'name': name})
        new_geom_collection.append(myfeat)

    # use the geojson module to create the final Feature Collection of features created from for loop above
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

export2geojson(dbRows)

# # ST_Within returns a True or False
# is_inside_query = """ CREATE TABLE geodata.points_inside as
#                       SELECT
#                           name
#                       FROM
#                           geodata.polygon_layer
#                       WHERE
#                           ST_DWITHIN(point_geom, polygon_geom,100);
#
#                   """
#
# # now view data using qgis to see this result
#
# intersection_query = """
#                         CREATE TABLE network_intersections as
#                         SELECT
#                             ST_Intersection(a.geom, b.geom),
#                             Count(Distinct a.gid)
#                         FROM
#                             geodata.roads as a,
#                             geodata.roads as b
#                         WHERE
#                             ST_Touches(a.geom, b.geom)
#                             AND a.gid != b.gid
#                         GROUP BY
#                             ST_Intersection(a.geom, b.geom)
#                         ;
#                     """
