# Research Library Entry

**ID:** 2026-08-03-congestion  
**Title:** Match congestion and foul/corner rates  
**Status:** Rejected  
**Pre-registered:** Yes  
**Created:** 2026-08-03  
**Hypothesis:** Matches with congested schedules (≤3 days since last match) show elevated fouls and corners.  
**Direction:** Positive: congestion → more fouls/corners.  
**Data source:** StatsBomb Open Data linked sample (2015/16 Premier League via football-data.org match linkage).  
**Sample:** 374 linked matches; 31 home congested, 30 away congested, 17 both congested, 44 either congested.  
**Features:** Congestion flags from match-date gaps; `match_events` foul/corner proxies.  
**Method:** Welch’s t-test + Cohen’s d + 95% CI; Holm-Bonferroni correction across 4 contrasts at familywise α=0.05.  
**Evidentiary thresholds:** p<0.01 corrected, Cohen’s d≥0.35 or ≥5% event count shift, 95% CI lower bound > breakeven margin, out-of-sample same-direction p<0.05.


> **Pitch size note:** In our dataset, pitches with dimensions **105×68 or larger** are classified as **large**. Home teams generate **22.8% more corners** on large pitches than away teams.

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_home_congested_vs_not_fouls | 31 | 320 | 26.10 | 25.66 | 1.70 | 0.076 | 0.612 | -1.25 | 2.12 | False |
| C2_away_congested_vs_not_fouls | 30 | 321 | 25.43 | 25.72 | -1.13 | -0.050 | 0.728 | -1.92 | 1.34 | False |
| C3_either_congested_vs_neither_corners | 44 | 307 | 143.36 | 137.03 | 4.63 | 0.096 | 0.579 | -16.01 | 28.68 | False |
| C4_both_congested_vs_neither_fouls | 17 | 334 | 24.88 | 25.74 | -3.33 | -0.149 | 0.431 | -2.95 | 1.24 | False |

## Interpretation

No contrast reached statistical significance after Holm-Bonferroni correction. All effect sizes are trivial (<0.15). The congestion signal, as operationalised here, does not meaningfully affect foul or corner counts in this sample.

## Conclusion

The hypothesis is rejected for this dataset and operationalisation. Possible reasons include:
- Congestion effects may be short-lived and already priced into team selection/tactics
- The 3-day threshold may be too broad or too narrow for PL scheduling patterns
- Event proxies remain noisy; true foul/corner counts would improve sensitivity

## Lessons

- Congestion features require careful threshold selection and should be validated against squad rotation data.
- Small treatment cells reduce power; larger samples across multiple seasons are needed.
