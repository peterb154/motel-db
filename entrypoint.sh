#!/usr/bin/env bash
# Wait for Postgres, apply migrations, ingest town reference data,
# then exec the agent command.
set -e

: "${STRANDS_PG_DSN:?STRANDS_PG_DSN is required}"

echo "[entrypoint] waiting for Postgres..."
python - <<'PY'
import os, sys, time
import psycopg

dsn = os.environ["STRANDS_PG_DSN"]
deadline = time.time() + 60
last = None
while time.time() < deadline:
    try:
        with psycopg.connect(dsn, connect_timeout=3) as c:
            c.execute("SELECT 1")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        last = exc
        time.sleep(1)
print(f"[entrypoint] Postgres not reachable: {last}", file=sys.stderr)
sys.exit(1)
PY

echo "[entrypoint] applying migrations..."
python scripts/migrate.py

echo "[entrypoint] ingesting town reference data..."
python scripts/ingest_towns.py

echo "[entrypoint] starting: $*"
exec "$@"
