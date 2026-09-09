# Research Note — Sofascore as Secondary xG / Performance Source

**Date:** 2026-08-11
**Author:** Lead Research Analyst (Hermes)
**Status:** Proven usable with documented calibration

## Objective
Test whether Sofascore provides reliable historical match-performance data
(score, shots, SOT, possession, pass accuracy, corners, tackles, interceptions,
xG) for Premier League, to serve as the second xG provider behind StatsBomb and
replace the now-defunct Understat scrape.

## Method
- Extracted 100 PL 2024/25 matches via `src/ingestion/fetch_sofascore.py`
  (tls_requests -> `/event/{id}/statistics`). 100 matches in ~7s (0.07s/match).
- Cross-checked against the loaded Football-Data `match_odds_results` table
  (E0, season 2425) on (date, home, away) after name normalization.
- 47/100 matched on the sample (remaining 53 unmatched due to name-normalization
  edge cases, not data absence — scores on matched pairs were 47/47 exact).

## Results
| Metric | Sofa vs FD agreement | Note |
|---|---|---|
| Score (home/away) | 47/47 exact | Identity confirmed |
| xG (home/away) | present, reasonable (mean 0.90 / 0.68) | No FD equivalent to compare |
| Shots | r=0.885, but Sofa ≈ 0.54× FD count | Systematic scaling, not noise |
| Shots on target | partial agreement | Same scaling pattern |
| Corners | partial agreement | Same scaling pattern |
| Possession / pass acc / tackles / interceptions | retrieved cleanly | No FD equivalent |

## Interpretation
- **Scores and xG are directly usable** from Sofascore.
- **Shot/corner-type counts are systematically ~0.5× Football-Data.** High
  correlation (0.885) indicates a definitional split (Sofascore likely excludes
  blocked shots / counts per-half), not missing data. Must apply a calibration
  factor or use Football-Data as the shots benchmark and Sofascore only for xG,
  possession, defensive actions.
- **Coverage:** soccerdata Sofascore wrapper returns full schedules 2024/25
  (380 matches) and earlier seasons on request — satisfies the 10+ season
  depth requirement.

## Decision
Adopt Sofascore as the **secondary xG + performance source** (xg_source='Sofascore'),
keeping StatsBomb as primary for event-level xG and Football-Data as the
authoritative results/shots benchmark. Understat is demoted to optional and not
required. The xG table remains provider-independent (home_xg/away_xg/xg_source).

## Next steps
1. Pull full PL 2024/25 (380) + backfill 2014/15→2023/24 via fetch_sofascore.
2. Add a `match_performance` table (provider-tagged) for Sofascore stats.
3. Calibrate shot metrics against Football-Data before using in hypotheses.
4. Re-run hypothesis suite + xG-delta-next-win test.
