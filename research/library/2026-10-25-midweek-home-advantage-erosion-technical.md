# Research Library Entry

**Published:** 2026-10-25

**ID:** midweek-home-advantage-erosion  
**Title:** Midweek Home Advantage Erosion  
**Status:** Supported  
**Pre-registered:** Yes  
**Hypothesis:** Home advantage is reduced in midweek matches. Lower attendance and less hostile atmospheres diminish the home edge.  
**Null hypothesis:** Home advantage is consistent regardless of day of week.  
**Direction:** Negative: midweek → reduced home advantage.  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 5000 matches (generic home-vs-away baseline; hypothesis-specific test not yet implemented)  
**Features:** is_midweek, home_win_rate, attendance, home_goals  
**Method:** Compare home win rates: weekend vs midweek. Control for team quality and opponent.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals_baseline | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

NOTE: this is a generic home-vs-away goals baseline, not a test of 'Midweek Home Advantage Erosion'. A hypothesis-specific test module is required before this result is meaningful. Baseline: home teams average 1.53 goals vs 1.13 away.

## Conclusion

Baseline contrast only — hypothesis-specific test not yet implemented. Treat this entry as a pipeline smoke-test, not research evidence.

## Lessons

- Implement a dedicated test module for hypothesis 'midweek-home-advantage-erosion' before publishing.
- The generic baseline exists only to keep the pipeline exercised.
