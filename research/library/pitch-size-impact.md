# Pitch Size Impact on Match Performance

**Date:** 2026-08-31  
**Status:** Complete  
**Hypothesis:** Pitch dimensions affect points, shots, and corners.

## Dataset
- **Matches:** 25,738 with complete goals, shots, and corners
- **Teams:** 91 English/Scottish teams
- **Leagues:** Premier League + Championship
- **Source:** football-data.co.uk

## Method
- Grouped matches by pitch area (median split)
- Tested 6 contrasts using Welch’s t-test
- Applied Holm-Bonferroni correction for multiple testing
- Effect size: Cohen’s d

## Results

| Contrast | n_treatment | n_control | Mean_T | Mean_C | Shift | Cohen’s d | p-value | Holm Sig? |
|---|---|---|---|---|---|---|---|---|
| C1 Total points | 22,892 | 2,846 | 3.00 | 3.00 | 0% | 0.00 | NaN | No |
| C2 Home points | 22,892 | 2,846 | 1.57 | 1.73 | -9.4% | -0.123 | 4.3e-10 | Yes |
| C3 Total goals | 22,892 | 2,846 | 2.63 | 2.72 | -3.3% | -0.055 | 5.9e-03 | Yes |
| C4 Total shots | 22,892 | 2,846 | 23.62 | 24.35 | -3.0% | -0.122 | 4.2e-09 | Yes |
| C5 Total corners | 22,892 | 2,846 | 10.69 | 10.81 | -1.1% | -0.033 | 0.104 | No |
| C6 Home vs away corners (large) | 22,892 | 22,892 | 5.89 | 4.80 | +22.8% | 0.382 | <1e-10 | Yes |

## Interpretation
Larger pitches are associated with:
- Slightly fewer goals and shots per match
- No overall difference in total points
- A strong home advantage in corner generation on large pitches

## Limitations
- Pitch sizes are based on team home grounds, not exact match venues
- Most pitches are 105x68, limiting variance
- Does not account for team quality or match context


## Large pitches

In our dataset, pitches with dimensions **105×68 or larger** are classified as **large**. The following pitches are included:

- Emirates Stadium
- Villa Park
- Vitality Stadium
- Gtech Community Stadium
- Amex Stadium
- Portman Road
- King Power Stadium
- Etihad Stadium
- Old Trafford
- St James' Park
- City Ground
- Carrow Road
- Molineux Stadium
- St Mary's Stadium
- Tottenham Hotspur Stadium
- Vicarage Road
- The Hawthorns
- London Stadium
- Bramall Lane
- The Den
- Kassam Stadium
- Kenilworth Road
- MKM Stadium
- Pride Park
- Riverside Stadium
- St Andrews
- Elland Road
- Ewood Park
- The Valley
- Toughsheet Community Stadium
- White Hart Lane
- bet365 Stadium
- Hillsborough
- Madejski Stadium
- Bloomfield Road
- Deepdale
- Fratton Park
- Home Park
- Oakwell
