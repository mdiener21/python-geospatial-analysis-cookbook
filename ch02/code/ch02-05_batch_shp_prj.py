#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os
from osgeo import osr


def create_epsg_wkt_esri(epsg):
    """
    Get the ESRI formatted .prj definition
    usage create_epsg_wkt(4326)

    We use the http://spatialreference.org/ref/epsg/4326/esriwkt/

    """
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(epsg)

    # transform projection format to ESRI .prj style
    spatial_ref.MorphToESRI()

    # export to WKT
    wkt_epsg = spatial_ref.ExportToWkt()

    return wkt_epsg


# Optional method to get EPGS as wkt from a web service
def get_epsg_code(epsg):
    """
    Get the ESRI formatted .prj definition
    usage get_epsg_code(4326)

    We use the http://spatialreference.org/ref/epsg/4326/esriwkt/

    """
    web_url = "http://spatialreference.org/ref/epsg/{0}/esriwkt/".format(epsg)
    f = urllib.urlopen(web_url)
    return f.read()


# Here we write out a new .prj file with the same name
# as our Shapefile named "schools" in this example
def write_prj_file(folder_name, shp_filename, epsg):
    """
    input the name of a Shapefile without the .shp
    input the EPSG code number as an integer

    usage  write_prj_file(<ShapefileName>,<EPSG CODE>)

    """

    in_shp_name = "/{0}.prj".format(shp_filename)
    full_path_name = folder_name + in_shp_name

    with open(full_path_name, "w") as prj:
        epsg_code = create_epsg_wkt_esri(epsg)
        prj.write(epsg_code)
        print ("done writing projection definition : " + epsg_code)


def run_batch_define_prj(folder_location, epsg):
    """
    input path to the folder location containing
    all of your Shapefiles

    usage  run_batch_define_prj("../geodata/no_prj")

    """

    # variable to hold our list of shapefiles
    shapefile_list = []

    # loop through the directory and find shapefiles
    # for each found shapefile write it to a list
    # remove the .shp ending so we do not end up with 
    # file names such as .shp.prj
    for shp_file in os.listdir(folder_location):
        if shp_file.endswith('.shp'):
            filename_no_ext = os.path.splitext(shp_file)[0]
            shapefile_list.append(filename_no_ext)

    # loop through the list of shapefiles and write
    # the new .prj for each shapefile
    for shp in shapefile_list:
        write_prj_file(folder_location, shp, epsg)


# Windows users please use the full path
# Linux users can also use full path        
run_batch_define_prj("c:/02_DEV/01_projects/04_packt/ch02/geodata/no_prj/", 4326)
