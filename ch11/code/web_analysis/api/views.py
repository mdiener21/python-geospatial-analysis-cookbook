#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geojson import loads, Feature, FeatureCollection
import logging
logger = logging.getLogger(__name__)
from django.db import connection


def find_closest_network_node(x_coord, y_coord, floor):
    """
    Enter a given coordinate x,y and floor number and
    find the nearest network node
    to start or end the route on
    :param x_coord: float  in epsg 3857
    :param y_coord: float  in epsg 3857
    :param floor: integer value equivalent to floor such as 2  = 2nd floor
    :return: node id as an integer
    """
    # connect to our Database
    logger.debug("now running function find_closest_network_node")
    cur = connection.cursor()

    # find nearest node on network within 200 m
    # and snap to nearest node
    query = """ SELECT
        verts.id as id
        FROM geodata.networklines_3857_vertices_pgr AS verts
        INNER JOIN
          (select ST_PointFromText('POINT(%s %s %s)', 3857)as geom) AS pt
        ON ST_DWithin(verts.the_geom, pt.geom, 200.0)
        ORDER BY ST_3DDistance(verts.the_geom, pt.geom)
        LIMIT 1;"""

    # pass 3 variables to our %s %s %s place holder in query
    cur.execute(query, (x_coord, y_coord, floor,))

    # get the result
    query_result = cur.fetchone()

    # check if result is not empty
    if query_result is not None:
        # get first result in tuple response there is only one
        point_on_networkline = int(query_result[0])
        return point_on_networkline
    else:
        logger.debug("query is none check tolerance value of 200")
        return False


# use the rest_framework decorator to create our api
#  view for get, post requests
@api_view(['GET', 'POST'])
def create_route(request, start_coord, start_floor, end_coord, end_floor):
    """
    Generate a GeoJSON indoor route passing in a start x,y,floor
    followed by &  then the end x,y,floor
    Sample request: http:/localhost:8000/api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    :param request:
    :param start_coord: start location x,y
    :param start_floor: floor number  ex)  2
    :param end_coord: end location x,y
    :param end_floor: end floor ex)  2
    :return: GeoJSON route
    """

    if request.method == 'GET' or request.method == 'POST':

        cur = connection.cursor()

        # parse the incoming coordinates and floor using
        # split by comma
        x_start_coord = float(start_coord.split(',')[0])
        y_start_coord = float(start_coord.split(',')[1])
        start_floor_num = int(start_floor)

        x_end_coord = float(end_coord.split(',')[0])
        y_end_coord = float(end_coord.split(',')[1])
        end_floor_num = int(end_floor)

        # use our helper function to get vertices
        # node id for start and end nodes
        start_node_id = find_closest_network_node(x_start_coord,
                                                  y_start_coord,
                                                  start_floor_num)

        end_node_id = find_closest_network_node(x_end_coord,
                                                y_end_coord,
                                                end_floor_num)

        routing_query = '''
            SELECT seq, id1 AS node, id2 AS edge,
              ST_Length(wkb_geometry) AS cost, layer,
              type_id, ST_AsGeoJSON(wkb_geometry) AS geoj
              FROM pgr_dijkstra(
                'SELECT ogc_fid as id, source, target,
                     st_length(wkb_geometry) AS cost,
                     layer, type_id
                 FROM geodata.networklines_3857',
                %s, %s, FALSE, FALSE
              ) AS dij_route
              JOIN  geodata.networklines_3857 AS input_network
              ON dij_route.id2 = input_network.ogc_fid ;
          '''

        # run our shortest path query
        if start_node_id or end_node_id:
            cur.execute(routing_query, (start_node_id, end_node_id))
        else:
            logger.error("start or end node is None "
                         + str(start_node_id))
            return HttpResponseNotFound('<h1>Sorry NO start or end node'
                                        ' found within 200m</h1>')

        # get entire query results to work with
        route_segments = cur.fetchall()

        # empty list to hold each segment for our GeoJSON output
        route_result = []

        # loop over each segment in the result route segments
        # create the list of our new GeoJSON
        for segment in route_segments:
            seg_cost = segment[3]      # cost value
            layer_level = segment[4]   # floor number
            seg_type = segment[5]
            geojs = segment[6]         # geojson coordinates
            geojs_geom = loads(geojs)  # load string to geom
            geojs_feat = Feature(geometry=geojs_geom,
                                 properties={'floor': layer_level,
                                              'length': seg_cost,
                                              'type_id': seg_type})
            route_result.append(geojs_feat)

        # using the geojson module to create our GeoJSON Feature Collection
        geojs_fc = FeatureCollection(route_result)

        try:
            return Response(geojs_fc)
        except:
            logger.error("error exporting to json model: "+ str(geojs_fc))
            logger.error(traceback.format_exc())
            return Response({'error': 'either no JSON or no key params in your JSON'})
    else:
        return HttpResponseNotFound('<h1>Sorry not a GET or POST request</h1>')
