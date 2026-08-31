# Research Library Entry

**ID:** 2026-08-03-weather-wind  
**Title:** Wind speed versus goals and corners  
**Status:** Rejected  
**Pre-registered:** Yes  
**Created:** 2026-08-03  
**Hypothesis:** Higher wind speeds are associated with fewer total goals but more total corners.  
**Direction:** Negative for goals, positive for corners.  
**Data source:** Open-Meteo archive API matched to StatsBomb-linked matches (2003/04 and 2015/16 seasons).  
**Sample:** 374 linked matches; 278 with weather data after matching; 170 high-wind, 13 low-wind.  
**Features:** `weather.wind_speed_10m_max`, `weather.precipitation_sum`; goals and corner proxies from match data.  
**Method:** Welch’s t-test + Cohen’s d + 95% CI; Holm-Bonferroni correction across 5 contrasts at familywise α=0.05.  
**Evidentiary thresholds:** p<0.01 corrected, Cohen’s d≥0.35 or ≥5% event count shift, 95% CI lower bound > breakeven margin, out-of-sample same-direction p<0.05.  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_high_wind_vs_low_goals | 170 | 13 | 2.5588 | 2.6923 | -4.96 | -0.081 | 0.8119 | -1.2186 | 0.9516 | False |
| C2_high_wind_vs_low_corners | 170 | 13 | 146.8882 | 133.7692 | 9.81 | 0.182 | 0.5835 | -32.9615 | 59.1995 | False |
| C3_home_vs_away_high_wind_corners | 170 | 170 | 75.5059 | 71.3824 | 5.78 | 0.094 | 0.3848 | -5.1972 | 13.4443 | False |
| C4_wet_vs_dry_goals | 135 | 98 | 2.4741 | 2.8061 | -11.83 | -0.204 | 0.1305 | -0.7629 | 0.0988 | False |
| C5_season_split_2015/2016_vs_2003/2004 | 164 | 6 | 2.5671 | 2.3333 | 10.02 | 0.144 | 0.6982 | -0.8958 | 1.3633 | False |

## Interpretation

No contrast reached statistical significance after Holm-Bonferroni correction. The primary contrast (C1) showed a small negative effect: high-wind matches had slightly fewer total goals than low-wind matches (-5.0%, d=-0.081), but this was far from significant. The corners contrast (C2) was in the predicted direction (+9.8%), but also non-significant with a very small control cell (n=13). The precipitation contrast (C4) showed a larger effect size (-11.8%, d=-0.204) but remained non-significant.

## Conclusion

The hypothesis is rejected for this dataset and operationalisation. Possible reasons include:
- Weather effects on goals/corners may be weak or mediated by pitch quality
- The wind threshold (20 kph high vs 10 kph low) may be too conservative
- Open-Meteo daily max wind may not capture match-day wind conditions accurately
- Sample imbalance: very few low-wind matches in the linked sample

## Lessons

- Weather as a second-order variable requires precise temporal matching to kickoff time, not just daily aggregates.
- Threshold selection for weather bands materially affects power; adaptive thresholds based on distribution should be explored.
- Cross-season validation is hampered by small sample sizes in weather-matched data.
