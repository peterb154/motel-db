# motel-db

A personal agent that finds **clean independent motels in small towns that also
have good non-chain food**, for motorcycle road-trip planning. The unit of
interest is the **town**: it only qualifies if it has *both* an independent motel
worth a look AND a good non-chain place to eat.

Built on the [`strands-pgsql-agent-framework`](https://github.com/peterb154/strands-pgsql-agent-framework)
(forked in shape from its `camping-db` example). Data from Google Places API (New).

## Phase 1 — bare loop (current)

Single town in → Places lookup → chain blocklist filter → one Bedrock judgment
call → printed verdict. No database. The goal is to tune the prompt + blocklist
against towns where the answer is already known before building anything else.

```bash
cp .env.example .env        # fill in GOOGLE_PLACES_API_KEY
aws sso login --profile css-aws1   # Bedrock judgment needs AWS creds
uv run python verdict.py "Stanley, ID"
```

Files: `places.py` (Places New client + geocode), `chains.py` (chain blocklist +
fuzzy backstop), `verdict.py` (the loop).

## Roadmap

- **Phase 2** — Postgres caching (verdicts + Places pointers; record failures too);
  chain blocklist becomes a tunable table.
- **Phase 3** — GPX corridor input (a point every ~25 mi).
- **Phase 4** — state batch over Census incorporated places.
- **Phase 5** — email interface for on-the-road queries.
