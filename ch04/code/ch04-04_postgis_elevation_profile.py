__author__ = 'mdiener'


# source  http://blog.mathieu-leplatre.info/drape-lines-on-a-dem-with-postgis.html

query = """
 WITH line AS
    -- From an arbitrary line
    (SELECT 'SRID=32632;LINESTRING (348595 4889225,352577 4887465,354784 4883841)'::geometry AS geom),
  cells AS
    -- Get DEM elevation for each intersected cell
    (SELECT ST_Centroid((ST_Intersection(mnt.rast, line.geom)).geom) AS geom,
    (ST_Intersection(mnt.rast, line.geom)).val AS val
     FROM mnt, line
     WHERE ST_Intersects(mnt.rast, line.geom)),
    -- Instantiate 3D points, ordered on line
  points3d AS
    (SELECT ST_SetSRID(ST_MakePoint(ST_X(cells.geom), ST_Y(cells.geom), val), 32632) AS geom
     FROM cells, line
     ORDER BY ST_Distance(ST_StartPoint(line.geom), cells.geom))
-- Build 3D line from 3D points
SELECT ST_MakeLine(geom) FROM points3d;"""

# drape your geometries
# -- Add a column to your table
alter = """ALTER TABLE yourtable ADD COLUMN geom_3d geometry(LineStringZ, 32632);"""

# -- Fill it
update = """UPDATE yourtable SET geom_3d = drape(geom);"""

# Altimetric profiles
# We obtain a basic chart, where you have the distance in abscissa and altitude in ordinate.
# This SQL query returns 2 columns, x and y axis.

profile_chart_query = """
WITH points3d AS
    (SELECT (ST_DumpPoints(geom_3d)).geom AS geom,
            ST_StartPoint(geom_3d) AS origin
     FROM yourtable
     WHERE id = 1234)
SELECT ST_distance(origin, geom) AS x, ST_Z(geom) AS y
FROM points3d;"""