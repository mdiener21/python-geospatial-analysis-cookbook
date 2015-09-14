#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
from geojson import loads, Feature, FeatureCollection

db_host = "localhost"
db_user = "pluto"
db_passwd = "secret"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port,
                        password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

start_x = 1587927.204
start_y = 5879726.142
end_x = 1587947.304
end_y = 5879611.257

# find the start node id within 1 meter of the given coordinate
# used as input in routing query start point
start_node_query = """
    SELECT id FROM geodata.ch08_e01_networklines_vertices_pgr AS p
    WHERE ST_DWithin(the_geom, ST_GeomFromText('POINT(%s %s)',3857), 1);"""

# locate the end node id within 1 meter of the given coordinate
end_node_query = """
    SELECT id FROM geodata.ch08_e01_networklines_vertices_pgr AS p
    WHERE ST_DWithin(the_geom, ST_GeomFromText('POINT(%s %s)',3857), 1);
    """

# get the start node id as an integer
cur.execute(start_node_query, (start_x, start_y))
sn = int(cur.fetchone()[0])

# get the end node id as an integer
cur.execute(end_node_query, (end_x, end_y))
en = int(cur.fetchone()[0])


# pgRouting query to return our list of segments representing
# our shortest path Dijkstra results as GeoJSON
# query returns the shortest path between our start and end nodes above
# using the python .format string syntax to insert a variable in the query
routing_query = '''
    SELECT seq, id1 AS node, id2 AS edge, ST_Length(wkb_geometry) AS cost,
           ST_AsGeoJSON(wkb_geometry) AS geoj
      FROM pgr_dijkstra(
        'SELECT ogc_fid as id, source, target, st_length(wkb_geometry) as cost
         FROM geodata.ch08_e01_networklines',
        {start_node},{end_node}, FALSE, FALSE
      ) AS dij_route
      JOIN  geodata.ch08_e01_networklines AS input_network
      ON dij_route.id2 = input_network.ogc_fid ;
  '''.format(start_node=sn, end_node=en)


# run our shortest path query
cur.execute(routing_query)

# get entire query results to work with
route_segments = cur.fetchall()

# empty list to hold each segment for our GeoJSON output
route_result = []

# loop over each segment in the result route segments
# create the list for our new GeoJSON
for segment in route_segments:
    geojs = segment[4]
    geojs_geom = loads(geojs)
    geojs_feat = Feature(geometry=geojs_geom, properties={'nice': 'route'})
    route_result.append(geojs_feat)

# using the geojson module to create our GeoJSON Feature Collection
geojs_fc = FeatureCollection(route_result)

# define the output folder and GeoJSON file name
output_geojson_route = "../geodata/ch08_shortest_path_pgrouting.geojson"


# save geojson to a file in our geodata folder
def write_geojson():
    with open(output_geojson_route, "w") as geojs_out:
        geojs_out.write(json.dumps(geojs_fc))


# run the write function to actually create the GeoJSON file
write_geojson()

# clean up and close database curson and connection
cur.close()
conn.close()