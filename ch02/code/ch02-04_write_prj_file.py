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

# Shapefile filename must equal the new .prj filename
shp_filename = "UTM_Zone_Boundaries"

# path to where Shapefile with no .prj is located
os.chdir("../geodata/")

# Here we write out a new .prj file with the same name
# as our Shapefile named "schools" in this example

with open("%s.prj" % shp_filename, "w") as prj:
    epsg_code = get_epsg_code(4326)
    prj.write(epsg_code)
    print "done writing projection definition " + prj.name + "to EPSG:" + epsg_code

# now change abck to our code directory
os.chdir("../code/")