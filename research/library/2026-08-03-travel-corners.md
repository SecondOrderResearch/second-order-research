# Research Library Entry

**ID:** 2026-08-03-travel-corners  
**Title:** Long away travel distance and total corners  
**Status:** Rejected  
**Pre-registered:** Yes  
**Created:** 2026-08-03  
**Hypothesis:** Matches with long away travel (>300 km) produce more total corners than short-travel matches (<100 km).  
**Direction:** Positive: longer travel → more corners.  
**Data source:** StatsBomb Open Data linked sample (2015/16 Premier League via football-data.org match linkage).  
**Sample:** 374 linked matches; 336 team-match rows after travel join; 50 long, 64 short, 222 mid.  
**Features:** `travel_matrix.distance_km`; `match_events` corner proxy (`play_pattern == From Corner`).  
**Method:** Welch’s t-test + Cohen’s d + 95% CI; Holm-Bonferroni correction across 4 contrasts at familywise α=0.05.  
**Evidentiary thresholds:** p<0.01 corrected, Cohen’s d≥0.35 or ≥5% event count shift, 95% CI lower bound > breakeven margin, out-of-sample same-direction p<0.05.  


> **Pitch size note:** In our dataset, pitches with dimensions **105×68 or larger** are classified as **large**. Home teams generate **22.8% more corners** on large pitches than away teams.

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_long_vs_short | 50 | 64 | 122.34 | 142.36 | -14.06 | -0.343 | 0.069995 | -41.69 | 1.65 | False |
| C2_home_vs_away_in_long | 50 | 50 | 58.54 | 63.80 | -8.24 | -0.159 | 0.427909 | -18.37 | 7.85 | False |
| C3_opponent_travel_adjusted_long_vs_short | 50 | 64 | 122.34 | 142.36 | -14.06 | -0.343 | 0.069995 | -41.69 | 1.65 | False |
| C5_season_split_2015/2016_vs_2003/2004 | 46 | 4 | 125.59 | 85.00 | 47.75 | 0.725 | 0.129663 | -2.70 | 83.87 | False |

## Interpretation

No contrast reached statistical significance after Holm-Bonferroni correction. The primary contrast (C1) showed a negative point estimate: long-travel matches had fewer corner proxies than short-travel matches (-14.1%, d=-0.343), opposite to the pre-registered direction. The season-split contrast (C5) showed a large effect but with very small control cell size (n=4) and non-significant p-value.

## Conclusion

The hypothesis is rejected for this dataset and operationalisation. Possible reasons include the indirect corner proxy, limited sample size, and confounding by team/season. The null result is informative: simple travel-distance thresholds do not appear to drive corner volume in this linked sample.

## Lessons

- Corner proxy via `play_pattern == From Corner` is noisy; true corner-kick event labels should be used if available.
- Travel effects may be non-linear or mediated by other factors; binary splits may miss subtler signals.
- Season-split checks require balanced samples; small cells should be flagged rather than over-interpreted.
