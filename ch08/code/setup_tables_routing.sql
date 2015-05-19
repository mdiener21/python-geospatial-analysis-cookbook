ALTER TABLE geodata.ch08_e01_networklines ADD COLUMN source INTEGER;
ALTER TABLE geodata.ch08_e01_networklines ADD COLUMN target INTEGER;
ALTER TABLE geodata.ch08_e01_networklines ADD COLUMN cost DOUBLE PRECISION;
ALTER TABLE geodata.ch08_e01_networklines ADD COLUMN length DOUBLE PRECISION;
UPDATE geodata.ch08_e01_networklines set length = ST_Length(wkb_geometry);

ALTER TABLE geodata.ch08_e02_networklines ADD COLUMN source INTEGER;
ALTER TABLE geodata.ch08_e02_networklines ADD COLUMN target INTEGER;
ALTER TABLE geodata.ch08_e02_networklines ADD COLUMN cost DOUBLE PRECISION;
ALTER TABLE geodata.ch08_e02_networklines ADD COLUMN length DOUBLE PRECISION;
UPDATE geodata.ch08_e02_networklines set length = ST_Length(wkb_geometry);

