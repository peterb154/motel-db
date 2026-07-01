-- PostgREST surface: read-only views of towns + verdicts (feed the map UI), and
-- read/write on the chain blocklist (curl-tunable, per the brief). web_anon is the
-- anonymous role PostgREST assumes. NOTE: chain_blocklist is anon-writable — fine
-- for a personal LAN tool; put auth in front if ever exposed beyond the LXC.

CREATE SCHEMA IF NOT EXISTS api;

DO $$ BEGIN
    CREATE ROLE web_anon NOLOGIN;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

GRANT USAGE ON SCHEMA api TO web_anon;
GRANT web_anon TO strands;

CREATE OR REPLACE VIEW api.towns AS
    SELECT geoid, name, state, lat, lon, lsad, population FROM towns;

CREATE OR REPLACE VIEW api.town_verdicts AS
    SELECT town, state, mode, lat, lon, total, band, scores, best_lodging, food,
           reason, tip, evaluated_at
    FROM town_verdicts;

CREATE OR REPLACE VIEW api.chain_blocklist AS
    SELECT term, kind, note, added_at FROM chain_blocklist;

GRANT SELECT ON api.towns, api.town_verdicts TO web_anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON api.chain_blocklist TO web_anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON chain_blocklist TO web_anon;

NOTIFY pgrst, 'reload schema';
