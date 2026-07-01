"""Apply numbered SQL migrations idempotently.

Tracks applied files in schema_migrations. Each file runs in its own
transaction; only files not yet recorded are applied. Migrations are
themselves idempotent (IF NOT EXISTS / CREATE OR REPLACE), so re-running
across restarts is safe.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import psycopg

DSN = os.environ.get("STRANDS_PG_DSN", "postgresql://strands:strands@localhost:5433/strands")
MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"


def _num(path: Path) -> int:
    m = re.match(r"(\d+)", path.name)
    return int(m.group(1)) if m else 0


def main() -> None:
    conn = psycopg.connect(DSN)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    filename   TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ DEFAULT now()
                )
                """
            )
        conn.commit()

        with conn.cursor() as cur:
            cur.execute("SELECT filename FROM schema_migrations")
            applied = {row[0] for row in cur.fetchall()}

        files = sorted(MIGRATIONS_DIR.glob("*.sql"), key=_num)
        for path in files:
            if path.name in applied:
                continue
            sql = path.read_text()
            with conn.cursor() as cur:
                cur.execute(sql)
                cur.execute(
                    "INSERT INTO schema_migrations (filename) VALUES (%s)", [path.name]
                )
            conn.commit()
            print(f"[migrate] applied {path.name}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
