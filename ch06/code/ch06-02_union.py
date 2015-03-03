#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import shapefile
from geojson import Feature, FeatureCollection
from shapely.geometry import asShape, MultiPolygon, Polygon
from shapely.ops import polygonize

shp1 = "../geodata/temp1-ply.shp"
shp2 = "../geodata/temp2-ply.shp"

out_geojson = "../geodata/temp22.geojson"

def shapefile_to_geojson(shapefile_path, out_geojson):
    # open shapefile
    in_ply = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_ply.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_ply.fields[1:]

    # using list comprehension to create list of field names
    field_names = [field_name[0] for field_name in fc_fields ]
    my_fc_list = []
    # run through each shape geometry and attribute
    for x in shp_records:
        field_attributes = dict(zip(field_names, x.record))
        geom_j = x.shape.__geo_interface__
        my_fc_list.append(dict(type='Feature', geometry=geom_j,
                               properties=field_attributes))

    # write GeoJSON to a file on disk
    with open(out_geojson, "w") as oj:
        oj.write(json.dumps({"type": "FeatureCollection",
                        "features": my_fc_list}))

    file_obj = json.dumps({"type": "FeatureCollection",
                    "features": my_fc_list})

    return file_obj


test = shapefile_to_geojson(shp1, out_geojson)
print test

def create_shapes(shapefile_path):
    """
    Convert Shapefile Geometry to Shapely MultiPolygon
    :param shapefile_path: path to a shapefile on disk
    :return: shapely MultiPolygon
    """
    in_ply = shapefile.Reader(shapefile_path)

    ply_shp = in_ply.shapes()
    # ply_shp = in_ply.shapeRecords()

    if len(ply_shp) > 1:
        # using python list comprehension syntax
        new_list = [asShape(feature) for feature in ply_shp]
        out_multi_ply = MultiPolygon(new_list)

        # # equivalent to list comprehension syntax
        # new_feature_list = []
        # for feature in features:
        #     temp = asShape(feature)
        #     new_feature_list.append(temp)
        # out_multi_ply = MultiPolygon(new_feature_list)

        print "converting to MultiPolygon: " + str(out_multi_ply)
    else:
        print "one or no features found"
        temp = asShape(ply_shp)
        out_multi_ply = MultiPolygon(temp)

    return out_multi_ply
    # return ply_shp

# access the geometries of each polygon using pyshp
in_ply_2_shape = create_shapes(shp1)
in_ply_1_shape = create_shapes(shp2)


def create_union(in_ply1, in_ply2):
    """
    Create union polygon
    :param in_ply1: first input polygon
    :param in_ply2: second input polygon
    :return: shapely polgon
    """
    # union the polygon outer linestrings together
    outer_bndry = in_ply1.boundary.union(in_ply2.boundary)

    # rebuild linestrings into polygons
    output_poly = polygonize(outer_bndry)
    return output_poly

result_union = create_union(in_ply_1_shape,in_ply_2_shape)

def output_geojson_fc(shply_features):
    """
    Create valid GeoJSON python dictionary
    :param shply_features: shaply geometries
    :return: GeoJSON FeatureCollection
    """
    new_geojson = []
    for feature in shply_features:
        feature_geom_geojson = feature.__geo_interface__
        myfeat = Feature(geometry=feature_geom_geojson,
                         properties={'name': "mojo"})
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