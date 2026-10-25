# Windfall or Wind Break: How Weather Skews Totals

**Published:** 2026-08-31
**Amended:** 2026-10-24 — headline claims withdrawn after failed replication
**Status:** Mechanism note only. No stakable totals claim survives.

> **Amendment notice.** The original version of this note claimed that wind above 20 kph reduced total goals by ~10% (~0.3 goals per match), that coastal grounds were disproportionately affected, and that bettors should fade overs at exposed grounds. All three were tested against the project's own data on 2026-10-24 and none held. See `2026-10-24-wind-fails-to-replicate.md` for the full replication study and `src/analysis/wind_analysis.py` for the code. The claims are withdrawn below and the reasoning retained as explicitly untested.
>
> **Note also:** `research/public/2026-08-03-weather-wind.md` had already tested this hypothesis and marked it **Rejected** on 2026-08-03 — four weeks before this note was published asserting the opposite. This note should never have been written in this form. That failure is documented in the replication study.

## Bottom Line Up Front

- **Wind shows no reliable goals effect in our data (n=241, −5.8%, p=0.46). Do not stake on wind totals.**
- The claimed coastal effect reverses on test: coastal **+0.15** goals vs inland **−0.22**, p=0.82.
- Wind + rain does not produce the claimed −0.5 goals: observed −0.38, p=0.20.
- The corners claim — "back the end with the wind" — cannot be tested with our data (no bearing, no pitch orientation). An orientation-free variance test finds no asymmetry inflation (r=+0.004, p=0.96).
- **Action:** none on totals. The only signal worth tracking is a fouls/cards lead in genuine storms, and it is too fragile to stake.

## What Was Withdrawn

| Original claim | Test | Observed | Outcome |
|---|---|---|---|
| Wind >20 kph cuts goals ~10% | t-test, 92 calm vs 149 windy | −5.8%, p=0.46 | Withdrawn |
| Goals drop ~0.3/match | mean difference | −0.163, CI [−0.60,+0.27] | Withdrawn |
| Wind + rain: −0.5 goals | wet-windy vs dry-calm | −0.379, p=0.20 | Withdrawn |
| Coastal grounds hit hardest | coastal vs inland | +0.15 vs −0.22, p=0.82 | Withdrawn (sign reverses) |
| First-half scoring most affected | FH goals vs wind | r=+0.05, p=0.46 | Withdrawn |
| Corners: back the end with the wind | needs bearing | no direction data | Untestable |

Sample: 241 Premier League fixtures, 2003-08-24 to 2016-05-15, venue-level weather joined from the legacy Open-Meteo files.

## The Read — Mechanism, Explicitly Untested

Weather data is increasingly available, and the betting market does tend to treat rain and wind as a binary "bad weather" flag rather than a nuanced performance modifier. That framing is plausible.

The mechanism is also plausible: wind plausibly degrades long-pass accuracy, crossing, and goalkeeper distribution, all of which would suppress scoring. **This remains reasoning, not measurement.** Nothing in our data confirms it, and the specific magnitudes the original note asserted were wrong.

Two things the original note got wrong at the level of reasoning, not just arithmetic:

- **Exposure is not the same as effect.** Naming St James' Park, St Mary's and Pittodrie as the worst-affected grounds is a claim about a subset selected *for being windy*. Testing the whole sample shows coastal grounds scoring slightly **more** in wind than inland ones. That is the signature of a pattern fitted to noise.
- **"The market hasn't priced it" needs evidence too.** Asserting bookmaker totals don't shift enough for wind requires a comparison of closing lines against realised outcomes. The original note never made that comparison.

## Key Numbers — Replaced With Tested Results

```
calm  (<=20 kph)  n= 92   goals = 2.793
windy ( >20 kph)  n=149   goals = 2.631
delta = -0.163 goals (-5.8%)    p = 0.46
```

The effect is less than half the originally claimed magnitude and indistinguishable from zero. A threshold scan across 16 cut-points from 15 to 37.5 kph found no cut producing significance; the minimum p was 0.12 at 35 kph, which fails Bonferroni correction (p×16 = 1.92).

**What does survive, tentatively.** Isolating the cell that resembles a genuine storm — wind >35 kph and rain >2 mm (n=29):

| Metric | Storm cell | Rest | Shift | p |
|---|---|---|---|---|
| Total fouls | 19.86 | 22.04 | −9.9% | 0.030 |
| Total cards | 2.52 | 3.29 | −23.4% | 0.019 |
| Second-half goals | 1.17 | 1.57 | −25.4% | 0.038 |
| Total goals | 2.31 | 2.75 | −15.8% | 0.096 |
| Total corners | 10.90 | 11.03 | −1.2% | 0.878 |

Seven metrics were tested on a 29-match cell; the Bonferroni threshold is p<0.007 and **nothing clears it**. The cell was also selected after observing that the full-sample test failed. Record it as a hypothesis with a coherent physical story — a scrappy, low-continuity game with fewer reckless challenges — not as an edge.

## Market Inefficiency — Unproven

The original note claimed weather lines are set late and don't reflect real-time conditions, and that bettors monitoring live weather gain an edge before the market catches up.

**This has not been tested and should not be assumed.** Testing it requires closing-line data paired with realised outcomes across a large sample of weather-affected fixtures. We hold no closing-line history. Until that exists, treat "the market hasn't priced the wind" as an untested hypothesis, not a finding.

## Betting Actions — Downgraded to Untested Hypotheses

| Market | Trigger | Original action | Status |
|---|---|---|---|
| Total goals | Wind >20 kph + exposed stadium | Fade over | **Withdrawn** — no effect found |
| In-play | Wind-affected early play + no goal by 30 min | Live under | **Untested** — no in-play data |
| Corners | Wind blowing toward one goal | Back end with wind advantage | **Untestable** — no bearing or pitch-orientation data |
| Fouls / cards | Wind >35 kph + rain >2 mm | — | **Hypothesis only** — p=0.03–0.02 on n=29, fails multiple-comparison correction |

None of these is a staking instruction. The first is positively contradicted by the data.

## Data Gaps That Block a Real Test

| Gap | Consequence |
|---|---|
| No gust data in the legacy files | Storms are defined by gusts (55–80 kph), not sustained speed. The sample never measured the variable that matters. |
| No wind bearing or pitch orientation | The one mechanism with a clean within-match test — half with the wind vs half against, opponent strength cancelling — cannot be run. |
| English Premier League only | Every ground where this advice would actually be used — Scottish, lower English divisions — is absent. |
| Only 17 of 241 matches exceed 40 kph | Storm conditions are extrapolation, not interpolation. |
| ~28% power to detect a 10pp shift | Absence of significance is **not** evidence of absence. The effect could be real and this sample cannot see it. |

The power point cuts both ways and must be stated plainly: this note does not prove wind is irrelevant. It proves the specific, stakable claims the original version made are not supported by the evidence the original version cited.

## Confidence

**None** for totals until the gust backfill completes. **None** for in-play (no data). **None** for corners (untestable as things stand). **Low** on the fouls/cards storm lead — physically plausible, statistically fragile, post-hoc selected.

## See Also

- `2026-10-24-wind-fails-to-replicate.md` — full replication study, method, and the build that would settle it
- `src/analysis/wind_analysis.py` — reproduces every number in this note from source
- `scripts/capture_wind_events.py` — logs windy fixtures with pre-match weather for future out-of-sample testing
