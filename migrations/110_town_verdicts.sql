-- Cache of evaluated towns: verdict + a pointer to what was scored + when.
-- Records FAILURES too (band = filter-out), so routing can tell "checked, dead"
-- from "not looked at yet". mode is part of the key (moto vs couple score differently).

CREATE TABLE IF NOT EXISTS town_verdicts (
    id           BIGSERIAL PRIMARY KEY,
    town         TEXT NOT NULL,
    state        TEXT NOT NULL,
    geoid        TEXT REFERENCES towns(geoid) ON DELETE SET NULL,
    mode         TEXT NOT NULL DEFAULT 'moto',   -- moto | couple
    lat          DOUBLE PRECISION,
    lon          DOUBLE PRECISION,
    location     geography(Point, 4326),
    total        REAL,
    band         TEXT,                            -- route-worthy|acceptable|marginal|filter-out
    scores       JSONB,                           -- per-dimension breakdown
    best_lodging JSONB,
    food         JSONB,
    reason       TEXT,
    tip          TEXT,
    verdict      JSONB,                           -- full raw judgment payload
    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (town, state, mode)                    -- one current verdict per town+mode
);

CREATE INDEX IF NOT EXISTS town_verdicts_loc_gix ON town_verdicts USING gist (location);
CREATE INDEX IF NOT EXISTS town_verdicts_band_idx ON town_verdicts (band);
CREATE INDEX IF NOT EXISTS town_verdicts_eval_idx ON town_verdicts (evaluated_at);
