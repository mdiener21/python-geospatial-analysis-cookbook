SELECT ST_AsGeoJSON(ST_Transform(ST_Buffer(wkb_geometry, 100,'quad_segs=8'),4326)) AS geom, name
               FROM geodata.schools;

SELECT Find_SRID('geodata', 'highest_mountains', 'wkb_geometry');

SELECT ST_SetSRID(wkb_geometry, 4326) FROM geodata.highest_mountains;

SELECT UpdateGeometrySRID('geodata.highest_mountains','wkb_geometry',4326);

SELECT UpdateGeometrySRID('geodata', 'highest_mountains', 'wkb_geometry', 4326);

SELECT UpdateGeometrySRID('geodata', 'bike_shops_3785', 'wkb_geometry', 3857);