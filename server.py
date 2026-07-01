"""Minimal local server for the map: serves the UI, reads cached verdicts, and
runs area sweeps live (SSE). This is the seed of the deployable agent service —
the FastAPI /chat + tools + email get added on top for the LXC step.

    uv run uvicorn server:app --reload --port 8000
"""

from __future__ import annotations

import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

import area
import cache

load_dotenv(override=True)

app = FastAPI(title="motel-db")

_COLS = ("town, state, mode, lat, lon, total, band, scores, notes, best_lodging, food, "
         "reason, tip, evaluated_at")


@app.get("/api/verdicts")
def verdicts():
    """All cached verdicts with coords (feeds the map)."""
    conn = cache.connect()
    with conn.cursor() as cur:
        cur.execute(f"SELECT {_COLS} FROM town_verdicts WHERE lat IS NOT NULL")
        cols = [d.name for d in cur.description]
        rows = [dict(zip(cols, r, strict=True)) for r in cur.fetchall()]
    conn.close()
    return rows


@app.get("/api/preview")
def preview(lat: float, lon: float, radius: float, mode: str = "moto"):
    """How many towns fall in the circle, and how many still need scoring — so a
    sweep's cost/time is known before launching it."""
    conn = cache.connect()
    towns = cache.towns_within(conn, lat, lon, radius)
    cached = sum(1 for t in towns if cache.get_cached(conn, t["name"], t["state"], mode))
    conn.close()
    return {"towns": len(towns), "cached": cached, "to_score": len(towns) - cached}


@app.get("/sweep")
def sweep(lat: float, lon: float, radius: float, mode: str = "moto", refresh: bool = False):
    """Stream (SSE) each town's verdict as it's scored/pulled from cache."""

    def gen():
        conn = cache.connect()
        towns = cache.towns_within(conn, lat, lon, radius)
        yield _sse({"event": "start", "towns": len(towns)})
        for i, t in enumerate(towns, 1):
            cached = None if refresh else cache.get_cached(conn, t["name"], t["state"], mode)
            if cached:
                r, src = cached, "cache"
            else:
                r = area.score_town(t["name"], t["lat"], t["lon"], mode)
                cache.store_verdict(conn, t["name"], t["state"], t["geoid"], mode,
                                    t["lat"], t["lon"], r)
                src = "scored"
            yield _sse({
                "event": "town", "src": src, "i": i, "n": len(towns),
                "town": t["name"], "state": t["state"], "lat": t["lat"], "lon": t["lon"],
                "total": r.get("total"), "band": r.get("band"),
            })
        conn.close()
        yield _sse({"event": "done"})

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


def _sse(obj) -> str:
    return f"data: {json.dumps(obj, default=str)}\n\n"


# Static map UI at / (mounted last so /api/* and /sweep win).
app.mount("/", StaticFiles(directory="web", html=True), name="web")
