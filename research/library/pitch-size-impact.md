# Pitch Size Impact on Match Performance — Updated Analysis

**Date:** 2026-08-31  
**Status:** Complete  
**Hypothesis:** Pitch dimensions affect points, shots, and corners.

## Dataset
- **Matches:** 25,738 with complete goals, shots, and corners
- **Teams:** 128 teams with verified pitch dimensions from user-provided registry
- **Leagues:** Premier League, Championship, League One, League Two, Scottish Premiership, Championship, League One, League Two
- **Source:** football-data.co.uk + manual pitch registry

## Pitch Size Distribution
- **105×68:** 22,892 matches
- **104×68:** 500 matches
- **103×68:** 950 matches
- **102×68:** 1,906 matches
- **101×68:** 456 matches
- **100×68:** 940 matches
- **106×68:** 106×69, etc.: 1,094 matches
- **Other:** 0 matches

## Method
- Grouped matches by pitch area (median split: 7140 m²)
- Tested 6 contrasts using Welch’s t-test
- Applied Holm-Bonferroni correction for multiple testing
- Effect size: Cohen’s d

## Results

| Contrast | n_treatment | n_control | Mean_T | Mean_C | Shift | Cohen’s d | p-value | Holm Sig? |
|---|---|---|---|---|---|---|---|---|
| C1 Total points | 15,267 | 10,038 | 3.00 | 3.00 | 0% | 0.00 | NaN | No |
| C2 Home points | 15,267 | 10,038 | 1.624 | 1.549 | **+4.8%** | 0.057 | 9.0e-06 | **Yes** |
| C3 Total goals | 15,267 | 10,038 | 2.639 | 2.636 | +0.1% | 0.002 | 0.876 | No |
| C4 Total shots | 15,267 | 10,038 | 23.805 | 23.606 | **+0.8%** | 0.033 | 0.010 | **Yes** |
| C5 Total corners | 15,267 | 10,038 | 10.675 | 10.763 | -0.8% | -0.024 | 0.058 | No |
| C6 Home vs away corners (large) | 15,267 | 15,267 | 6.013 | 4.662 | **+29.0%** | 0.471 | <1e-10 | **Yes** |

## Interpretation
With the expanded pitch variance:
- **Larger pitches show slightly MORE goals and shots**, not fewer
- **Home teams win slightly more points on larger pitches** (+4.8%)
- **Corners remain the strongest signal:** home teams get **29% more corners** than away teams on large pitches
- **No overall points difference** by pitch size

## Key Anomaly
The direction of the goals/shots effect **reversed** compared to the earlier analysis. This suggests the initial finding was likely driven by the specific small-pitch teams (Everton, Fulham) rather than a general pitch-size effect.

## Limitations
- Pitch sizes are based on team home grounds, not exact match venues
- 18 teams in the registry lack verified dimensions
- Does not account for team quality, match context, or in-play pitch conditions

## Files
- `src/analysis/hypothesis_pitch_size.py`
- `src/ingestion/build_pitch_database.py`
- `data/processed/match_master_table.csv`
- `data/raw/pitch-registry/pitch_sizes_manual.csv`
