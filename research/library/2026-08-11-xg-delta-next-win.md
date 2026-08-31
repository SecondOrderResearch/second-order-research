# Research Library Entry

**ID:** 2026-08-11-xg-delta-next-win
**Title:** xG-difference over previous N games predicts next-game win (PL, Sofascore xG)
**Status:** Supported
**Pre-registered:** Yes
**Created:** 2026-08-11 16:27
**Hypothesis:** Teams with few points but a high xG-difference over the previous N games have a higher chance of winning the next game, especially where the opponent shows the inverse.
**Direction:** Positive: home xG-diff -> next win; interaction home xG-diff x away underperformance -> next win.
**Data source:** match_performance (Sofascore), PL 2014/15-2025/26, 5 seasons.
**Sample:** unified PL panel; n per contrast in table.
**Features:** rolling xG-for / xG-against / points over windows 3 and 5 (shifted 1), next-game win flag.
**Method:** OLS contrasts + Holm-Bonferroni correction (familywise alpha=0.05) per window.

## Results

| Contrast | n | beta | p_value | significant_holm |
|---|---|---|---|---|
| W3_C1_home_xg_diff_vs_next_win | 1519 | 0.0168 | 0.0601 | False |
| W3_C2_away_xg_diff_vs_next_win | 1519 | 0.0062 | 0.4816 | False |
| W3_C3_home_xg_diff_x_away_underperf | 1519 | 0.0032 | 0.2821 | False |
| W3_C4_home_underperf_vs_next_win | 1519 | 0.0135 | 0.0004 | True |
| W5_C1_home_xg_diff_vs_next_win | 1481 | 0.0232 | 0.0005 | True |
| W5_C2_away_xg_diff_vs_next_win | 1481 | 0.0035 | 0.6013 | False |
| W5_C3_home_xg_diff_x_away_underperf | 1481 | 0.0036 | 0.0169 | True |
| W5_C4_home_underperf_vs_next_win | 1481 | 0.0109 | 0.0001 | True |

## Interpretation

At least one contrast survived Holm-Bonferroni correction.

## Conclusion

Hypothesis supported for this operationalisation and sample.
