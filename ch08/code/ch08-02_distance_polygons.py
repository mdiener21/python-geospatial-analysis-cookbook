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
cur = conn.cursor()


x_start_coord = 71384.9532168
y_start_coord = 164571.903749

evac_times = [10, 20, 30, 60]
distance_from_start = 60
for evac_time in evac_times:
    # query including two variables for the x, y POINT coordinate
    start_node_query = """
        SELECT id FROM geodata.ch08_e01_networklines_vertices_pgr AS p
        WHERE ST_DWithin(the_geom,
                 ST_GeomFromText('POINT(%s %s)',31255),1);"""

    # get the start node id as an integer
    # pass the variables
    cur.execute(start_node_query, (x_start_coord, y_start_coord))
    sn = int(cur.fetchone()[0])

    print sn

    distance_poly_query = '''
        SELECT seq, id1 AS node, cost, ST_AsGeoJSON(the_geom)
            FROM pgr_drivingDistance(
                    'SELECT ogc_fid as id, source, target, ST_Length(wkb_geometry)/5000*60*60 as cost FROM geodata.ch08_e01_networklines',
                    {start_point}, {distance}, false, false
            ) as drive_dist
            JOIN geodata.ch08_e01_networklines_vertices_pgr as networklines
            ON drive_dist.id1 = networklines.id;
        '''.format(start_point=sn, distance=evac_time)

    test_poly_query = '''
        SELECT seq, id1 AS node, cost
            FROM pgr_drivingDistance(
                    'SELECT ogc_fid as id, source, target, st_length(wkb_geometry)/5000*60*60 AS cost FROM geodata.ch08_e01_networklines',
                    472, 20, false, false
            );
        '''

    # some_view = """
    #  SELECT seq, id1 AS node, id2 AS edge, cost, geom
    #   FROM pgr_drivingdistance(
    #     'SELECT ogc_fid as id, source, target, traveltime_min as cost FROM network.publictransport',
    #     1, 100000, false, false
    #   ) as di
    #   JOIN network.publictransport_nodes pt
    #   ON di.id1 = pt.id;
    #   """

    cur.execute(distance_poly_query)
    # get entire query results to work with
    route_segments = cur.fetchall()

    # empty list to hold each segment for our GeoJSON output
    route_result = []

    # loop over each segment in the result route segments
    # create the list of our new GeoJSON
    for segment in route_segments:
        print segment
        sequence = segment[0]
        node = segment[1]
        cost = segment[2]

        geojs = segment[3]
        geojs_geom = loads(geojs)
        geojs_feat = Feature(geometry=geojs_geom, properties={'sequence_num': sequence,
                                                              'node':node, 'evac_time_sec':cost,
                                                              'evac_code': evac_time})
        route_result.append(geojs_feat)

    # using the geojson module to create our GeoJSON Feature Collection
    geojs_fc = FeatureCollection(route_result)

    # define the output folder and GeoJSON file name
    output_geojson_route = "../geodata/ch08-02_dist_pts_60.geojson"

    output_geojson_route2 = "../geodata/ch08-02_dist_pts_" + str(evac_time) + ".geojson"

    # save geojson to a file in our geodata folder
    def write_geojson():
        file_out = open(output_geojson_route2, "w")
        file_out.write(json.dumps(geojs_fc))
        file_out.close()

    # run the write function to actually create the GeoJSON file
    write_geojson()

# clean up and close database curson and connection
cur.close()
conn.close()