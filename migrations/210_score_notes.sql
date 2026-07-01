-- Per-dimension explanations (why each score is what it is), surfaced in the
-- CLI, cache, and map. Kept separate from numeric `scores` so map/dedup/ranking
-- keep working unchanged.

ALTER TABLE town_verdicts ADD COLUMN IF NOT EXISTS notes JSONB;

DROP VIEW IF EXISTS api.town_verdicts;
CREATE VIEW api.town_verdicts AS
    SELECT town, state, mode, lat, lon, total, band, scores, notes, best_lodging, food,
           reason, tip, evaluated_at
    FROM town_verdicts;

GRANT SELECT ON api.town_verdicts TO web_anon;
NOTIFY pgrst, 'reload schema';
