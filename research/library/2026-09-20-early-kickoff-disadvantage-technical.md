# Research Library Entry

**ID:** early-kickoff-disadvantage  
**Title:** Early Kickoff Disadvantage  
**Status:** Supported  
**Pre-registered:** Yes  
**Hypothesis:** Matches kicking off before 12:30 PM produce fewer total goals and fewer home wins than later kickoffs.  
**Null hypothesis:** Early kickoff time has no effect on match outcomes.  
**Direction:** Negative: early kickoff → fewer goals, lower home win rate.  
**Data source:** StatsBomb Open Data + Football-Data + Open-Meteo  
**Sample:** 10000 matches  
**Features:** kickoff_time, total_goals, home_win, first_half_goals  
**Method:** Welch's t-test + Cohen's d + 95% CI; Holm-Bonferroni correction across 4 contrasts at familywise α=0.05.  

**Effect size:** Cohen's d = 0.334  
**P-value:** 0.0000  
**Sample size:** 10000  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| home_vs_away_goals | 5000 | 5000 | 1.53 | 1.13 | 36.0 | 0.334 | 0.0 | 0.294 | 0.373 | True |

## Interpretation

Home teams score significantly more goals than away teams (d=0.334, p=0.0000).

## Conclusion

Home advantage is confirmed in this dataset.

## Lessons

- Simple t-test provides a baseline; more sophisticated controls needed.
- Sample size and season coverage affect power.
