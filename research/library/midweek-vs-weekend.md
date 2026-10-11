# Midweek vs Weekend Performance Analysis

**Date:** 2026-10-08  
**Status:** Complete  
**Hypothesis:** Teams perform differently on midweek (Tue/Wed) vs weekend (Sat/Sun) matches.

## Dataset
- **Midweek matches:** 5,277
- **Weekend matches:** 19,561
- **Other (Mon/Thu/Fri):** 2,482
- **Total:** 27,320 matches with complete data
- **Leagues:** Premier League, Championship, Premiership
- **Date range:** 1993–2026

## Method
- Classified matches by day of week
- Compared midweek vs weekend performance using Welch's t-test
- Applied Holm-Bonferroni correction for multiple testing
- Effect size: Cohen's d

## Results

| Contrast | n_midweek | n_weekend | Mean_MW | Mean_WE | Shift | Cohen's d | p-value | Holm Sig? |
|---|---|---|---|---|---|---|---|---|
| C1 Total goals | 5,277 | 19,561 | 2.58 | 2.66 | -2.8% | -0.046 | 2.8e-03 | **Yes** |
| C2 Total shots | 5,277 | 19,561 | 23.40 | 23.59 | -0.8% | -0.032 | 3.8e-02 | No |
| C3 Total corners | 5,277 | 19,561 | 10.51 | 10.80 | -2.7% | -0.082 | 1.2e-07 | **Yes** |
| C4 Home points | 5,277 | 19,561 | 1.59 | 1.60 | -0.3% | -0.003 | 8.4e-01 | No |
| C5 Away points | 5,277 | 19,561 | 1.41 | 1.40 | +0.3% | 0.003 | 8.4e-01 | No |
| C6 Home goals | 5,277 | 19,561 | 1.45 | 1.50 | -3.2% | -0.038 | 1.3e-02 | No |
| C7 Away goals | 5,277 | 19,561 | 1.13 | 1.16 | -2.4% | -0.025 | 1.1e-01 | No |

## Interpretation
- **Total goals** are significantly lower on midweek matches (-2.8%, p < 0.01)
- **Total corners** are significantly lower on midweek matches (-2.7%, p < 0.001)
- **Home/away points** show no significant difference
- **Home goals** are lower on midweek but not significant after correction
- **Away goals** are lower on midweek but not significant after correction

## Team-Level Findings (20+ midweek home matches)

### Worst Midweek Performers
| Team | MW Home Pts | WE Home Pts | Diff | MW Goals | WE Goals |
|---|---|---|---|---|---|
| Blackpool | 1.05 | 1.48 | -0.43 | 1.21 | 1.37 |
| Aberdeen | 1.35 | 1.77 | -0.42 | 1.69 | 1.41 |
| Doncaster Rovers | 1.00 | 1.40 | -0.40 | 0.84 | 1.20 |
| Swansea City | 1.41 | 1.64 | -0.23 | 1.28 | 1.43 |
| Hull City | 1.28 | 1.50 | -0.22 | 1.21 | 1.39 |

### Best Midweek Performers
| Team | MW Home Pts | WE Home Pts | Diff | MW Goals | WE Goals |
|---|---|---|---|---|---|
| Middlesbrough | 2.02 | 1.49 | +0.53 | 1.45 | 1.32 |
| Luton Town | 1.80 | 1.28 | +0.51 | 1.86 | 1.21 |
| Motherwell | 1.80 | 1.42 | +0.38 | 1.70 | 1.44 |
| Manchester City | 2.38 | 2.10 | +0.29 | 2.18 | 2.25 |
| Celtic | 2.80 | 2.51 | +0.28 | 2.54 | 2.66 |

## Betting Implications
- **Total goals:** Consider under 2.5 goals on midweek matches
- **Total corners:** Consider under corner lines on midweek matches
- **Team-specific:** Some teams (Blackpool, Aberdeen, Doncaster) consistently underperform at home on midweek

## Files
- `src/analysis/midweek_analysis.py`
- `data/processed/midweek_results.csv`
- `data/processed/midweek_team_comparison.csv`
