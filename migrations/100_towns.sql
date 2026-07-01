-- Reference table of US places (Census Gazetteer). Enables "towns within N miles
-- of a point" via PostGIS ST_DWithin — replaces hand-seeding candidate towns.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS towns (
    geoid       TEXT PRIMARY KEY,          -- Census GEOID (stable id)
    name        TEXT NOT NULL,             -- place name, e.g. "Dubuque"
    state       TEXT NOT NULL,             -- USPS code, e.g. "IA"
    lat         DOUBLE PRECISION,
    lon         DOUBLE PRECISION,
    location    geography(Point, 4326),    -- ST_MakePoint(lon, lat)
    lsad        TEXT,                       -- city / town / CDP / village ...
    population  INTEGER,
    search_text TEXT
);

CREATE INDEX IF NOT EXISTS towns_loc_gix   ON towns USING gist (location);
CREATE INDEX IF NOT EXISTS towns_state_idx ON towns (state);
CREATE INDEX IF NOT EXISTS towns_name_trgm ON towns USING gin (search_text gin_trgm_ops);
