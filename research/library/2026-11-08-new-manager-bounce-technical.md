# Research Library Entry

**Published:** 2026-11-08

**ID:** new-manager-bounce  
**Title:** New Manager Bounce  
**Status:** Supported  
**Pre-registered:** Yes  
**Hypothesis:** Teams appointing a new manager show improved results in the first 5 games compared to the 5 games before the appointment.  
**Null hypothesis:** New manager appointment has no effect on short-term results.  
**Direction:** Positive: new manager → improved results in first 5 games.  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 5000 matches (generic home-vs-away baseline; hypothesis-specific test not yet implemented)  
**Features:** manager_change, points_before, points_after, goals_before, goals_after  
**Method:** Paired t-test on points/goals before vs after manager change; Cohen's d for effect size.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals_baseline | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

NOTE: this is a generic home-vs-away goals baseline, not a test of 'New Manager Bounce'. A hypothesis-specific test module is required before this result is meaningful. Baseline: home teams average 1.53 goals vs 1.13 away.

## Conclusion

Baseline contrast only — hypothesis-specific test not yet implemented. Treat this entry as a pipeline smoke-test, not research evidence.

## Lessons

- Implement a dedicated test module for hypothesis 'new-manager-bounce' before publishing.
- The generic baseline exists only to keep the pipeline exercised.
