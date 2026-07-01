-- The chain blocklist as a TABLE (the core IP), so it can be tuned via
-- PostgREST/curl without a code change or rebuild. Seeded from chains.py.
-- kind: lodging | food | soft_brand (soft_brand = affiliation whitelist, NOT blocked).

CREATE TABLE IF NOT EXISTS chain_blocklist (
    term     TEXT PRIMARY KEY,          -- normalized match term, e.g. "super 8"
    kind     TEXT NOT NULL DEFAULT 'lodging',
    note     TEXT,
    added_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chain_blocklist_kind_idx ON chain_blocklist (kind);
