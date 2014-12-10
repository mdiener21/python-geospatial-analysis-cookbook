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


split_lines_query = """
                    CREATE TABLE
                        geodata.split_roads
                    AS SELECT
                        (ST_Dump(ST_Node(ST_Collect(geom)))).geom AS GEOM
                    FROM
                        geodata.van_raw_roads;
                     """
cur.execute("ALTER TABLE geodata.temp_roads ADD COLUMN id serial;")
cur.execute("ALTER TABLE geodata.temp_roads ADD CONSTRAINT temp_pkey PRIMARY KEY (id);")

# create table geodata.temp_roads as select (st_dump(st_node(st_collect(geom)))).geom as geom from geodata.van_raw_roads;



