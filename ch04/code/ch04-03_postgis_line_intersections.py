#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection


# Database Connection Info
db_host = "localhost"
db_user = "pluto"
db_passwd = "stars"
db_database = "py_test"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user,
    port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

# drop table if exists
# cur.execute("DROP TABLE IF EXISTS geodata.split_roads;")

# split lines at intesections query
split_lines_query = """ CREATE TABLE geodata.split_roads
    AS SELECT(ST_Dump(ST_Node
        (ST_Collect(wkb_geometry)))).geom AS geom
    FROM geodata.lines;
                     """
cur.execute(split_lines_query)
conn.commit()

cur.execute("ALTER TABLE geodata.split_roads ADD COLUMN id serial;")
cur.execute("ALTER TABLE geodata.split_roads ADD CONSTRAINT split_roads_pkey PRIMARY KEY (id);")

# close cursor
cur.close()

# close connection
conn.close()
