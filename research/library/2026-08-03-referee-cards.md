# Research Library Entry

**ID:** 2026-08-03-referee-cards  
**Title:** Referee foul/card ratio and total cards  
**Status:** Rejected  
**Pre-registered:** Yes  
**Created:** 2026-08-03  
**Hypothesis:** Referees with above-league-average foul/card ratios inflate total cards in matches they officiate.  
**Direction:** Positive: higher referee card ratio → more cards.  
**Data source:** StatsBomb Open Data linked sample (2015/16 Premier League via football-data.org match linkage).  
**Sample:** 374 linked matches; 461 high-ratio team-match rows, 1384 control.  
**Features:** `referee_features.referee_avg_cards_per_game`, `referee_avg_fouls_per_game`; `match_events` card proxy (`Bad Behaviour`).  
**Method:** Welch’s t-test + Cohen’s d + 95% CI; Holm-Bonferroni correction across 3 contrasts at familywise α=0.05.  
**Evidentiary thresholds:** p<0.01 corrected, Cohen’s d≥0.35 or ≥5% event count shift, 95% CI lower bound > breakeven margin, out-of-sample same-direction p<0.05.  

## Results

| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| C1_high_ref_ratio_vs_league | 461 | 1384 | 0.4100 | 0.5087 | -19.40 | -0.123 | 0.0125 | -0.1761 | -0.0213 | True |
| C2_home_vs_away_under_high_ref | 461 | 461 | 78.7939 | 68.8568 | 14.43 | 0.238 | 0.0003 | 4.5454 | 15.3288 | True |
| C4_season_split_2015/2016_vs_2003/2004 | 445 | 16 | 0.3888 | 1.0000 | -61.12 | -0.887 | 0.0325 | -1.1225 | -0.1000 | True |

## Interpretation

All contrasts reached Holm-Bonferroni significance. However, the primary contrast (C1) showed a **negative** effect: high-ratio referees had **fewer** card proxies than the league average (-19.4%, d=-0.123), opposite to the pre-registered direction. The home/away split (C2) showed more corners for home teams under high-ratio referees, but this is a secondary finding. The season split (C4) had a large effect but very small control cell (n=16).

## Conclusion

The hypothesis is **rejected** for this dataset and operationalisation. The directional prediction that high foul/card ratio referees inflate cards is falsified; if anything, the opposite pattern appears. Possible reasons include:
- `Bad Behaviour` as a card proxy may undercount yellows or be inconsistently recorded across referees
- Referee card ratios may reflect stricter overall control rather than card-heavy tendencies
- Sample bias from 2003/04 season data quality issues

## Lessons

- Card proxy via `Bad Behaviour` is noisy and should be validated against true card counts.
- Referee-level ratios require careful calibration; simple ratio thresholds may not capture behavioral style.
- Falsification of the directional hypothesis is a successful null result under this methodology.
