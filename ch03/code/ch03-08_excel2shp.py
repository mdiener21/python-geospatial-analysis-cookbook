#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import shapefile

# open the excel file
excel_file = xlrd.open_workbook("../geodata/highest-mountains-europe.xlsx")

# get the first sheet
sh = excel_file.sheet_by_index(0)
w = shapefile.Writer(shapefile.POINT)

# fields available GeoNameId	Name	Country	Latitude	Longitude	Altitude (m)
w.field('GeoNameId','F')
w.field('Name', 'C')
w.field('Country', 'C')
w.field('Latitude', 'F')
w.field('Longitude', 'F')
w.field('Altitude', 'F')

# loop over each row in the excel sheet
for rownum in range(sh.nrows):
    # skips over the first row since it is the header row
    if rownum == 0:
        continue
    else:
        x_coord = sh.cell_value(rowx=rownum, colx=4)
        y_coord = sh.cell_value(rowx=rownum, colx=3)
        w.point(x_coord, y_coord)

        w.record(GeoNameId=sh.cell_value(rowx=rownum, colx=0), Name=sh.cell_value(rowx=rownum, colx=1),
                 Country=sh.cell_value(rowx=rownum, colx=2), Latitude=sh.cell_value(rowx=rownum, colx=3),
                 Longitude=sh.cell_value(rowx=rownum, colx=4),Altitude=sh.cell_value(rowx=rownum, colx=5))
        print "Adding row: " + str(rownum) + " creating mount: " + sh.cell_value(rowx=rownum, colx=1)

w.save('../geodata/highest-mountains')
