#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

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

# the PostGIS buffer query
valid_query = """SELECT
                   ogc_fid, 
                   ST_IsValidDetail(wkb_geometry)
                FROM 
                   geodata.lines
                WHERE NOT
                   ST_IsValid(wkb_geometry);
                """

# execute the query
cur.execute(valid_query)

# return all the rows, we expect more than one
validity_results = cur.fetchall()

print validity_results

# close cursor
cur.close()

# close connection
conn.close()
