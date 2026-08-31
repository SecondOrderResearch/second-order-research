# Research Library Entry

**ID:** 2026-08-03-xg-form-matchup  
**Title:** 3-game rolling xG/xGA form vs opponent outperformance matchup  
**Status:** Rejected  
**Pre-registered:** Yes  
**Created:** 2026-08-03  
**Hypothesis:** A team’s 3-match rolling xG differential predicts match-point outcome, but this relationship weakens when the opponent has been outperforming its xGA.  
**Direction:** Interaction expected: high xG differential advantage should be muted or reversed against opponents who have conceded fewer goals than xGA suggested.  
**Data source:** StatsBomb Open Data linked sample (2015/16 Premier League via football-data.org match linkage).  
**Sample:** 374 linked matches, 748 team-match rows, 320 matched pairs after rolling-window requirements.  
**Features:** `match_xg` (home_xg, away_xg, home_xga, away_xga); `form_features` (rolling 3-game xG for/against and points).  
**Method:** OLS on home_points with Holm-Bonferroni correction across 5 contrasts at familywise α=0.05.  
**Evidentiary thresholds:** p<0.01 corrected, Cohen’s d≥0.35 or ≥5% event count shift, 95% CI lower bound > breakeven margin, out-of-sample same-direction p<0.05.  

## Results

| Contrast | n | beta | p_value | significant_holm |
|---|---|---|---|---|
| C1_home_xg_diff_vs_away | 320 | 0.0369 | 0.2531 | False |
| C2_opponent_xga_outperformance | 320 | -0.0383 | 0.2692 | False |
| C3_interaction_home_xg_diff_x_away_outperformance | 320 | 0.0116 | 0.4799 | False |
| C4_home_xg_diff_home_only | 320 | 0.0369 | 0.2531 | False |
| C5_home_xg_diff_second_half | 160 | -0.0007 | 0.9877 | False |

## Interpretation

No contrast approached statistical significance after multiple-testing correction. The primary main effect (C1) showed a small positive beta (+0.037 points per unit xG differential) but with wide uncertainty and no detectable interaction effect. The opponent xGA outperformance term (C2) was also non-significant and in the opposite direction to the pre-registered expectation. Split-sample checks (home-only, second-half season) were null.

## Conclusion

The hypothesis is rejected for this dataset and operationalisation. Possible reasons include limited sample size (one season, one competition), coarse 3-game window, simplistic rolling sum without opponent strength adjustment, and the use of `statsbomb_xg` rather than a consensus xG model. The null result is informative: it suggests recent shot-quality differentials alone are not a strong standalone predictor of match outcome in this period, and opponent xGA outperformance does not materially alter that relationship.

## Lessons

- xG differentials may need longer windows or opponent-weighted forms.
- Interaction effects require larger samples or more powerful designs.
- StatsBomb shot-level xG is usable but may benefit from calibration or comparison against alternative providers.
- The falsification-first protocol correctly classified this as a successful null result rather than a failed test.
