#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.geometry import asShape, MultiPolygon
from utils import shp2_geojson_obj, out_geoj, write_wkt
from os.path import realpath

def create_polys(shp_data):
    """
    :param shp_data: input GeoJSON
    :return: MultiPolygon Shapely geometry
    """
    plys = []
    for feature in shp_data['features']:
        shape = asShape(feature['geometry'])
        plys.append(shape)

    new_multi = MultiPolygon(plys)
    return new_multi


def create_out(res1, res2):
    """

    :param res1: input feature
    :param res2: identity feature
    :return: MultiPolygon identity results
    """
    identity_geoms = []

    for g1 in res1:
        identity_geoms.append(g1)
    for g2 in res2:
        identity_geoms.append(g2)

    out_identity = MultiPolygon(identity_geoms)
    return out_identity


if __name__ == "__main__":
    # out two input test Shapefiles
    shp1 = realpath("../geodata/temp1-ply.shp")
    shp2 = realpath("../geodata/temp2-ply.shp")

    # output resulting GeoJSON file
    out_geojson_file = realpath("../geodata/result_identity.geojson")

    output_wkt_identity = realpath("ol3/data/ch06-04_results_identity.js")


    # convert our Shapefiles to GeoJSON
    # then to python dictionaries
    shp1_data = shp2_geojson_obj(shp1)
    shp2_data = shp2_geojson_obj(shp2)

    # transform our GeoJSON data into Shapely geom objects
    shp1_polys = create_polys(shp1_data)
    shp2_polys = create_polys(shp2_data)

    # run the difference and intersection
    res_difference = shp1_polys.difference(shp2_polys)
    res_intersection = shp1_polys.intersection(shp2_polys)

    # combine the difference and intersection polygons into results
    result_identity = create_out(res_difference, res_intersection)

    # export identity results to a GeoJSON
    out_geoj(result_identity, out_geojson_file)

    # write out new javascript variable with wkt geometry
    write_wkt(output_wkt_identity, result_identity )
