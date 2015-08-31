#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from os.path import realpath
import shapefile  # pyshp
from geojson import Feature, FeatureCollection
from shapely.geometry import asShape, MultiPolygon
from shapely.ops import polygonize
from shapely.wkt import dumps


def create_shapes(shapefile_path):
    """
    Convert Shapefile Geometry to Shapely MultiPolygon
    :param shapefile_path: path to a shapefile on disk
    :return: shapely MultiPolygon
    """
    in_ply = shapefile.Reader(shapefile_path)

    # using pyshp reading geometry
    ply_shp = in_ply.shapes()
    ply_records = in_ply.records()
    ply_fields = in_ply.fields
    print ply_records
    print ply_fields

    if len(ply_shp) > 1:
        # using python list comprehension syntax
        # shapely asShape to convert to shapely geom
        ply_list = [asShape(feature) for feature in ply_shp]

        # create new shapely multipolygon
        out_multi_ply = MultiPolygon(ply_list)

        # # equivalent to the 2 lines above without using list comprehension
        # new_feature_list = []
        # for feature in features:
        #     temp = asShape(feature)
        #     new_feature_list.append(temp)
        # out_multi_ply = MultiPolygon(new_feature_list)

        print "converting to MultiPolygon: " + str(out_multi_ply)
    else:
        print "one or no features found"
        shply_ply = asShape(ply_shp)
        out_multi_ply = MultiPolygon(shply_ply)

    return out_multi_ply


def create_union(in_ply1, in_ply2, result_geojson):
    """
    Create union polygon
    :param in_ply1: first input shapely polygon
    :param in_ply2: second input shapely polygon
    :param result_geojson: output geojson file including full file path
    :return: shapely MultiPolygon
    """
    # union the polygon outer linestrings together
    outer_bndry = in_ply1.boundary.union(in_ply2.boundary)

    # rebuild linestrings into polygons
    output_poly_list = polygonize(outer_bndry)

    out_geojson = dict(type='FeatureCollection', features=[])

    # generate geojson file output
    for (index_num, ply) in enumerate(output_poly_list):
        feature = dict(type='Feature', properties=dict(id=index_num))
        feature['geometry'] = ply.__geo_interface__
        out_geojson['features'].append(feature)

    # create geojson file on disk
    json.dump(out_geojson, open(result_geojson, 'w'))

    # create shapely MultiPolygon
    ply_list = []
    for fp in polygonize(outer_bndry):
        ply_list.append(fp)

    out_multi_ply = MultiPolygon(ply_list)

    return out_multi_ply


def write_wkt(filepath, features):
    """

    :param filepath: output path for new javascript file
    :param features: shapely geometry features
    :return:
    """
    with open(filepath, "w") as f:
        # create a javascript variable called ply_data used in html
        # Shapely dumps geometry out to WKT
        f.write("var ply_data = '" + dumps(features) + "'")


def output_geojson_fc(shply_features, outpath):
    """
    Create valid GeoJSON python dictionary
    :param shply_features: shapely geometries
    :param outpath:
    :return: GeoJSON FeatureCollection File
    """

    new_geojson = []
    for feature in shply_features:
        feature_geom_geojson = feature.__geo_interface__
        myfeat = Feature(geometry=feature_geom_geojson,
                         properties={'name': "mojo"})
        new_geojson.append(myfeat)

    out_feat_collect = FeatureCollection(new_geojson)

    with open(outpath, "w") as f:
        f.write(json.dumps(out_feat_collect))


if __name__ == "__main__":

    # define our inputs
    shp1 = realpath("../geodata/temp1-ply.shp")
    shp2 = realpath("../geodata/temp2-ply.shp")

    # define outputs
    out_geojson_file = realpath("../geodata/res_union.geojson")
    output_union = realpath("../geodata/output_union.geojson")
    out_wkt_js = realpath("ol3/data/results_union.js")

    # create our shapely multipolygons for geoprocessing
    in_ply_1_shape = create_shapes(shp1)
    in_ply_2_shape = create_shapes(shp2)

    # run generate union function
    result_union = create_union(in_ply_1_shape, in_ply_2_shape, out_geojson_file)

    # write to our output js file the new polygon as wkt
    write_wkt(out_wkt_js, result_union)

    # write the results out to well known text (wkt) with shapely dump
    geojson_fc = output_geojson_fc(result_union, output_union)
