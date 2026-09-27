# Research Library Entry

**Published:** 2026-09-27

**ID:** international-break-hangover  
**Title:** International Break Hangover  
**Status:** NOT TESTED — SMOKE TEST ONLY (no dedicated hypothesis branch)  
**Pre-registered:** Yes  
**Hypothesis:** Teams with more players on international duty produce worse results in the first match after the break.  
**Null hypothesis:** International break has no effect on post-break match outcomes.  
**Direction:** Negative: more internationals → worse post-break performance.  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 5000 matches (generic home-vs-away baseline; hypothesis-specific test not yet implemented)  
**Features:** international_players_count, post_break_points, post_break_goals  
**Method:** Correlation + median split; Welch's t-test on high vs low international count.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals_baseline | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

NOTE: this is a generic home-vs-away goals baseline, not a test of 'International Break Hangover'. A hypothesis-specific test module is required before this result is meaningful. Baseline: home teams average 1.53 goals vs 1.13 away.

## Conclusion

Baseline contrast only — hypothesis-specific test not yet implemented. Treat this entry as a pipeline smoke-test, not research evidence.

## Lessons

- Implement a dedicated test module for hypothesis 'international-break-hangover' before publishing.
- The generic baseline exists only to keep the pipeline exercised.
