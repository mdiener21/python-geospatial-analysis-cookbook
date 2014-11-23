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

# generate points where lines intesect

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

# postgis function to create a fishnet grid
# http://gis.stackexchange.com/questions/16374/how-to-create-a-regular-polygon-grid-in-postgis
create_function_query = """
CREATE OR REPLACE FUNCTION ST_CreateFishnet(
        nrow integer, ncol integer,
        xsize float8, ysize float8,
        x0 float8 DEFAULT 0, y0 float8 DEFAULT 0,
        OUT "row" integer, OUT col integer,
        OUT geom geometry)
    RETURNS SETOF record AS
$$
SELECT i + 1 AS row, j + 1 AS col, ST_Translate(cell, j * $3 + $5, i * $4 + $6) AS geom
FROM generate_series(0, $1 - 1) AS i,
     generate_series(0, $2 - 1) AS j,
(
SELECT ('POLYGON((0 0, 0 '||$4||', '||$3||' '||$4||', '||$3||' 0,0 0))')::geometry AS cell
) AS foo;
$$ LANGUAGE sql IMMUTABLE STRICT;
"""