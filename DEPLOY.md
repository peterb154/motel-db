# Deploying waypoint

The app (**waypoint**, repo `peterb154/waypoint`) is deployed as a Docker Compose stack on a
Proxmox LXC.

- **Live:** https://waypoint.epetersons.com (map + `/api/*` + `/sweep`)
- **LXC:** CT 122 on Proxmox1, `192.168.0.34`, `/opt/waypoint`
- **Stack:** `db` (pgvector + PostGIS) · `postgrest` (:3001, read/tune API) · `agent` (FastAPI `server.py`, :8000)
- **Reachability:** Pi-hole A record → NPM (CT 103) → the LXC, Let's Encrypt cert (Route53 DNS-01)

## Auto-deploy

Push to `main` → GitHub webhook → n8n `Deploy: waypoint` → `POST /api/deploy` (bearer
`DEPLOY_TOKEN`) → the app touches `/opt/waypoint/.deploy-trigger` → host systemd
`waypoint-deploy.path`/`.service` → `deploy.sh` (`git reset --hard origin/main` +
`docker compose up -d --build`). `GET /api/health` reports the deployed commit.

## Secrets (`/opt/waypoint/.env`, chmod 600, not in git)

`DEPLOY_TOKEN`, `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` (IAM user
`waypoint-epetersons-com`, `bedrock:InvokeModel` only), `AWS_REGION`, `STRANDS_PG_MODEL_ID`,
`GOOGLE_PLACES_API_KEY` (IP-locked to the house WAN — the LXC egresses that IP).
`STRANDS_PG_DSN` is set by docker-compose.

## Data

Migrations (`migrations/*.sql`) and the 32k-town Census reference load run automatically on
container start (`entrypoint.sh` → `scripts/migrate.py` + `scripts/ingest_towns.py`). The
verdict cache is the LXC's own; migrate a local cache with
`pg_dump --data-only --table=town_verdicts` → `psql` on the LXC.

## DNS gotcha (LXC-only, not in the repo)

The LAN advertises IPv6 with no working route, so Docker tried IPv6 and failed. Fixed on the
LXC: IPv6 disabled, a local `dnsmasq` with `filter-AAAA` + reliable upstreams, and Docker's
container DNS pointed at the docker0 gateway (`172.17.0.1`). Needed if the container is ever
rebuilt from a fresh template.

## Rebuild from scratch

`pct create` (Ubuntu 22.04, `nesting=1,keyctl=1`) → clone into `/opt/waypoint` →
`bash bootstrap-lxc.sh` → apply the DNS gotcha above → `cp .env.example .env` and fill →
`docker compose up -d --build`.

<!-- deployed via GitHub push -> n8n -> /api/deploy (auto) -->
<!-- auto-deploy test 2026-07-01T22:42:18Z -->
