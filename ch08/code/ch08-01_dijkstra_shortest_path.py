#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection

db_host = "localhost"
db_user = "postgres"
db_passwd = "air" # secret
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port,
                        password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

# passing the name of the imported table
# plus the tolerance value, geometry column and primary key field
create_table = '''
    SELECT public.pgr_createTopology('geodata.ch08_e01_networklines',
        0.0005, 'wkb_geometry', 'ogc_fid');
    '''
# run the create table query
# cur.execute(create_table)

# commit the new table to the database
#conn.commit()

# pgRouting query to return our list of segments representing
# our shortest path Dijkstra results as GeoJSON
routing_query =  '''
    SELECT seq, id1 AS node, id2 AS edge, ST_Length(wkb_geometry) AS cost,
           ST_AsGeoJSON(wkb_geometry) as geoj
      FROM pgr_dijkstra(
        'SELECT ogc_fid as id, source, target, st_length(wkb_geometry) as cost
         FROM geodata.ch08_e01_networklines',
        1, 472, FALSE, FALSE
      ) AS di
      JOIN  geodata.ch08_e01_networklines pt
      ON di.id2 = pt.ogc_fid ;
  '''

# run our shortest path query
cur.execute(routing_query)

# get entire query results to work with
route_segments = cur.fetchall()

# empty list to hold each segment for our GeoJSON output
route_result = []

# loop over each segment in the result route segments
# create the list of our new GeoJSON
for segment in route_segments:
    geojs = segment[4]
    geojs_geom = loads(geojs)
    geojs_feat = Feature(geometry=geojs_geom, properties={'nice': 'route'})
    route_result.append(geojs_feat)

# using the geojson module to create our GeoJSON Feature Collection
geojs_fc = FeatureCollection(route_result)

# define the output folder and GeoJSON file name
output_geojson_route = "../geodata/ch08_shortest_path.geojson"

# save geojson to a file in our geodata folder
def write_geojson():
    file_out = open(output_geojson_route, "w")
    file_out.write(json.dumps(geojs_fc))
    file_out.close()

# run the write function to actually create the GeoJSON file
write_geojson()

# clean up and close database curson and connection
cur.close()
conn.close()