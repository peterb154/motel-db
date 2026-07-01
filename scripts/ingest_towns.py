"""Load US place reference data (Census 2023 Gazetteer) into the towns table.

Idempotent: if towns already has rows, do nothing. Otherwise stage the raw
tab-delimited gazetteer file, insert into towns, then apply the proven
name-cleaning UPDATEs (strip the "city"/"town"/... suffix and rebuild
search_text).
"""

from __future__ import annotations

import os
from pathlib import Path

import psycopg

DSN = os.environ.get("STRANDS_PG_DSN", "postgresql://strands:strands@localhost:5433/strands")
GAZ_FILE = Path(__file__).resolve().parent.parent / "data" / "2023_Gaz_place_national.txt"

# Suffixes the Census appends to place names; stripped so "Dubuque city" -> "Dubuque".
NAME_SUFFIX_RE = (
    r"\s+(city|town|village|CDP|borough|municipality|comunidad|zona urbana|"
    r"township|plantation|gore|grant|urban county|unified government|"
    r"metropolitan government|consolidated government|corporation)$"
)


def main() -> None:
    conn = psycopg.connect(DSN)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM towns")
            if cur.fetchone()[0] > 0:
                print("towns already loaded")
                return

            cur.execute(
                """
                CREATE TEMP TABLE gaz_stage (
                    usps        TEXT,
                    geoid       TEXT,
                    ansicode    TEXT,
                    name        TEXT,
                    lsad        TEXT,
                    funcstat    TEXT,
                    aland       TEXT,
                    awater      TEXT,
                    aland_sqmi  TEXT,
                    awater_sqmi TEXT,
                    intptlat    TEXT,
                    intptlong   TEXT
                )
                """
            )

            with (
                GAZ_FILE.open("r", encoding="utf-8") as fh,
                cur.copy(
                    "COPY gaz_stage FROM STDIN WITH (FORMAT csv, DELIMITER E'\t', HEADER true)"
                ) as copy,
            ):
                for line in fh:
                    copy.write(line)

            cur.execute(
                """
                INSERT INTO towns (geoid, name, state, lat, lon, location, lsad, search_text)
                SELECT
                    trim(geoid),
                    trim(name),
                    trim(usps),
                    trim(intptlat)::float,
                    trim(intptlong)::float,
                    ST_SetSRID(
                        ST_MakePoint(trim(intptlong)::float, trim(intptlat)::float), 4326
                    )::geography,
                    trim(lsad),
                    trim(name) || ' ' || trim(usps)
                FROM gaz_stage
                ON CONFLICT (geoid) DO NOTHING
                """
            )
            inserted = cur.rowcount

            cur.execute(
                "UPDATE towns SET name = regexp_replace(name, %s, '', 'i')",
                [NAME_SUFFIX_RE],
            )
            cur.execute("UPDATE towns SET search_text = name || ' ' || state")
        conn.commit()
        print(f"[ingest_towns] loaded {inserted} towns")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
