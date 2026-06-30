# Calibration Learnings — Lodging & Food Judgment Layer

Living log of real towns/motels used to tune the judgment prompt. Each entry
is ground truth from Brian's actual experience or research, paired with what
the review data showed, paired with the rule it implies. Add to this file
as new towns get checked — don't let it go stale.

---

## REJECT — 1st Inn Alliance, Alliance, NE

**Verdict:** Independent, clears a ratings bar, but Brian's nose said no —
"zero charm... looked like a week to week rental. Not my scene."

**What the reviews showed:** Price-as-apology language is the tell.
> "Yes, you can pay $119 for a better name, but sometimes the most basic
> and simple is sufficient... We could have spent more, but because Arlene
> was so personable and helpful, she helped sell the room."

A fellow Tripadvisor tip-writer separately warned other travelers: "pick
one somewhere else or see if they have newly remodeled, but I doubt it."

**Rule:** Distinguish *price-as-apology* (reviewer is justifying why they
settled, comparing unfavorably to what they could've gotten) from
*price-as-value* (reviewer is delighted at what they got for the money).
"You CAN pay more for better" = apology. "Best stay for the price, full
stop" = value. Same vocabulary (price, $, "for the money"), opposite
meaning — this can't be a keyword filter, it needs the judgment layer
reading stance, not just topic.

---

## PASS — Covered Wagon Motel, Lusk, WY

**Verdict:** Brian's favorite of the Lusk options — "the place I thought
was perfect."

**What the reviews showed:** Consistent unqualified, sensory, repeat-visit
language across multiple reviews:
> "What a wonderful little motel!... We were surprised to return and find
> our room had been cleaned and our towels replaced, we have not stayed
> anywhere with maid service since the beginning of Covid."

One review was business-travel-coded ("excellent place for inbound non-
touristy Wyoming necessities") and Claude initially over-weighted that
single review as a caution flag. It was wrong to — the review was still
unambiguously positive, just from a different traveler type.

**Rule:** Don't let one outlier-flavored review (e.g. mentions "business")
override a cluster of consistent, specific, sensory, repeat-visit reviews.
Weigh preponderance, not the presence of any single flagged word. A motel
serving both leisure and business travelers well is evidence of being
well-run, not evidence of being generic.

**Also confirmed:** Lusk passes on food but thinly — one real sit-down
option (Silver Dollar Bar and Grill) plus a Subway. "Both bars clear"
rule should pass this, but it's a near-thing, not a slam dunk. Town-level
food strength is a spectrum, not just pass/fail.

---

## PASS — Mountain Spirit Inn, Darby, MT

**Verdict:** "What a cool little place that was."

**What the reviews showed:** The strongest single signal of all four
towns so far — the *owner's own review responses* are personal, specific,
and funny, not templated:
> Guest: "...a real gem in Darby." Owner (Adele) reply: "Regarding gems,
> the Mountain Spirit Inn is gem. However, you can find real gems at
> Crystal Mountain... and also at Gem Mountain along the Skalkaho Pass,
> which is a business where you can pan for Sapphires."

Also: owner mailed a forgotten hat and a forgotten pillow back to guests
at no charge, unprompted, more than once (different guests, different
trips) — a repeated pattern, not a one-off.

**Rule:** Owner-responds-to-reviews is a strong, *structurally available*
signal (Places data shows whether/how a business replies). Template
replies ("Thank you for your feedback!") are neutral-to-weak. Specific,
personality-laden, individualized replies are a strong positive — often
stronger than guest review text itself, because it's the owner's own
unfiltered voice.

**Caution surfaced:** Listing mentioned "extended stay/weekly rates" —
structurally identical to the Alliance red flag. But context made it a
non-issue: it was one listed amenity among overwhelmingly leisure-
traveler reviews (skiers, hunters, road-trippers), not the dominant use
case. **"Offers weekly rates" alone is not the tell. "Weekly rates is the
dominant pattern in actual reviews" is.** Same structural fact, opposite
meaning depending on what the review corpus actually shows — this is
why it has to be a judgment call on the whole picture, not a rule on a
single field.

---

## PASS — Georgetown Mountain Inn, Georgetown, CO

**Verdict:** Loved it.

**What the reviews showed:** Larger, more conventional operation (33
rooms, 2 stories, pool/hot tub) than the other three — reads as "well-run
small hotel" more than "owner's personality is the whole place." Reviews
skew toward competent-and-consistent rather than personality-driven:
"friendly and helpful staff, comfortable, clean rooms" — genuinely the
most generic-sounding praise of the four. A couple of minor gripes
showed up too (dusty cabinets, a cold room one morning, one review
mentioning a torn box spring under the bed) — nothing disqualifying.

**Food-proximity signal, explicit in reviews:**
> "It is well within walking distance to tasty food..."
> "The next door restaurant/bar fit in great with my way of travel."
> "...our favorite restaurant Coopers on The Creek!"

**Rule (Brian's explicit framing):** *"Nice restaurants don't usually
exist next to a hell hole drug den."* Food quality and proximity isn't
just a separate checklist item to verify alongside lodging — it's
corroborating evidence about the town/block itself. A good named,
specifically-loved restaurant mentioned unprompted in a motel's own
reviews is a signal about the surrounding area, not just about dinner.
Weigh it as such.

**Also confirmed:** A motel doesn't need to be tiny or owner-personality-
driven to pass. "Competent, well-run, real town, good food nearby" is a
valid pass even without an Adele. Don't over-index Phase 1 calibration
toward only rewarding the most charming/personal cases — Georgetown shows
the bar admits solid-but-unspectacular too, as long as the fundamentals
(independent, clean, good food nearby, no major complaints) hold.

---

## PASS (with texture) — Hotel Seville, Harrison, AR

**Verdict:** Brian loves it. Notable: this is the first entry that's not a
motel at all — a 55-room, 1929-era full-service historic hotel with a bar
and restaurant, soft-branded as part of Choice Hotels' "Ascend Hotel
Collection."

**New wrinkle — soft brands aren't the same as flagged brands.** "Ascend
Hotel Collection" is Choice's affiliation tier for independently owned,
individually-named historic/boutique properties — they keep their own
identity and character but tap into a chain's booking/loyalty system. A
flat blocklist match on "Choice Hotels" or "Ascend" would wrongly kill
this one. **Rule: the blocklist needs a soft-brand exception list**
(Ascend Hotel Collection, Tapestry Collection by Hilton, Tribute Portfolio
by Marriott, Curio Collection by Hilton, Autograph Collection — these are
explicitly "independent character, chain-affiliated" tiers) distinct from
flagged full chain brands (Quality Inn, Comfort Inn, Holiday Inn Express,
etc., which are also technically Choice/IHG but are standardized,
interchangeable builds).

**What the reviews showed — best example yet of "good but uneven," not
flawless:**

Strong, specific, can't-be-faked praise:
> "Bar and restaurant on site with excellent food and a very friendly
> bartender. Centrally located to some of the best riding in Arkansas and
> Missouri." (unprompted moto-relevant detail — high-value signal)

Real, clustered, legitimately negative reviews sitting right next to it:
> "room was directly over the bar so we didn't get any sleep until after
> midnight. The hotel over promises and under performs."
> "First, the restaurant is a joke. Basically hotdogs and chili. Then,
> something went wrong with the water system and the water was cut off,
> without explanation, for about an hour."
> "The walls are paper thin so we could hear everything going on the next
> room."

Multiple independent reviewers converge on the same complaint pattern
("could have been nice but...", "over promises and under performs") —
old building, mid-renovation, restaurant under separate sub-let
management so quality is inconsistent and disconnected from the hotel's
own management.

**Rule:** This is a different failure-adjacent pattern than anything else
logged so far — not fake/generic (Alliance), not an outlier review to
discount (Lusk). It's **a real, charming, worth-it place with genuine
inconsistency**, openly acknowledged by multiple reviewers in similar
language. Don't auto-penalize a cluster of specific operational
complaints (noise, an under-construction feel, a so-so sub-let
restaurant) the way a cluster of *generic* complaints should be
penalized. The texture is: complaints are specific, varied in topic, and
sit alongside equally specific praise — that combination reads as "real
old building with real character and real flaws," which is a pass, not
a borderline case. A town/property log should be able to say "great, but
ask for a room not over the bar" — that's a usable verdict, not a wishy-
washy one.

**Food note:** Restaurant-on-site quality is explicitly inconsistent here
(excellent per one review, "basically hotdogs and chili" per another) —
this is a case where the *hotel* passes clearly but the on-site food
specifically should not be the sole food signal for the town. Worth
checking Harrison's separate food options rather than resting on the
hotel's own restaurant.

## Running rule set (cumulative, plain-language)

1. **Price-as-apology vs. price-as-value.** Read the stance, not just
   whether price is mentioned.
2. **Preponderance over outliers.** One oddly-flavored review shouldn't
   override a cluster of consistent positive ones.
3. **Owner review-response quality is a strong, cheap, structural signal.**
   Specific > templated. Look at it as seriously as guest review text.
4. **Structural facts (e.g. "weekly rates offered") need context, not a
   blanket penalty.** Ask whether it's the dominant use case in the
   reviews or a side option.
5. **Food proximity corroborates the town/block, not just dinner plans.**
   A good, specifically-named restaurant mentioned inside a motel's own
   reviews is evidence about the surrounding area's character.
6. **The bar isn't "must be charming/personality-driven."** Competent and
   well-run, in a real town, with food nearby and no major complaints, is
   a legitimate pass even without an owner-personality angle.
7. **Soft chain brands (Ascend, Tapestry, Tribute Portfolio, Curio,
   Autograph Collection) are not the same as flagged chain brands.** They
   affiliate independently-named/run historic or boutique properties with
   a booking system. Blocklist needs to whitelist these explicitly rather
   than matching on the parent company name.
8. **Specific, varied, real complaints sitting next to specific, real
   praise = an honest "good but uneven" pass, not a red flag.** This is
   different from generic complaints (weak signal either way) and
   different from a single outlier review (rule 2). Multiple reviewers
   independently converging on the same specific gripe (e.g. "room over
   the bar," "restaurant under separate management is hit or miss") is
   useful, actionable detail to surface in the verdict, not a reason to
   fail the town.

## Still needed
- **A known REJECT for a town that looked fine on paper but Brian knows
  is a miss** (other than Alliance, which we do have). A second reject
  example, ideally one that *isn't* the price-apology pattern, would
  reveal a different failure mode. Without variety in the rejects, the
  judgment layer only learns to catch one type of bad town.

---

## Composite Scoring Model v1

Output: a score from 0–10. Towns scoring below ~5 are filtered out.
Towns scoring 7+ are strong candidates. 5–7 are "acceptable if the
corridor goes there, wouldn't build a day around it."

### Lodging (5 pts)

**Independence & Character (2 pts)**
- 2 — Clearly independent, character evident in reviews (named owner, specific decor, personality-driven praise, owner responses individualized)
- 1 — Independent but generic execution, or soft-brand affiliated (Ascend, Tapestry, Tribute Portfolio, Curio, Autograph Collection)
- 0 — Chain (blocklist hit, excluding soft-brand exceptions)

**Price Tier Signal (1.5 pts)**
- 1.5 — No price-apologetics; price not mentioned or mentioned as pleasant surprise for value delivered
- 0.75 — Mixed: some value-qualified praise offset by unqualified praise
- 0 — Price-as-apology dominant ("decent for the money," "you can pay more for better," "budget option but")

**Review Quality (1.5 pts)**
- 1.5 — Specific, sensory, repeat-visit; owner responses individualized; complaints if present are specific and offset by equally specific praise
- 1.0 — Generally positive but generic
- 0.5 — Mixed: real praise alongside real clustered complaints (legitimate "good but uneven" — don't auto-fail)
- 0 — Thin, generic, or dominant complaint pattern

### Food (3 pts)

**Proximity & Quality (2 pts)**
- 2 — Non-chain restaurant within walking distance, specifically named in lodging reviews
- 1.5 — Good food nearby, mentioned in reviews but not named/specific
- 1.0 — Food exists, not mentioned in lodging reviews
- 0 — Chain-only, dead food scene, or poor on-site only option

**Recency (1 pt)**
- 1.0 — Strong reviews within 18 months
- 0.5 — Older reviews or mixed recency
- 0 — No recent signal or evidence of closure

### Town Fit (2 pts)

**Leisure vs. Workforce Character (1 pt)**
- 1 — Dominated by through-travelers, recreationists, road-trippers, repeat leisure visitors
- 0.5 — Mixed leisure and workforce
- 0 — Workforce/industrial dominant, weekly-rate pattern common

**Riding Context (1 pt)**
- 1 — On or near known good riding; reviews mention riding or outdoor recreation unprompted
- 0.5 — General outdoor/tourism area, no specific riding signal
- 0 — No recreational context, pure transit or freight town

---

## Town Scores

| Dimension | Alliance NE | Lusk WY | Darby MT | Georgetown CO | Harrison AR |
|---|---|---|---|---|---|
| Independence & Character | 1.0 | 2.0 | 2.0 | 1.5 | 1.5 |
| Price Tier Signal | 0.0 | 1.5 | 1.5 | 1.0 | 0.75 |
| Review Quality | 0.5 | 1.5 | 1.5 | 1.0 | 0.5 |
| Food Proximity & Quality | 0.5 | 1.5 | 2.0 | 2.0 | 1.0 |
| Food Recency | 0.5 | 0.5 | 1.0 | 0.75 | 0.5 |
| Leisure vs. Workforce | 0.0 | 0.75 | 1.0 | 1.0 | 0.75 |
| Riding Context | 0.0 | 0.5 | 1.0 | 0.5 | 1.0 |
| **TOTAL** | **2.5** | **8.25** | **10.0*** | **7.75** | **6.0** |

*Darby scores ceiling on this rubric but is realistically 8.5–9 in a larger corpus. Relative ordering is what matters: Darby > Lusk > Georgetown > Harrison >> Alliance.

**Score interpretation:**
- 8–10: Route-worthy — build a day around this town
- 6–7.9: Acceptable — good stop if the corridor goes there
- 4–5.9: Marginal — surface with a warning, let the human decide
- <4: Filter out
