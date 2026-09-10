# League Position and Form Overlay

## Concept

Overlaying pre-match league position and recent form (last 5 games) on existing research findings to improve predictive power and identify segment-specific edges.

## Why It Matters

Existing research findings (e.g., "home teams generate 29% more corners on large pitches") are reported as average effects across all teams. But the effect may be stronger or weaker depending on:

- **League position**: Top-half teams may behave differently than bottom-half teams
- **Recent form**: Teams in strong form may amplify or dampen effects
- **Interaction**: Top-half teams in strong form may show the strongest effects

## How to Apply

For each existing significant finding, add league position and form as interaction terms:

1. **Segment the data** by league position (top half vs bottom half) and form (last 5 games: >1.5 PPG = strong, <1.0 PPG = weak)
2. **Re-test the hypothesis** within each segment
3. **Compare effect sizes** across segments using interaction terms
4. **Report** which segments show the strongest/weakest effects

## Expected Outcomes

- Effects that are **stronger for top-half teams** suggest the edge is quality-dependent
- Effects that are **stronger for bottom-half teams** suggest the edge is desperation/relegation-driven
- Effects that **vary by form** suggest momentum modulates the edge
- Effects that **don't vary** are robust across all segments

## Implementation Notes

- League position should be measured at the time of the match (not final position)
- Form should be measured as points per game over the last 5 matches
- Minimum sample size per segment: 100 matches
- Use Welch's t-test within segments; ANOVA for interaction terms

## Example Overlay: Pitch Size Corners Finding

Original finding: Home teams generate 29% more corners on large pitches.

Overlay questions:
- Is this stronger for top-half home teams (who dominate possession)?
- Is it stronger when the home team is in strong form?
- Does it hold for bottom-half home teams?

If the effect is 40% for top-half teams but only 15% for bottom-half teams, the betting edge is concentrated in matches involving stronger home sides.
