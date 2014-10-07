#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os

def get_epsg_code(epsg):
   """
   Get the ESRI formatted .prj definition
   usage get_epsg_code(4326)

   We use the http://spatialreference.org/ref/epsg/4326/esriwkt/
   
   """
  
   f=urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/esriwkt/".format(epsg))
   return (f.read())

# Here we write out a new .prj file with the same name
# as our Shapefile named "schools" in this example
def write_prj_file(shp_filename, epsg):
    """
    input the name of a Shapefile without the .shp
    input the EPSG code number as an integer

    usage  write_prj_file(<ShapefileName>,<EPSG CODE>)

    """
    with open("%s.prj" % shp_filename, "w") as prj:
        epsg_code = get_epsg_code(epsg)
        #prj.write(epsg_code)
        print epsg_code
        print "done writing projection definition : " +  prj.name

# variable to hold our list of shapefiles
shapefile_list = []

# change directory to where we have folder with Shapefiles
# with no .prj files
os.chdir("../geodata/no_prj/")
current_dir = os.getcwd()

# loop through the current directory and find shapefiles
# for each found shapefile write it to a list
# remove the .shp ending so we do not end up with 
# file names such as .shp.prj
for file in os.listdir('.'):
  if file.endswith('.shp'):
    filename_no_ext = os.path.splitext(file)[0]
    shapefile_list.append(filename_no_ext)

# loop through the list of shapefiles and write
# the new .prj for each shapefile
for shp in shapefile_list:
    write_prj_file(shp, 4326)

