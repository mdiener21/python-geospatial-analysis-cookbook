#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile
from shapely.geometry import asShape, MultiPolygon, MultiPoint, MultiLineString
import json

def shp2_geojson_obj(shapefile_path):
    # open shapefile
    in_shp = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_shp.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_shp.fields[1:]

    # using list comprehension to create list of field names
    field_names = [field_name[0] for field_name in fc_fields]
    my_fc_list = []
    # run through each shape geometry and attribute
    for x in shp_records:
        field_attributes = dict(zip(field_names, x.record))
        geom_j = x.shape.__geo_interface__
        my_fc_list.append(dict(type='Feature', geometry=geom_j,
                               properties=field_attributes))

    geoj_json_obj = {'type': 'FeatureCollection',
                     'features': my_fc_list}

    return geoj_json_obj


def create_shply_multigeom(in_geojs, geom_type):
    '''

    :param in_geojs: geojson input
    :param geom_type: enter string MultiPolygon, MultiPoint, MultiLineString
    :return: Shapely Geometry
    '''
    shps_list = []
    for feature in in_geojs['features']:
        shape = asShape(feature['geometry'])
        shps_list.append(shape)

    if geom_type == "MultiPolygon":
        new_multi = MultiPolygon(shps_list)
    elif geom_type == "MultiPoint":
        new_multi = MultiPoint(shps_list)
    elif geom_type == "MultiLineString":
        new_multi = MultiLineString(shps_list)
    else:
        print "sorry invalid geom_type only accepted MultiPolygon, MultiPoint, MultiLineString"
    return new_multi


def out_geoj(list_geom, out_geoj_file):
    out_geojson = dict(type='FeatureCollection', features=[])

    # generate geojson file output
    for (index_num, ply) in enumerate(list_geom):
        feature = dict(type='Feature', properties=dict(id=index_num))
        feature['geometry'] = ply.__geo_interface__
        out_geojson['features'].append(feature)

    # create geojson file on disk
    json.dump(out_geojson, open(out_geoj_file, 'w'))