#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import json
import pprint
from geojson import loads, Feature, FeatureCollection

# Database Connection Info
db_host = "localhost"
db_user = "pluto"
db_passwd = "stars"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user,
    port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

complex_query = """
    SELECT
      ST_AsGeoJSON(st_centroid(g.wkb_geometry)) AS geom,
          c.name AS city,
          g.name AS golfclub,
          p.name_en AS park,
	  ST_Distance(geography(c.wkb_geometry), geography(g.wkb_geometry)) AS distance,
	  ST_Distance(geography(p.geom), geography(g.wkb_geometry)) AS distance
      FROM 
	    geodata.parks_pa_canada AS p,
	    geodata.cities_bc_alberta AS c
      JOIN 
	    geodata.golf_courses_bc_alberta AS g
      ON
        ST_DWithin(geography(c.wkb_geometry), geography(g.wkb_geometry),4000)
     WHERE
        ST_DWithin(geography(p.geom), geography(g.wkb_geometry),5000)
                """
# WHERE c.population is not null and e.name is not null
# execute the query
cur.execute(complex_query)

# return all the rows, we expect more than one
validity_results = cur.fetchall()

# an empty list to hold each feature of our feature collection
new_geom_collection = []

# loop through each row in result query set and add to my feature collection
# assign name field to the GeoJSON properties
for each_result in validity_results:
    geom = each_result[0]
    city_name = each_result[1]
    course_name = each_result[2]
    park_name = each_result[3]
    dist_city_to_golf = each_result[4]
    dist_park_to_golf = each_result[5]
    geoj_geom = loads(geom)
    myfeat = Feature(geometry=geoj_geom, properties={'city': city_name, 'golf_course': course_name,
												 'park_name': park_name, 'dist_to city': dist_city_to_golf,
												 'dist_to_park': dist_park_to_golf})
    new_geom_collection.append(	myfeat)  # use the geojson module to create the final Feature Collection of features created from for loop above

my_geojson = FeatureCollection(new_geom_collection)

pprint.pprint(my_geojson)

# define the output folder and GeoJSon file name
output_geojson_buf = "../../../geodata/golfcourses_analysis.geojson"


# save geojson to a file in our geodata folder
def write_geojson():
    fo = open(output_geojson_buf, "w")
    fo.write(json.dumps(my_geojson))
    fo.close()

# run the write function to actually create the GeoJSON file
write_geojson()

# close cursor
cur.close()

# close connection
conn.close()
