# Wind Does Not Do What We Said It Does: A Failed Replication and What Survives

**Published:** 2026-10-24
**Supersedes (in part):** `windfall-or-wind-break-weather-skews-totals.md` (2026-08-31)
**Status:** Replication failure on headline claim. One exploratory lead. Data gaps documented.

---

## Bottom Line Up Front

- The claim that **wind >20 kph cuts goals by ~10%** does **not** replicate. Observed effect is **−5.8%**, p = 0.46. 95% CI [−0.60, +0.27] goals.
- The claim that **coastal grounds are disproportionately affected** reverses in the data: coastal **+0.15** goals vs inland **−0.22**, p = 0.82.
- The claim that **first-half scoring is most affected** is unsupported: r = +0.05, p = 0.46.
- The claim to **back the end with the wind** cannot be tested — we hold no wind bearing data, and an orientation-free variance test finds **no asymmetry inflation** (r = +0.004, p = 0.96).
- **What survives:** in the extreme cell (wind >35 kph + rain >2 mm, n=29), fouls fall 9.9% (p=0.030), cards fall 23.4% (p=0.019), second-half goals fall 25.4% (p=0.038). None survives Bonferroni correction for seven tests. This is a lead, not a finding.
- **Action:** stop publishing wind-based totals advice until the gust and bearing backfill is complete. The current library note is overstated and should not drive staking.

---

## Why This Note Exists

On 24 October 2026, Storm Boelo brought a Met Office yellow wind warning to the UK — gusts of 55–65 mph widely, 70–80 mph on exposed coasts, strongest across Scotland and the far north of England. Rain totals of 9–13 mm fell across Scottish grounds in the three hours around kick-off.

A day like that is the natural test case for `windfall-or-wind-break-weather-skews-totals.md`, which advises *"fade overs at exposed grounds when wind speeds exceed 20 kph"* and asserts a ~10% goals reduction with ~0.3 goals per match.

Before applying that advice to a live card, the claim was tested. It did not hold.

## The Note Contradicted Our Own Earlier Work

This is the part that matters more than the statistics.

`research/public/2026-08-03-weather-wind.md`, **created 2026-08-03 and marked Status: Rejected**, concluded:

> - Wind speed does not show a meaningful relationship with total goals.
> - Corners are not significantly affected by wind either.
> - The 'wind factor' is mostly noise in this dataset.

The library note asserting a ~10% goals reduction was **published 2026-08-31 — twenty-eight days later** — with no reference to that rejection, no new data, and no code.

So this is not a case of a hypothesis that looked true and later failed. The project had already tested wind and rejected it. The library note then published the opposite, with specific magnitudes and staking instructions attached. The replication below independently reaches the same conclusion as the August public note, which is reassuring for the method and damning for the process.

**The process failure to fix:** nothing connected the public research stream to the library. A claim can enter the library contradicting a rejected public finding, and no gate catches it. Two things would have prevented this — requiring a reproducing script before a library claim is accepted (now done for wind, see `src/analysis/wind_analysis.py`), and checking the library against prior public findings on the same topic before publishing.

---

## The Test

**Data.** The 286 legacy per-match Open-Meteo files under `data/raw/open-meteo/` (`weather_<ref_id>_<date>.csv`) carry daily aggregates: `wind_speed_10m_max`, `wind_gusts_10m_max`, `precipitation_sum`, `temperature_2m_max`.

**Join.** Legacy files carry coordinates but no team identity. Each was mapped to its nearest stadium via a manual ground registry, then joined to `data/processed/match_master_table.csv` on `(date, HomeTeam)`.

**Result.** 278 legacy weather rows → **241** matched Premier League fixtures, 2003-08-24 to 2016-05-15. The remainder were played at grounds with no coordinate match or fell outside the master table.

**Methods.** Welch t-tests, Pearson correlation, likelihood-ratio tests against intercept-only logits, two-way ANOVA, 10,000-sample bootstrap, Levene variance tests, and a power calculation.

---

## Claim-by-Claim Results

| Claim | Test | Result | Verdict |
|---|---|---|---|
| Wind >20 kph cuts goals ~10% | t-test, 92 calm vs 149 windy | −5.8%, p=0.46 | **Fails** |
| Goals drop ~0.3/match | mean difference | −0.163, CI [−0.60,+0.27] | **Fails** |
| Wind + rain: −0.5 goals | wet-windy vs dry-calm | −0.379, p=0.20 | **Fails** |
| Coastal grounds hit hardest | coastal vs inland | +0.15 vs −0.22, p=0.82 | **Reverses** |
| First-half scoring most affected | FH goals vs wind | r=+0.05, p=0.46 | **Fails** |
| Corners: back the end with the wind | needs bearing | no direction data | **Untestable** |

### Detail: the headline claim

```
calm (<=20 kph)  n= 92  goals = 2.793
windy (>20 kph)  n=149  goals = 2.631
delta = -0.163 goals (-5.8%)   p = 0.4633
```

The observed effect is less than half the claimed magnitude and indistinguishable from zero. A threshold scan across 16 cut-points from 15 to 37.5 kph found no threshold producing a significant effect; the minimum p was 0.12 at 35 kph, which fails Bonferroni correction (p×16 = 1.92).

### Detail: the direction claim, tested without bearing data

The library advises backing *"the end with the wind advantage"*. We hold no pitch-orientation or wind-bearing data, so a direct test is impossible. But the mechanism makes a testable prediction: if wind genuinely creates directional asymmetry, then across many matches the **variance** of `(home_corners − away_corners)` must rise with wind, because wind direction relative to pitch varies randomly across fixtures.

It does not:

```
corr(wind, |home_corners - away_corners|) = +0.004   p = 0.956
SD(corner diff):  calm 4.56  |  moderate 4.54  |  strong 5.02
Levene test (calm vs strong): W=0.387, p=0.535
```

No inflation in mean, no inflation in spread. The mechanism is not detectable in this data.

---

## What Survives — and How Much to Trust It

Isolating the cell that resembles a genuine storm (wind >35 kph **and** rain >2 mm, n=29):

| Metric | Extreme cell | Rest | Shift | p |
|---|---|---|---|---|
| Total fouls | 19.86 | 22.04 | −9.9% | 0.030 |
| Total cards | 2.52 | 3.29 | −23.4% | 0.019 |
| Second-half goals | 1.17 | 1.57 | −25.4% | 0.038 |
| Total goals | 2.31 | 2.75 | −15.8% | 0.096 |
| Total corners | 10.90 | 11.03 | −1.2% | 0.878 |

**Do not over-read this.** Seven metrics were tested on a 29-match cell; the Bonferroni-corrected threshold is p < 0.007 and **nothing clears it**. The cell was also selected post hoc after observing that the full-sample test failed — which is exactly the garden of forking paths that produces spurious findings.

What makes it worth recording rather than discarding is that it is physically coherent: in extreme wind and rain, the game breaks into a scrappy, low-continuity contest with fewer reckless challenges. That is a mechanism a coach would recognise. But a mechanism plus p=0.03 on n=29 is a hypothesis, not an edge.

A separate exploratory signal: home **shot** advantage declines monotonically with wind — +3.17 shots (calm) → +2.80 (moderate) → +2.26 (strong). But the trend is not significant (r=−0.040, p=0.53), and home **win rate** moves the wrong way for a "wind is a leveller" story (39.1% → 31.0% → 44.6%, non-monotonic). Do not build on this.

---

## Why the Original Claim Probably Looked True

Three plausible routes to a false positive:

1. **Confounding by season.** Windy matches cluster in autumn and winter. If the original analysis did not control for month or season, it would pick up winter's lower scoring rather than wind's effect. Our calm/windy split spans all months, which is part of why the effect shrinks.
2. **Small-sample threshold scanning.** With ~90 calm matches, a 10% goals difference is well within noise. A single season's data can easily show −0.3 goals from wind alone.
3. **Selection on exposed grounds.** "Coastal grounds are worst affected" is a claim about a subset chosen for being windy. Testing it on the whole sample shows the opposite sign, which is the classic signature of a pattern fitted to noise.

---

## Data Gaps That Block a Proper Test

| Gap | Consequence |
|---|---|
| **No gust data.** Legacy files hold `wind_speed_10m_max` only. | Storm days are defined by gusts (55–80 kph), not sustained speed. The sample never measured the variable that matters. |
| **No wind bearing or pitch orientation.** | The only mechanism with a clean within-match test — half with the wind vs half against, opponent strength cancelling — cannot be run. |
| **No Scottish football.** Entire sample is English Premier League. | The library generalises an EPL result to grounds it has never seen. Today's tradeable fixtures were almost all Scottish or lower-English. |
| **Only 17 of 241 matches exceed 40 kph.** p90 = 38.8 kph. | Storm conditions are extrapolation, not interpolation. |
| **n=241 gives ~28% power** to detect a 10pp shift on a 50% base. | Absence of significance here is *not* evidence of absence. The effect could be real and this sample cannot see it. |

The power point cuts both ways and must be stated plainly: this note does **not** prove wind is irrelevant. It proves the library's confident, specific, stakable claim is not supported by the evidence the library itself cites.

---

## Capture Integrity Defects in the 2026-10-24 Wind-Day Log

*(Added during the post-match review of the day, 2026-10-24. Nothing below changes a conclusion in this note: the wind-day log is a single day's record and this note's claims rest on the separate n=241 replication. It is recorded here because the review re-scraped the same source the log was built from and the two disagreed.)*

The 90-fixture log in `data/processed/wind_event_log.csv` is not clean. Three defects, all in the capture code rather than the weather data:

| Defect | Rows | Detail |
|---|---|---|
| **Mis-dated fixtures** | 3 | `Johnstone Burgh v Formartine United`, `Threave Rovers v Pollok` and `Hill Of Beath Hawthorn v Musselburgh Athletic` carry 24 October kick-off-hour weather, but the BBC page for 31 October lists all three as Scottish Cup 2nd Round ties on that date. Their competition labels ("Scottish League One") are also wrong. The capture filter admits any fixture carrying a kick-off time and a `scheduled` status without checking it belongs to the requested date. |
| **Results silently dropped** | 8 | `bbc_scores.parse` matches only the inline `X 1 , Y 2 at Full time` rendering. Fixtures rendered with the score on its own line, or whose status is not "Full time" (after extra time, postponed, suspended), are not emitted at all. Barrow v Forest Green Rovers, Greenock Morton v Ayr United (postponed), Cove Rangers v East Kilbride, Bonnyton Thistle v Clachnacuddin, Brechin City v Strathspey Thistle, Brora Rangers v Cowdenbeath, Huntly v Annan Athletic and Troon v Caledonian Braves therefore carry no result. |
| **Opponent discarded** | 2 | `grounds.resolve()` returns `None` for clubs absent from the ground registry, and the raw BBC name is discarded rather than retained, so Dumbarton v Keith and Bury v Prescot Cables are stored with a null away team. |

Consequences for anything built on this log: only 79 of 90 fixtures could be validated; four of the eight dropped matches are shown on the BBC page as having gone to extra time, so the usable sample under-represents high-scoring games; and the three mis-dated rows must be excluded before this log is aggregated with any other date.

---

## The Build That Would Settle It

Three steps, in order:

1. **Backfill gusts and sustained wind per ground across the full master history.** `match_master_table.csv` holds 33,785 matches from 1993-08-14 to 2026-05-24 across 94 home teams; a venue backfill would take usable n from 241 to roughly 25,000. Open-Meteo's archive endpoint returns `wind_gusts_10m_max` for any coordinate back to 1940.
   - *Status:* partially complete (9 grounds cached) then blocked by Open-Meteo's hourly request limit. Resumable script at `scratch/backfill_archive.py`; needs ~10s throttling and a multi-hour window.
   - *Risk:* a 33-year daily request with four variables is weighted heavily against the free-tier quota. Chunk by decade, or split by variable.

2. **Add hourly wind bearing and pitch orientation.** Bearing is available from the same endpoint. Pitch orientation is the hard part — it must be sourced or measured per ground; a reasonable proxy is the long axis bearing from satellite imagery, but it needs validation. This unlocks the paired within-match test.

3. **Extend to Scotland and the lower English divisions.** Every fixture where weather advice would actually be used sits outside the current sample. `football-data.co.uk` publishes E0–E3, EC, SC0–SC1 season CSVs; Scottish lower leagues need a separate source.

---

## Corrections to the Original Note

`windfall-or-wind-break-weather-skews-totals.md` should be amended as follows:

- **Delete** the BUIF bullets claiming ~10% goals reduction and ~0.3 goals per match. Replace with: *"Wind shows no reliable goals effect in our data (n=241, −5.8%, p=0.46). Do not stake on wind totals."*
- **Delete** the "Coastal/exposed stadiums disproportionately affected" bullet. The sign reverses on test.
- **Downgrade** the betting-actions table from *Action* to *Untested hypothesis*. The corners row is not testable with current data.
- **Change** the confidence line from *"Medium for totals"* to *"None for totals until the gust backfill completes."*
- **Retain** the qualitative mechanism discussion — long-pass and crossing accuracy plausibly suffer — but label it as untested reasoning, not measured effect.

---

## Method Notes and Reproducibility

Scripts (scratch, not yet promoted to `src/`):
- `wind_map.py` — legacy file → stadium → master join
- `wind_hypothesis.py` — banded descriptives, correlations, ANOVA
- `wind_predictive.py` — likelihood-ratio tests, bootstrap, power
- `wind_claims.py` — claim-by-claim replication
- `wind_mechanism.py` — first-half test, threshold scan with Bonferroni
- `wind_asymmetry.py` — orientation-free variance test
- **`src/analysis/wind_analysis.py`** — the consolidated, reproducible module (see below)
- `wind_home_adv.py` — home advantage channel
- `wind_rain_combined.py` — wind × rain 2×2, extreme cell
- `backfill_archive.py` — resumable venue weather backfill

**The consolidated module is `src/analysis/wind_analysis.py`** and it reproduces every number in this note from source data. It did not exist when this investigation began: the original note's claims had no backing code anywhere in the repository. That is the root cause of this failure and the thing that has now been fixed. A research claim should not enter the library without a script that reproduces it — that rule now has a worked example behind it.

---

## Confidence

**High** that the headline wind-totals claim does not replicate on the available data.
**Medium** that wind has no material effect on goals — the sample is underpowered and lacks the gust and bearing variables that would define the effect.
**Low** on the fouls/cards/second-half lead. Physically plausible, statistically fragile, post-hoc selected.
**None** on any wind-based betting action until the backfill is complete.
