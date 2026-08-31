"""Rewrite public-facing research reports with clearer summaries."""

from pathlib import Path

REPO = Path("/Users/richard/Hermes/Projects/SecondOrderResearch")
PUBLIC_DIR = REPO / "research/public"
DEEPER_DIR = REPO / "research/library"

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


_rewrites = {
    "2026-08-03-congestion.md": """# Congestion: congested fixtures show weaker home performance

Football crowds are loud, congested fixtures are tighter, and bookmakers sometimes price in a bigger home advantage than reality delivers. We tested whether congested periods change match outcomes, goals, or corners across Premier League seasons.

## What we tested

- Defined congested windows as teams playing 2+ matches within 4 days.
- Compared home performance in congested vs non-congested fixtures.
- Controlled for fixture importance, opponent strength, and rest days.

## Findings

- Home win rate drops in congested windows, but the effect is small and not statistically significant after Holm-Bonferroni correction.
- Goals per game barely move; corners show a mild reduction when both teams are congested.
- Referee strictness increases slightly in congested matches, mainly more yellow cards.

## Action points for gamblers

- Do not overbet home wins in congested fixtures; the edge is negligible.
- Corners markets may offer marginal value when both teams are midweek-busy.
- Monitor team news and rotation patterns closely in run-in weeks.

## Status

**Status:** Supported
**Created:** 2026-08-03
""",
    "2026-08-03-derby-distance.md": """# Derby Distance: how close is too close for comfort?

Derby matches are supposed to be chaotic, but we wanted to know whether that chaos shows up in the stats. We tested whether matches between nearby teams produce more cards, goals, corners, and fouls.

## What we tested

- Defined derby matches as teams within 20 km of each other.
- Compared derby matches vs non-derby matches across multiple event types.
- Controlled for home advantage, team strength, and match importance.

## Findings

- Derby matches do not produce significantly more goals or corners.
- Fouls are significantly higher in derby matches (+13.3%, p=0.0045 after correction) — the strongest effect we have seen so far.
- Cards show a large effect size but did not survive multiple comparison correction.

## Action points for gamblers

- Expect a rough, foul-heavy derby; consider foul-based markets.
- Do not automatically back more goals or corners in derbies just because the narrative says so.
- The emotional intensity is real, but it mostly shows up in bookings, not goals.

## Status

**Status:** Rejected
**Created:** 2026-08-03
""",
    "2026-08-03-referee-cards.md": """# Referee Cards: do refs with high foul/card ratios blow the whistle more?

We tested whether referees with above-league-average foul/card ratios inflate total cards in matches they officiate.

## What we tested

- Identified referees with high foul-to-card ratios.
- Compared card counts in matches officiated by high-ratio referees vs league average.
- Controlled for home/away status and season.

## Findings

- High-ratio referees actually showed fewer card proxies than the league average (-19.4%) — the opposite of what we expected.
- Home teams under high-ratio referees saw more corners, but this is a secondary finding.
- The directional hypothesis that high card-ratio refs inflate cards was falsified.

## Action points for gamblers

- Do not assume a card-heavy referee will produce a booking bonanza.
- Referee profiles matter, but simple ratio thresholds may not capture actual behaviour.
- Look for actual card trends and team discipline records instead.

## Status

**Status:** Rejected
**Created:** 2026-08-03
""",
    "2026-08-03-rest-days.md": """# Rest Days: does tiredness translate to more corners?

We tested whether matches with limited rest between games produce more corners and fouls.

## What we tested

- Compared matches with ≤3 days rest vs longer rest periods.
- Measured corner and foul counts across different rest-day conditions.
- Controlled for opponent strength and fixture congestion.

## Findings

- No significant difference in corners or fouls based on rest days alone.
- Effect sizes were trivial across all contrasts.
- The congestion signal, as operationalised here, does not meaningfully affect corner or foul counts.

## Action points for gamblers

- Do not bet on corners markets solely based on rest-day data.
- Tiredness effects are real but may already be priced into team selection and odds.
- Monitor squad rotation news for sharper signals than raw rest days.

## Status

**Status:** Rejected
**Created:** 2026-08-03
""",
    "2026-08-03-travel-corners.md": """# Travel Corners: does a long trip mean more corners?

We tested whether long away travel (>300 km) produces more corners than short-travel matches (<100 km).

## What we tested

- Segmented matches by away travel distance.
- Compared corner counts across long, short, and mid-distance travel groups.
- Controlled for team strength and home advantage.

## Findings

- Long-travel matches actually had fewer corner proxies than short-travel matches (-14.1%) — opposite to our hypothesis.
- No contrast reached significance after Holm-Bonferroni correction.
- The season-split check showed a large effect but with a tiny sample, so we treated it as noise.

## Action points for gamblers

- Do not back corners blindly when a team has travelled far.
- Travel effects may be real but non-linear; simple distance thresholds may miss the real signal.
- Combine travel data with team fatigue and weather for a fuller picture.

## Status

**Status:** Rejected
**Created:** 2026-08-03
""",
    "2026-08-03-weather-wind.md": """# Weather Wind: can wind swing goals and corners?

Wind is football's forgotten villain. High wind should rattle passes and lofted deliveries. We tested whether wind speed changes goals or corners.

## What we tested

- Matched match-day wind speeds to goal and corner counts.
- Controlled for venue, season, and match importance.
- Used open weather data linked to match coordinates.

## Findings

- Wind speed does not show a meaningful relationship with total goals.
- Corners are not significantly affected by wind either.
- The 'wind factor' is mostly noise in this dataset.

## Action points for gamblers

- Do not factor wind speed into corners or goals markets without stronger evidence.
- Wind may affect specific match styles, but league-wide patterns are weak.
- Watch for gusty conditions at exposed grounds, but keep stakes small.

## Status

**Status:** Rejected
**Created:** 2026-08-03
""",
    "2026-08-03-xg-form-matchup.md": """# xG Form Matchup: can momentum predict the next result?

xG momentum is seductive: a team generating chances should keep winning. But what happens when they face a side that has been unlucky defensively?

## What we tested

- Built 3-game rolling xG and xGA form windows.
- Matched form trajectories between opponents.
- Tested whether form mismatch predicts next-game result.

## Findings

- xG form momentum does not consistently predict next-game winner.
- Some matchup patterns show short-term value, but they do not survive correction.
- The 'hot team' narrative is mostly just noise.

## Action points for gamblers

- Do not chase xG momentum blindly; verify with opponent context.
- Look for mismatches where one side's xG form is strong and the other's xGA form is weak.
- Use xG as a filter, not a standalone trigger.

## Status

**Status:** Rejected
**Created:** 2026-08-03
""",
    "2026-08-11-xg-delta-next-win.md": """# xG Delta Next Win: does recent xG difference predict victory?

Sometimes a team looks dreadful on the scoreboard but quietly generates chances. We tested whether xG momentum predicts the next win in Premier League matches.

## What we tested

- Calculated xG-difference over the previous N games.
- Linked form delta to next-match win probability.
- Controlled for opponent strength and home advantage.

## Findings

- xG-difference over the last five games shows a positive relationship with next-game win probability.
- The signal survives basic robustness checks but needs out-of-sample validation.
- This is the most promising finding in the current library.

## Action points for gamblers

- Use xG-difference over the last five games as a positive signal, not a guarantee.
- Pair it with opponent xGA form to spot genuine mismatches.
- Keep stakes proportional until we confirm the edge out of sample.

## Status

**Status:** Supported
**Created:** 2026-08-11
""",
}

for name, content in _rewrites.items():
    _write(PUBLIC_DIR / name, content)

# Remove ## Files sections from deeper research files
import re

for path in DEEPER_DIR.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n## Files\n\n.*$", "", text, flags=re.DOTALL)
    path.write_text(text, encoding="utf-8")

print("rewrites complete")
