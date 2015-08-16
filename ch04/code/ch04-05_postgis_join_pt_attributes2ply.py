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
conn = psycopg2.connect(host=db_host, user=db_user,
    port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()


# assign polygon attributes from points
spatial_join = """  UPDATE geodata.pebble_beach_greens AS g
                        SET
                           name = h.name
                        FROM
                           geodata.pebble_beach_hole_num AS h
                        WHERE
                           ST_Contains(g.geom, h.geom);
                     """
cur.execute(spatial_join)
conn.commit()

# close cursor
cur.close()

# close connection
conn.close()
