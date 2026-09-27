# International Break Hangover

**Published:** 2026-09-27

*NOTE: This report is a pipeline smoke-test, NOT real research evidence. No dedicated hypothesis module exists for "International Break Hangover" (only a generic home-vs-away goals baseline was run). Treat this as a placeholder, not a betting edge.*

## Bottom Line Up Front

- **Status:** NOT TESTED — no dedicated test branch implemented.
- **Result:** No betting edge identified — do not trade this angle.
- **Method note:** The pipeline ran a generic home-vs-away goals contrast (home 1.53 vs away 1.13, Cohen's d ≈ 0.334) which is NOT a test of international-break hangover. A real test requires linking `matches` to international-break dates and international-player counts, then comparing post-break results by international-duty load.

**Market Inefficiency:** None  
**Betting Actions:** No actions  

## The Read (honest version)

- The hypothesis queue (22 ideas) includes "International Break Hangover" as untested.
- The weekly pipeline (`scripts/weekly_research.py`) has dedicated branches for `early-kickoff-disadvantage` and `post-european-fatigue`; everything else falls back to this clearly-labelled baseline.
- Before this becomes evidence, implement a dedicated `test_hypothesis()` branch that reads `matches` + `international_break_dates` and runs Welch's t-test on high vs low international-player count post-break.
- The current generic baseline (n ≈ 10,000) is a smoke-test only; do not interpret p = 0.000 as support for the hangover hypothesis.

## Key Numbers

- **Generic home-vs-away baseline (NOT the hypothesis test):** Cohen's d ≈ 0.334, p ≈ 0.000, shift ≈ 36.0% — but this compares all home vs all away, not post-break vs normal.
- **Dedicated test:** Not implemented. Expected design: correlation + median split on `international_players_count`; Welch's t-test comparing high (> median) vs low (≤ median) international-duty load in first match after break.

## Action Points for Gamblers

- Do NOT trade on this report — it contains no validated signal.
- Watch for a future entry with a real `test_hypothesis()` branch, verified warehouse counts, and a non-baseline contrast table before considering any international-break betting angle.

## Confidence

**None — smoke-test only.**
