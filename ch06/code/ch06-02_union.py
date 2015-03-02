#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import shapefile
from geojson import Feature, FeatureCollection
from shapely.geometry import asShape, MultiPolygon, Polygon
from shapely.ops import polygonize

# open first polygon shapefile with pyshp
in_ply_1 = shapefile.Reader("../geodata/temp1-ply.shp")

# open second polygon shapefile with pyshp
in_ply_2 = shapefile.Reader("../geodata/temp2-ply.shp")

# access the geometries of each polygon using pyshp
in_ply_2_shape = in_ply_2.shapes()
in_ply_1_shape = in_ply_1.shapes()


def create_shply_features(features):
    """
    create shapely MultiPolygons
    :param features: list of geometry shapes
    :return: a list of shapely geometries
    """
    if len(features) > 1:
        print "we have more than one feature"
        new_feature_list = []
        for feature in features:
            temp = asShape(feature)
            new_feature_list.append(temp)
        out_multi_ply = MultiPolygon(new_feature_list)
    else:
        print "one or no features found"
        temp = asShape(features)
        out_multi_ply = MultiPolygon(temp)
    return out_multi_ply

def run_union(in_ply1, in_ply2):
    polygons2 = create_shply_features(in_ply1)
    polygons1 = create_shply_features(in_ply2)

    out_boundaries2 = polygons1.boundary.union(polygons2.boundary)

    out_shply = polygonize(out_boundaries2)
    return out_shply

result_union = run_union(in_ply_1_shape,in_ply_2_shape)

def output_geojson_fc(shply_features):
    new_geojson = []
    for feature in shply_features:
        foo = feature.__geo_interface__
        myfeat = Feature(geometry=foo, properties={'name': "mojo"})
        new_geojson.append(myfeat)

    out_feat_collect = FeatureCollection(new_geojson)
    return out_feat_collect


geojson_fc = output_geojson_fc(result_union)

output_union = "../geodata/output_union.geojson"

def write_geojson(outpath, in_geojson_fc):
    """
    create a GeoJSON file and write to disk
    :param outpath: for example could be "../geodata/output_union.geojson"
    :return: a geojson file written to outpath
    """
    with open(outpath, "w") as f:
        f.write(json.dumps(in_geojson_fc))

write_geojson(output_union, geojson_fc)