# Research Library Entry

**Published:** 2026-09-21

**ID:** post-european-fatigue  
**Title:** Post-European Weekend Fatigue  
**Status:** Rejected  
**Pre-registered:** Yes  
**Hypothesis:** Teams playing in European competitions (UCL, UEL, UECL) produce worse results the following weekend compared to non-European teams.  
**Null hypothesis:** European participation has no effect on weekend match outcomes.  
**Direction:** Negative: European midweek → worse weekend performance (fewer points, more goals conceded).  
**Data source:** football-data.co.uk (football_data table)  
**Sample:** 2660 PL matches 2019/20–2025/26 (5320 team-match rows); European participants identified per season  
**Features:** european_midweek, weekend_points, weekend_goals_conceded, weekend_goal_difference  
**Method:** Welch's t-test + Cohen's d + 95% CI; compare European vs non-European teams on weekend outcomes.  

**Sample size:** 2660  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_euro_teams_in_vs_out_of_window_points | 1326 | 764 | 1.747 | 1.708 | 2.3 | 0.03 | 0.512 | -0.078 | 0.157 | False |
| C2_euro_teams_in_vs_out_of_window_gd | 1326 | 764 | 0.542 | 0.603 | -10.1 | -0.032 | 0.4768 | -0.23 | 0.107 | False |
| C3_placebo_non_euro_in_vs_out_of_window_points | 2068 | 1162 | 1.159 | 1.147 | 1.0 | 0.009 | 0.8061 | -0.08 | 0.103 | False |
| C4_euro_vs_non_euro_in_window_points | 1326 | 2068 | 1.747 | 1.159 | 50.8 | 0.449 | 0.0 | 0.498 | 0.68 | True |

## Interpretation

Across 2660 PL matches, European teams' points during European windows do not differ significantly from outside them after correction. Midweek European football alone does not measurably dent league performance in this sample.

## Conclusion

The post-European fatigue hypothesis is rejected for this dataset — squad rotation appears to absorb the congestion at this level.

## Lessons

- European qualification is proxied by a per-season registry, not fixture lists; deep UCL/UEL runs are not distinguished from early exits.
- The placebo contrast (non-European teams, same windows) is the key falsification device — without it, seasonal form drift masquerades as fatigue.
- Window boundaries (Sep 15 / Dec 15 / Feb 15) approximate the European calendar; a fixture-level join would sharpen the treatment definition.
