#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############
# code to import osm street data direct into PG postgis
###############

import subprocess
# database options
db_schema = "SCHEMA=geodata"
overwrite_option = "OVERWRITE=YES"
geom_type = "LINESTRING"
output_format = "PostgreSQL"

# database connection string
db_connection = "PG:host=localhost port=5432 \
	user=postgres dbname=py_geoan_cb password=air"

# input shapefile
input_osm = "../geodata/vancouver-osm-data.osm"

# call ogr2ogr from python
subprocess.call(["ogr2ogr","-lco", db_schema, "-lco", overwrite_option,
	"-nlt", geom_type, "-f", output_format, db_connection,  input_osm, 'lines'])

##############
# END
###############


# source http://blog.mathieu-leplatre.info/use-postgis-topologies-to-clean-up-road-networks.html
split_query = """SELECT r.lib_off, r.ogc_fid, e.geom
FROM roads_topo.edge e,
     roads_topo.relation rel,
     roads r
WHERE e.edge_id = rel.element_id
  AND rel.topogeo_id = (r.topo_geom).id"""

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


# ST_Within returns a True or False
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

# Discover if a point is inside a polygon using PostGIS

# CREATE TABLE test_points as
# SELECT
#     ST_Intersection(a.geom, b.geom),
#     Count(Distinct a.gid)
# FROM
#     roads as a,
#     roads as b
# WHERE
#     ST_Touches(a.geom, b.geom)
#     AND a.gid != b.gid
# GROUP BY
#     ST_Intersection(a.geom, b.geom)



# source  http://blog.mathieu-leplatre.info/drape-lines-on-a-dem-with-postgis.html

query = """
 WITH line AS
    -- From an arbitrary line
    (SELECT 'SRID=32632;LINESTRING (348595 4889225,352577 4887465,354784 4883841)'::geometry AS geom),
  cells AS
    -- Get DEM elevation for each intersected cell
    (SELECT ST_Centroid((ST_Intersection(mnt.rast, line.geom)).geom) AS geom,
    (ST_Intersection(mnt.rast, line.geom)).val AS val
     FROM mnt, line
     WHERE ST_Intersects(mnt.rast, line.geom)),
    -- Instantiate 3D points, ordered on line
  points3d AS
    (SELECT ST_SetSRID(ST_MakePoint(ST_X(cells.geom), ST_Y(cells.geom), val), 32632) AS geom
     FROM cells, line
     ORDER BY ST_Distance(ST_StartPoint(line.geom), cells.geom))
-- Build 3D line from 3D points
SELECT ST_MakeLine(geom) FROM points3d;"""

# drape your geometries
# -- Add a column to your table
alter = """ALTER TABLE yourtable ADD COLUMN geom_3d geometry(LineStringZ, 32632);"""

# -- Fill it
update = """UPDATE yourtable SET geom_3d = drape(geom);"""

# Altimetric profiles
# We obtain a basic chart, where you have the distance in abscissa and altitude in ordinate.
# This SQL query returns 2 columns, x and y axis.

profile_chart_query = """
WITH points3d AS
    (SELECT (ST_DumpPoints(geom_3d)).geom AS geom,
            ST_StartPoint(geom_3d) AS origin
     FROM yourtable
     WHERE id = 1234)
SELECT ST_distance(origin, geom) AS x, ST_Z(geom) AS y
FROM points3d;"""
