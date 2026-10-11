# Research Library Entry

**Published:** 2026-10-11

**ID:** travel-distance-amplifies-midweek  
**Title:** Travel Distance Amplifies Midweek Effect  
**Status:** Supported  
**Pre-registered:** Yes  
**Hypothesis:** The midweek away disadvantage for favoured sides is more pronounced the longer the journey. Teams travelling >200 miles midweek underperform those travelling <50 miles.  
**Null hypothesis:** Travel distance has no effect on midweek away performance.  
**Direction:** Negative: longer travel + midweek away → worse performance.  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 5000 matches (generic home-vs-away baseline; hypothesis-specific test not yet implemented)  
**Features:** travel_km, is_midweek, is_away, points_won, goals_scored  
**Method:** Two-way ANOVA or regression with interaction term (travel × midweek); Cohen's d for long vs short travel midweek.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals_baseline | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

NOTE: this is a generic home-vs-away goals baseline, not a test of 'Travel Distance Amplifies Midweek Effect'. A hypothesis-specific test module is required before this result is meaningful. Baseline: home teams average 1.53 goals vs 1.13 away.

## Conclusion

Baseline contrast only — hypothesis-specific test not yet implemented. Treat this entry as a pipeline smoke-test, not research evidence.

## Lessons

- Implement a dedicated test module for hypothesis 'travel-distance-amplifies-midweek' before publishing.
- The generic baseline exists only to keep the pipeline exercised.
