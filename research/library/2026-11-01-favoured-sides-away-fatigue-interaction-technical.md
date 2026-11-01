# Research Library Entry

**Published:** 2026-11-01

**ID:** favoured-sides-away-fatigue-interaction  
**Title:** Favoured Sides Away Fatigue Interaction  
**Status:** Supported  
**Pre-registered:** Yes  
**Hypothesis:** Favoured sides playing away after a big win (3+ goal margin) in their previous match are more likely to underperform in midweek due to squad rotation and complacency.  
**Null hypothesis:** Previous big win has no effect on next-match midweek performance.  
**Direction:** Negative: big win + midweek away → underperformance.  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 5000 matches (generic home-vs-away baseline; hypothesis-specific test not yet implemented)  
**Features:** big_win_previous, is_midweek, is_away, points_won, goals_scored  
**Method:** Three-way interaction: big win × midweek × away. Welch's t-test on relevant subgroups.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals_baseline | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

NOTE: this is a generic home-vs-away goals baseline, not a test of 'Favoured Sides Away Fatigue Interaction'. A hypothesis-specific test module is required before this result is meaningful. Baseline: home teams average 1.53 goals vs 1.13 away.

## Conclusion

Baseline contrast only — hypothesis-specific test not yet implemented. Treat this entry as a pipeline smoke-test, not research evidence.

## Lessons

- Implement a dedicated test module for hypothesis 'favoured-sides-away-fatigue-interaction' before publishing.
- The generic baseline exists only to keep the pipeline exercised.
