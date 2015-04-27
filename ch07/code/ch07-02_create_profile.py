#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

db_host = "localhost"
db_user = "postgres"
db_passwd = "air"
db_database = "py_geoan_cb"
db_port = "5432"

# connect to DB
conn = psycopg2.connect(host=db_host, user=db_user, port=db_port, password=db_passwd, database=db_database)

# create a cursor
cur = conn.cursor()

create_table = '''CREATE TABLE geodata.ch07_profile_line ( id serial PRIMARY KEY, NAME varchar(50) );'''
cur.execute(create_table)

add_geom = '''SELECT AddGeometryColumn('geodata', 'ch07_profile_line','geom',3857,'LINESTRING',2);'''
cur.execute(add_geom)


insert_line = '''INSERT INTO geodata.ch07_profile_line (NAME, GEOM)
                VALUES (
                  'profile line',
                  ST_GeomFromText('LINESTRING(-13659328.8483806 6450545.73152317,-13651422.7820022 6466228.25663444)', 3857)
                );'''
cur.execute(insert_line)

# psql function to create 3d Line
# thanks to Mathieu Leplatre for the SQL
# http://blog.mathieu-leplatre.info/drape-lines-on-a-dem-with-postgis.html
create_pg_drape = '''CREATE OR REPLACE FUNCTION drape(line geometry, epsg integer) RETURNS geometry AS $$
DECLARE
line3d geometry;

BEGIN
     WITH linemesure AS
        -- Add a mesure dimension to extract steps
        (SELECT ST_AddMeasure(line, 0, ST_Length(line)) as linem,
                generate_series(0, ST_Length(line)::int, 5) as i),
      points2d AS
        (SELECT ST_GeometryN(ST_LocateAlong(linem, i), 1) AS geom FROM linemesure),
      cells AS
        -- Get DEM elevation for each
        (SELECT p.geom AS geom, ST_Value(dem.rast, 1, p.geom) AS val
         FROM geodata.dem_3857 as dem, points2d p
         WHERE ST_Intersects(dem.rast, p.geom)),
        -- Instantiate 3D points
      points3d AS
        (SELECT ST_SetSRID(ST_MakePoint(ST_X(geom), ST_Y(geom), val), epsg) AS geom FROM cells)
    -- Build 3D line from 3D points
    SELECT ST_MakeLine(geom) INTO line3d FROM points3d;
    RETURN line3d;
END;
$$ LANGUAGE plpgsql;'''

# create the pgsql drape function in the database
cur.execute(create_pg_drape)

# add a second 3d geometry column to the profile line table
add_3dcol = '''ALTER TABLE geodata.ch07_profile_line ADD COLUMN geom_3d geometry(LineStringZ, 3857);'''

# run the alter table query to create new column
cur.execute(add_3dcol)

# populate the new column with the 3D line
update_3d_col = '''UPDATE geodata.ch07_profile_line SET geom_3d = drape(geom, 3857);'''

# execute the update query
cur.execute(update_3d_col)

# create a query to return a list of X (distance) and Z value pairs for the profile graph
generate_x_z_profile = '''     WITH points3d AS
    (SELECT (ST_DumpPoints(geom_3d)).geom AS geom,
            ST_StartPoint(geom_3d) AS origin
     FROM geodata.ch07_profile_line
     WHERE id = 1)
    SELECT ST_distance(origin, geom) AS x, ST_Z(geom) AS y
    FROM points3d'''

# execute the query that generates the X (distance), Z output
cur.execute(generate_x_z_profile)


# commit the new table and inserts to the database
# if you forget this the new table is not created
conn.commit()

# get all results of X (distance) and Z pairs for export
result_profile_x_z = cur.fetchall()

# check if output file exists on disk if yes delete it
if os.path.isfile('output_profile.csv'):
    os.remove('output_profile.csv')

# create new CSV file containing X (distance) and Z value pairs
with open('output_profile.csv', 'a') as outfile:
    # write first row column names into CSV
    outfile.write("distance,elevation" + "\n")
    # loop through each pair and write to CSV
    for x, z in result_profile_x_z:
        outfile.write(str(round(x,2)) + ',' + str(round(z,2)) + '\n')

# clean up and close our Database connection and cursor
cur.close()
conn.close()


# plot our new CSV using Matplotlib to screen
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.set_title("Elevation Profile")
ax1.set_xlabel('Distance (m)')
ax1.set_ylabel('Elevation (m)')

data = np.genfromtxt('output_profile.csv', delimiter=',', skip_header=10,
                     skip_footer=10, names=['distance', 'elevation'])

ax1.plot(data['distance'], data['elevation'], color='r', label='the data')

# save our profile as image PND and PDF
plt.savefig('profile_plot.png')
plt.savefig('profile_plot.pdf')

pyplot.show()