# waypoint

Finds worthy small-town road-trip stops — a clean independent place to **sleep**,
good **non-chain food**, and some **town character** — for motorcycle or car trips.
The unit of interest is the **town**: it only qualifies if it has all three.

Built on the [`strands-pgsql-agent-framework`](https://github.com/peterb154/strands-pgsql-agent-framework)
(forked in shape from its `camping-db` example). Data from Google Places API (New);
judgment by Claude on Bedrock.

## Live

Deployed at **https://waypoint.epetersons.com** — a map you click to draw an area and
sweep it (scores every town within a radius, cached so you never re-pay). See `DEPLOY.md`.

## How it works

Per town: geocode → Google Places (lodging + food + attractions) → chain blocklist →
Place Details on the survivors → one Bedrock judgment → a **0–10 score** across lodging
(independence / price / reviews), food (dinner quality + recency), and town (charm +
riding), each with a one-line "why". A lodging gate zeroes towns with nowhere bookable to
sleep. Verdicts cache in Postgres/PostGIS; candidate towns enumerate from the Census
gazetteer via `ST_DWithin`. Trip mode: `moto` (default — no B&Bs) vs `--couple`.

Calibration notes + the scoring rubric are in `CALIBRATION.md`.

## Run locally

```bash
cp .env.example .env                       # GOOGLE_PLACES_API_KEY + AWS creds
docker compose up -d db postgrest          # Postgres (PostGIS) + read API
uv run uvicorn server:app --port 8000      # map + API -> http://localhost:8000
```

CLI helpers:

```bash
uv run python verdict.py "Stanley, ID"     # score one town
uv run python area.py "Dubuque, IA" 30     # sweep an area (moto); add --couple
```
