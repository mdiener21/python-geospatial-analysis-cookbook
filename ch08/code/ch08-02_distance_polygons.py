#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import shapefile
import json
import shapely.geometry as geometry
from geojson import loads, Feature, FeatureCollection
from shapely.geometry import asShape

# database connection
db_host = "localhost"
db_user = "postgres"
db_passwd = "air"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port,
                        password=db_passwd, database=db_database)
cur = conn.cursor()

def write_geojson(outfilename, indata):
    file_out = open(outfilename, "w")
    file_out.write(json.dumps(indata))

# center point for creating our distance polygons
x_start_coord = 71384.9532168
y_start_coord = 164571.903749

# query including two variables for the x, y POINT coordinate
start_node_query = """
    SELECT id
    FROM geodata.ch08_e01_networklines_vertices_pgr AS p
    WHERE ST_DWithin(the_geom,
             ST_GeomFromText('POINT(%s %s)',31255),1);"""

# get the start node id as an integer
# pass the variables
cur.execute(start_node_query, (x_start_coord, y_start_coord))
sn = int(cur.fetchone()[0])

comb_res = []

hallways = shapefile.Reader("../geodata/shp/e01_hallways_union.shp")
e01_hallway_features = hallways.shape()
e01_hallway_shply = asShape(e01_hallway_features)

# time in seconds
evac_times = [10, 20, 30, 60]


for evac_time in evac_times:

    distance_poly_query = '''
        SELECT seq, id1 AS node, cost, ST_AsGeoJSON(the_geom)
            FROM pgr_drivingDistance(
                    'SELECT ogc_fid AS id, source, target,
                        ST_Length(wkb_geometry)/5000*60*60 AS cost
                     FROM geodata.ch08_e01_networklines',
                    %s, %s, false, false
            ) as drive_dist
            JOIN geodata.ch08_e01_networklines_vertices_pgr
            AS networklines
            ON drive_dist.id1 = networklines.id;
        '''

    cur.execute(distance_poly_query,(sn, evac_time))
    # get entire query results to work with
    distance_nodes = cur.fetchall()

    # empty list to hold each segment for our GeoJSON output
    route_results = []

    # loop over each segment in the result route segments
    # create the list of our new GeoJSON
    for dist_node in distance_nodes:
        sequence = dist_node[0]     # sequence number
        node = dist_node[1]         # node id
        cost = dist_node[2]         # cost value
        geojs = dist_node[3]        # geometry
        geojs_geom = loads(geojs) # create geojson geom
        geojs_feat = Feature(geometry=geojs_geom,
                properties={'sequence_num': sequence,
                'node':node, 'evac_time_sec':cost,
                'evac_code': evac_time})
        # add each point to total including all points
        comb_res.append(geojs_feat)
        # add each point for individual evacuation time
        route_results.append(geojs_geom)

    # geojson module creates GeoJSON Feature Collection
    geojs_fc = FeatureCollection(route_results)

    # create list of points for each evac time
    evac_time_pts = [asShape(route_segment) for route_segment in route_results]

    # code here is same as list comprehension above for better readability
    # evac_time_pts = []
    # for route_segment in route_results:
    #     shply_geom = asShape(route_segment)
    #     evac_time_pts.append(shply_geom)

    # create MultiPoint from our list of points for evac time
    point_collection = geometry.MultiPoint(list(evac_time_pts))

    #create our convex hull polyon around evac time points
    convex_hull_polygon = point_collection.convex_hull

    # intersect convex hull with hallways polygon  (ch = convex hull)
    ch_intersect = e01_hallway_shply.intersection(convex_hull_polygon)

    # export convex hull intersection to geojson
    ch = ch_intersect.__geo_interface__

    # for each evac time we create a unique GeoJSON polygon
    output_ply = "../geodata/ch08-02_dist_poly_" + str(evac_time) + ".geojson"

    write_geojson(output_ply, ch)

    output_geojson_route = "../geodata/ch08-02_dist_pts_" + str(evac_time) + ".geojson"

    # save GeoJSON to a file in our geodata folder
    write_geojson(output_geojson_route, geojs_fc )

# final result GeoJSON
final_res = FeatureCollection(comb_res)

# write to disk
write_geojson("../geodata/final_res.geojson", final_res)

# clean up and close database curson and connection
cur.close()
conn.close()