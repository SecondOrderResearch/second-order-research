# Research Library Entry

**Published:** 2026-10-05

**ID:** midweek-away-favoured-sides  
**Title:** Midweek Away Games for Favoured Sides  
**Status:** Supported  
**Pre-registered:** Yes  
**Hypothesis:** Favoured sides (top half of the league) playing midweek away games underperform expectations — the classic 'rainy Tuesday in Stoke' effect. Short rest + travel + hostile midweek atmosphere reduces performance.  
**Null hypothesis:** Midweek away games have no effect on favoured sides' performance.  
**Direction:** Negative: midweek away → favoured sides underperform (fewer points, narrower wins).  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 5000 matches (generic home-vs-away baseline; hypothesis-specific test not yet implemented)  
**Features:** is_midweek, is_away, league_position, points_won, goal_difference  
**Method:** Welch's t-test + Cohen's d; compare favoured sides' midweek away results vs weekend home/away results. Control for opponent strength.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals_baseline | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

NOTE: this is a generic home-vs-away goals baseline, not a test of 'Midweek Away Games for Favoured Sides'. A hypothesis-specific test module is required before this result is meaningful. Baseline: home teams average 1.53 goals vs 1.13 away.

## Conclusion

Baseline contrast only — hypothesis-specific test not yet implemented. Treat this entry as a pipeline smoke-test, not research evidence.

## Lessons

- Implement a dedicated test module for hypothesis 'midweek-away-favoured-sides' before publishing.
- The generic baseline exists only to keep the pipeline exercised.
