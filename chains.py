"""Chain blocklist — the core IP. Phase 1 keeps it as an in-code list so we can
tune it fast against the calibration towns; Phase 2 moves it to a Postgres table.

is_chain(name) -> (bool, matched_term). Normalized substring match first, then a
fuzzy backstop (difflib) to catch variants/misspellings of single-token brands.
"""

from __future__ import annotations

import re

# Lodging chains. Includes the sneaky parent-brand ones called out in the brief
# (Super 8 / Days Inn / Travelodge / Howard Johnson / Microtel are all Wyndham).
LODGING_CHAINS = [
    # Wyndham
    "super 8", "days inn", "travelodge", "howard johnson", "microtel", "ramada",
    "baymont", "la quinta", "wingate", "americinn", "hawthorn", "wyndham",
    "echo suites", "trademark collection", "dazzler", "esplendor",
    # Choice
    "comfort inn", "comfort suites", "quality inn", "sleep inn", "econo lodge",
    "rodeway", "mainstay", "clarion", "cambria", "ascend", "woodspring",
    "suburban studios",
    # IHG
    "holiday inn", "holiday inn express", "candlewood", "staybridge", "avid",
    "atwell suites", "even hotels",
    # Marriott
    "fairfield inn", "courtyard", "springhill", "towneplace", "residence inn",
    "moxy", "ac hotel", "four points", "aloft", "element",
    # Hilton
    "hampton inn", "hampton by hilton", "hilton garden", "home2", "tru by hilton",
    "doubletree", "homewood", "embassy suites", "spark by hilton",
    # Best Western family
    "best western", "surestay", "glo ",
    # Economy / extended stay / others
    "motel 6", "studio 6", "red roof", "extended stay america", "g6",
    "cobblestone", "boarders inn", "sonesta", "red lion", "knights inn",
    "americas best value", "budget inn", "budget host", "passport inn",
    "national 9", "surestay", "vagabond inn", "shilo inn", "oyo", "signature inn",
    "magnuson", "scottish inns", "select inn", "town house motel",
]

# Restaurant / fast-food / chain-food blocklist. Food bar is more forgiving, but
# we still drop the obvious national chains so the judgment focuses on local food.
FOOD_CHAINS = [
    "mcdonald", "subway", "burger king", "wendy", "taco bell", "kfc",
    "kentucky fried", "pizza hut", "domino", "papa john", "papa murphy",
    "little caesar", "arby", "dairy queen", "sonic drive", "hardee", "carl's jr",
    "jack in the box", "culver", "a&w", "jimmy john", "chipotle", "panera",
    "starbucks", "dunkin", "denny", "ihop", "applebee", "chili's", "perkins",
    "village inn", "cracker barrel", "pizza ranch", "runza", "wingstop",
    "popeyes", "chick-fil-a", "panda express", "five guys", "in-n-out",
    "qdoba", "moe's southwest", "del taco", "whataburger", "sbarro", "quiznos",
    "firehouse subs", "jersey mike", "tim hortons", "long john silver",
    "golden corral", "olive garden", "outback", "red lobster", "texas roadhouse",
    "buffalo wild wings", "dutch bros", "baskin", "cold stone", "jamba",
    "noodles & company", "raising cane", "zaxby", "bojangle", "church's chicken",
    "hardees", "dq grill", "mcalister", "pizza factory", "godfather's pizza",
    "round table pizza", "blimpie", "schlotzsky",
]

ALL_CHAINS = LODGING_CHAINS + FOOD_CHAINS

_PUNCT = re.compile(r"[^a-z0-9 ]+")


def _normalize(text: str) -> str:
    """Lowercase, punctuation -> spaces, collapse whitespace."""
    return " ".join(_PUNCT.sub(" ", text.lower()).split())


# Pre-normalize blocklist terms so matching is apples-to-apples with names
# (e.g. "a&w" -> "a w", "chick-fil-a" -> "chick fil a"). Keep the original for
# readable logging.
_NORM_CHAINS = [(t, _normalize(t)) for t in ALL_CHAINS]
_NORM_CHAINS = [(orig, norm) for orig, norm in _NORM_CHAINS if norm]


def is_chain(name: str) -> tuple[bool, str | None]:
    """Return (is_chain, matched_term).

    Word-boundary match: a blocklist term must begin at the start of a word in
    the name, but may continue past it — so the stem "mcdonald" still catches
    "mcdonalds" while "arby" no longer matches "darby". Fuzzy/variant matching
    is deferred to Phase 2 (pg_trgm in Postgres).
    """
    norm = _normalize(name)
    if not norm:
        return False, None
    haystack = " " + norm  # leading space gives the first word a left boundary
    for orig, term in _NORM_CHAINS:
        if (" " + term) in haystack:
            return True, orig
    return False, None


def filter_independents(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split candidates into (independents, dropped_chains)."""
    keep, dropped = [], []
    for c in candidates:
        chain, term = is_chain(c.get("name", ""))
        if chain:
            dropped.append({**c, "matched_chain": term})
        else:
            keep.append(c)
    return keep, dropped
