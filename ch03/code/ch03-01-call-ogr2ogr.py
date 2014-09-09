#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


subprocess.call(['/Library/Frameworks/GDAL.framework/Programs/ogr2ogr', '-f',
                 '"GeoJSON"', 'output.json', 'input.shp'])

############### option 1 with subprocess
### convert .tab to SHP
import os
output_format = "ESRI Shapefile"
output_shp = "C:/Users/mdiener/myshape.shp"
input_tab = "C:/Users/mdiener/myshape.tab"
command = "ogr2ogr -f \"" + output_format + "\" " + output_shp + " " input_tab
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000) 

command = "ogr2ogr -f \"ESRI Shapefile\" E:\\CABWorking\\MapINFO2SHP\\SHP\\LincsBoundary.shp E:\\CABWorking\\MapINFO2SHP\\MapINFOData\\Lincolnshire.tab"
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000) 
#the third command suppresses the opening of a new window for each process
#and can be removed if this is not the desired outcome
process.wait() #waits for one process to complete before launching another one

# export select pg tables to shapefile
#ogr2ogr -f "ESRI Shapefile" mydatadump PG:"host=myhost user=myloginname dbname=mydbname password=mypassword" neighborhood parcels

#c:/OSGeo4W/bin/ogr2ogr.exe -f "ESRI Shapefile" shp geodata.sqlite -dsco SPATIALITE=yes
#c:/OSGeo4W/bin/ogr2ogr.exe/ogr2ogr.exe -append -lco GEOMETRY_NAME=geom -lco SCHEMA=geodata -f "PostgreSQL" PG:"host=localhost port=5432 user=username dbname=nameOfDatabase password=yourDbPassword" -a_srs "EPSG:31468" gisdata.sqlite
#c:/OSGeo4W/bin/ogr2ogr.exe -f SQlite output.sqlite input_spatialdb.sqlite -dsco SPATIALITE=no -lco FORMAT=WKT

####### option other
import os
command = "ogr2ogr -f \"ESRI Shapefile\" E:\\CABWorking\\MapINFO2SHP\\SHP\\LincsBoundary.shp E:\\CABWorking\\MapINFO2SHP\\MapINFOData\\Lincolnshire.tab"
os.system(command)
################### option 2
import os, glob
inputDir = raw_input("==> ") # Had to have this code compatible with 2.3.4
outputDir = raw_input("==> ") # So that meant no easy file dialog boxes
TabFiles = glob.glob(str(inputDir) + '/*.tab')
for TabFile in TabFiles:
    TabFileName = TabFile[(TabFile.rfind("\\"))+1:(TabFile.rfind("."))]
    command = 'ogr2ogr -f "ESRI Shapefile" ' + outputDir + "/" + TabFileName + '.shp ' + TabFile
    os.system(command)