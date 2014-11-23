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

buffer_bike_query = """ SELECT ST_Buffer(geom.a, 100) from geodata.bikepaths; """
# ST_Within returns a True or False
is_inside_query = """ CREATE TABLE geodata.points_inside as
                      SELECT
                          ST_WITHIN(point_geom, polygon_geom)
                      FROM polygon_layer;
                  """


intersection_query = """
                        CREATE TABLE network_intersections as
                        SELECT
                            ST_Intersection(a.geom, b.geom),
                            Count(Distinct a.gid)
                        FROM
                            geodata.roads as a,
                            geodata.roads as b
                        WHERE
                            ST_Touches(a.geom, b.geom)
                            AND a.gid != b.gid
                        GROUP BY
                            ST_Intersection(a.geom, b.geom)
                        ;
                    """

# execute the query
cur.execute(is_inside_query)

# return all the rows, we expect more than one
dbRows = cur.fetchall()

if value is True:
    # the point is inside our polygon
    # export these points to GeoJSON
