select ST_AsGeoJSON(ST_Buffer(st_transform(wkb_geometry, 3857), 100)) as geom, name, country,
               altitude from geodata.highest_mountains where ogc_fid = 2;

SELECT Find_SRID('geodata', 'highest_mountains', 'wkb_geometry');

Select ST_SetSRID(wkb_geometry, 4326) from geodata.highest_mountains;

SELECT UpdateGeometrySRID('geodata.highest_mountains','wkb_geometry',4326);

select UpdateGeometrySRID('geodata', 'highest_mountains', 'wkb_geometry', 4326);

select UpdateGeometrySRID('geodata', 'bike_shops_3785', 'wkb_geometry', 3857);