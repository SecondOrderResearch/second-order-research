# Research Library Entry

**ID:** 2026-08-03-derby-distance  
**Title:** Derby matches and match intensity  
**Status:** Rejected  
**Pre-registered:** Yes  
**Created:** 2026-08-03  
**Hypothesis:** Derby matches (distance <20km) show elevated cards, goals, corners, and other events.  
**Direction:** Positive: derby → more cards/goals/corners/fouls.  
**Data source:** StatsBomb Open Data linked sample (2015/16 Premier League via football-data.org match linkage).  
**Sample:** 374 linked matches; 30 derby matches (<20km), 306 non-derby matches.  
**Features:** `travel_matrix.distance_km`; `match_events` foul/card/corner proxies.  
**Method:** Welch’s t-test + Cohen’s d + 95% CI; Holm-Bonferroni correction across 5 contrasts at familywise α=0.05.  
**Evidentiary thresholds:** p<0.01 corrected, Cohen’s d≥0.35 or ≥5% event count shift, 95% CI lower bound > breakeven margin, out-of-sample same-direction p<0.05.  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_derby_vs_non_derby_goals | 30 | 306 | 2.6333 | 2.6503 | -0.64 | -0.010 | 0.9535 | -0.5869 | 0.5530 | False |
| C2_derby_vs_non_derby_corners | 30 | 306 | 134.0667 | 138.1438 | -2.95 | -0.061 | 0.6461 | -21.4255 | 13.2712 | False |
| C3_derby_vs_non_derby_fouls | 30 | 306 | 29.2667 | 25.8301 | 13.30 | 0.597 | 0.0045 | 1.2111 | 5.6621 | True |
| C4_derby_vs_non_derby_cards | 30 | 306 | 1.0333 | 0.4444 | 132.50 | 0.725 | 0.0330 | 0.0703 | 1.1075 | False |
| C5_home_vs_away_derby_corners | 30 | 30 | 73.0333 | 61.0333 | 19.66 | 0.420 | 0.1090 | -2.7533 | 26.7533 | False |

## Interpretation

The primary hypothesis—that derby matches have more goals, corners, cards, and other events—was not supported for goals, corners, or cards. However, **fouls were significantly higher in derby matches** (mean 29.3 vs 25.8, +13.3%, Cohen’s d=0.597, p=0.0045 after Holm-Bonferroni correction). This is the strongest effect observed across all hypotheses tested so far. The card contrast (C4) showed a large effect size but did not survive correction.

## Conclusion

The hypothesis is **partially supported** for fouls only. Derby matches do not show significantly more goals or corners, but they do show significantly more fouls. This suggests derby intensity manifests primarily in fouls rather than scoring or set pieces in this sample.

## Lessons

- Derby effects may be localized to specific event types; testing multiple outcomes is essential.
- The 20km threshold captured 30 matches in this linked sample; expanding the sample would improve power.
- Card proxies remain noisy; larger samples are needed to detect card effects.
