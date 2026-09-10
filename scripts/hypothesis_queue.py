"""Hypothesis queue for weekly research rotation.

Maintains a rotating queue of novel hypotheses across different categories.
Each week the pipeline picks the next untested hypothesis, tests it, and
records the result.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

from src.config import RESEARCH_DIR

QUEUE_PATH = RESEARCH_DIR / "hypothesis_queue.json"


@dataclass
class Hypothesis:
    id: str
    category: str
    title: str
    hypothesis: str
    negative: str
    direction: str
    markets_affected: list[str]
    variables_tested: list[str]
    data_requirements: list[str]
    method: str
    status: str = "untested"
    last_tested: Optional[str] = None
    result: Optional[str] = None
    effect_size: Optional[float] = None
    p_value: Optional[float] = None
    sample_size: Optional[int] = None
    tags: list[str] = field(default_factory=list)


def get_default_queue() -> list[Hypothesis]:
    """Return the default hypothesis queue with novel, untested hypotheses."""
    return [
        Hypothesis(
            id="early-kickoff-disadvantage",
            category="scheduling",
            title="Early Kickoff Disadvantage",
            hypothesis="Matches kicking off before 12:30 PM produce fewer total goals and fewer home wins than later kickoffs.",
            negative="Early kickoff time has no effect on match outcomes.",
            direction="Negative: early kickoff → fewer goals, lower home win rate.",
            markets_affected=["Total goals", "Match result", "Both teams to score"],
            variables_tested=["kickoff_time", "total_goals", "home_win", "first_half_goals"],
            data_requirements=["matches", "kickoff_time"],
            method="Welch's t-test + Cohen's d + 95% CI; Holm-Bonferroni correction across 4 contrasts at familywise α=0.05.",
            tags=["scheduling", "kickoff", "goals", "home-advantage"],
        ),
        Hypothesis(
            id="post-european-fatigue",
            category="scheduling",
            title="Post-European Weekend Fatigue",
            hypothesis="Teams playing in European competitions (UCL, UEL, UECL) produce worse results the following weekend compared to non-European teams.",
            negative="European participation has no effect on weekend match outcomes.",
            direction="Negative: European midweek → worse weekend performance (fewer points, more goals conceded).",
            markets_affected=["Match result", "Total goals", "Asian handicap"],
            variables_tested=["european_midweek", "weekend_points", "weekend_goals_conceded", "weekend_goal_difference"],
            data_requirements=["matches", "european_fixtures"],
            method="Welch's t-test + Cohen's d + 95% CI; compare European vs non-European teams on weekend outcomes.",
            tags=["scheduling", "europe", "fatigue", "weekend"],
        ),
        Hypothesis(
            id="international-break-hangover",
            category="scheduling",
            title="International Break Hangover",
            hypothesis="Teams with more players on international duty produce worse results in the first match after the break.",
            negative="International break has no effect on post-break match outcomes.",
            direction="Negative: more internationals → worse post-break performance.",
            markets_affected=["Match result", "Total goals", "First half goals"],
            variables_tested=["international_players_count", "post_break_points", "post_break_goals"],
            data_requirements=["matches", "international_break_dates"],
            method="Correlation + median split; Welch's t-test on high vs low international count.",
            tags=["scheduling", "internationals", "fatigue", "break"],
        ),
        Hypothesis(
            id="new-manager-bounce",
            category="squad_dynamics",
            title="New Manager Bounce",
            hypothesis="Teams appointing a new manager show improved results in the first 5 games compared to the 5 games before the appointment.",
            negative="New manager appointment has no effect on short-term results.",
            direction="Positive: new manager → improved results in first 5 games.",
            markets_affected=["Match result", "Total goals", "Asian handicap"],
            variables_tested=["manager_change", "points_before", "points_after", "goals_before", "goals_after"],
            data_requirements=["matches", "manager_appointments"],
            method="Paired t-test on points/goals before vs after manager change; Cohen's d for effect size.",
            tags=["squad", "manager", "bounce", "change"],
        ),
        Hypothesis(
            id="january-transfer-window",
            category="squad_dynamics",
            title="January Transfer Window Impact",
            hypothesis="Teams making significant January signings (3+ players) show improved results in the second half of the season.",
            negative="January transfer activity has no effect on second-half performance.",
            direction="Positive: January signings → improved second-half results.",
            markets_affected=["Match result", "Total goals", "Clean sheets"],
            variables_tested=["january_signings_count", "first_half_points", "second_half_points"],
            data_requirements=["matches", "transfer_data"],
            method="Welch's t-test comparing high-activity vs low-activity teams on second-half outcomes.",
            tags=["squad", "transfers", "january", "improvement"],
        ),
        Hypothesis(
            id="key-player-absence",
            category="squad_dynamics",
            title="Key Player Absence",
            hypothesis="Teams missing their top scorer (injury/suspension) produce fewer goals and win fewer points.",
            negative="Key player absence has no effect on match outcomes.",
            direction="Negative: top scorer absent → fewer goals, fewer points.",
            markets_affected=["Total goals", "Match result", "Both teams to score"],
            variables_tested=["top_scorer_absent", "goals_scored", "points_won"],
            data_requirements=["matches", "injury_data", "suspension_data"],
            method="Welch's t-test + Cohen's d; compare matches with and without top scorer.",
            tags=["squad", "injuries", "absence", "goals"],
        ),
        Hypothesis(
            id="overreaction-big-wins",
            category="market_pricing",
            title="Overreaction to Big Wins",
            hypothesis="Teams winning by 3+ goals are overpriced in their next match; the market overestimates their form.",
            negative="Big wins have no effect on next-match pricing or outcomes.",
            direction="Negative: big win → overpriced next match → fade value.",
            markets_affected=["Match result", "Asian handicap", "Total goals"],
            variables_tested=["big_win_last_match", "next_match_result", "next_match_closing_odds"],
            data_requirements=["matches", "odds_data"],
            method="Compare next-match results for big-win teams vs control; analyze odds movement.",
            tags=["market", "overreaction", "big-win", "fade"],
        ),
        Hypothesis(
            id="derby-home-advantage-mispricing",
            category="market_pricing",
            title="Derby Home Advantage Mispricing",
            hypothesis="Local derbies show lower home win rates than the market prices; home advantage is reduced in derby fixtures.",
            negative="Derby status has no effect on home win rates or market pricing.",
            direction="Negative: derby → lower home win rate than implied by odds.",
            markets_affected=["Match result", "Asian handicap", "Draw"],
            variables_tested=["is_derby", "home_win", "implied_home_win_prob", "actual_home_win_rate"],
            data_requirements=["matches", "odds_data", "derby_list"],
            method="Compare actual vs implied home win rates in derbies; binomial test.",
            tags=["market", "derby", "home-advantage", "mispricing"],
        ),
        Hypothesis(
            id="newly-promoted-mispricing-week10",
            category="market_pricing",
            title="Newly Promoted Team Mispricing by Week 10",
            hypothesis="By week 10, newly promoted teams are still overpriced; the market is slow to adjust to the quality gap.",
            negative="Newly promoted teams are correctly priced by week 10.",
            direction="Negative: promoted teams underperform their implied odds through week 10.",
            markets_affected=["Match result", "Asian handicap", "Total goals"],
            variables_tested=["is_promoted", "matchday_1_to_10", "points_vs_implied", "goals_vs_implied"],
            data_requirements=["matches", "odds_data", "promotion_data"],
            method="Compare actual vs implied points/goals for promoted teams in first 10 matches.",
            tags=["market", "promoted", "mispricing", "early-season"],
        ),
        Hypothesis(
            id="rain-wind-interaction",
            category="weather",
            title="Rain + Wind Interaction",
            hypothesis="The combination of rain AND strong wind suppresses goals more than either factor alone.",
            negative="Rain and wind have no interaction effect on goals.",
            direction="Negative: rain + wind → fewer goals than either alone.",
            markets_affected=["Total goals", "Both teams to score", "First half goals"],
            variables_tested=["rain_mm", "wind_kph", "total_goals", "interaction_term"],
            data_requirements=["matches", "weather_data"],
            method="Two-way ANOVA or multiple regression with interaction term; Cohen's d for combined vs single factors.",
            tags=["weather", "rain", "wind", "interaction", "goals"],
        ),
        Hypothesis(
            id="cold-weather-goal-suppression",
            category="weather",
            title="Cold Weather Goal Suppression",
            hypothesis="Matches played in temperatures below 5°C produce fewer total goals than matches above 15°C.",
            negative="Temperature has no effect on total goals.",
            direction="Negative: cold → fewer goals.",
            markets_affected=["Total goals", "Both teams to score", "First half goals"],
            variables_tested=["temperature_c", "total_goals", "first_half_goals"],
            data_requirements=["matches", "weather_data"],
            method="Welch's t-test + Cohen's d; cold (<5°C) vs warm (>15°C).",
            tags=["weather", "cold", "temperature", "goals"],
        ),
        Hypothesis(
            id="heat-wave-corner-effects",
            category="weather",
            title="Heat Wave Corner Effects",
            hypothesis="Matches played in temperatures above 25°C produce more corners due to slower defending and wider play.",
            negative="Temperature has no effect on corner counts.",
            direction="Positive: heat → more corners.",
            markets_affected=["Total corners", "Team corners", "Corner handicap"],
            variables_tested=["temperature_c", "total_corners", "home_corners", "away_corners"],
            data_requirements=["matches", "weather_data"],
            method="Welch's t-test + Cohen's d; hot (>25°C) vs moderate (10-20°C).",
            tags=["weather", "heat", "temperature", "corners"],
        ),
        Hypothesis(
            id="referee-derby-interaction",
            category="referee",
            title="Referee × Derby Interaction",
            hypothesis="High-card referees produce even more cards in derby matches than in normal matches.",
            negative="Referee card rate is not amplified in derbies.",
            direction="Positive: high-card ref + derby → more cards than either alone.",
            markets_affected=["Total cards", "Player cards", "Team cards"],
            variables_tested=["referee_card_rate", "is_derby", "total_cards", "interaction_term"],
            data_requirements=["matches", "referee_data", "derby_list"],
            method="Two-way ANOVA or regression with interaction term; Cohen's d for ref × derby.",
            tags=["referee", "derby", "cards", "interaction"],
        ),
        Hypothesis(
            id="referee-home-bias-by-card-type",
            category="referee",
            title="Referee Home Bias by Card Type",
            hypothesis="Some referees show home bias in yellow cards but not red cards; the bias is referee-specific.",
            negative="Referees do not show home bias in card distribution.",
            direction="Negative: certain refs → fewer home yellows, no difference in reds.",
            markets_affected=["Team cards", "Player cards", "Total cards"],
            variables_tested=["referee_id", "home_yellows", "away_yellows", "home_reds", "away_reds"],
            data_requirements=["matches", "referee_data", "card_data"],
            method="Referee-level analysis; paired t-test on home vs away yellows per referee.",
            tags=["referee", "home-bias", "cards", "yellow-cards"],
        ),
        Hypothesis(
            id="xg-overperformance-sustainability",
            category="xg_anomalies",
            title="xG Overperformance Sustainability",
            hypothesis="Teams significantly overperforming their xG (goals >> xG) regress toward the mean in subsequent matches.",
            negative="xG overperformance is sustainable and does not regress.",
            direction="Negative: overperformance → regression in next 5 matches.",
            markets_affected=["Total goals", "Match result", "Both teams to score"],
            variables_tested=["xg_overperformance", "next_5_goals", "next_5_xg", "regression_ratio"],
            data_requirements=["matches", "xg_data"],
            method="Identify overperformers (goals > xG + 1 SD); compare next-5-match goals vs xG.",
            tags=["xg", "overperformance", "regression", "sustainability"],
        ),
        Hypothesis(
            id="shot-quality-vs-quantity",
            category="xg_anomalies",
            title="Shot Quality vs Quantity",
            hypothesis="Teams with high xG per shot (quality) sustain performance better than teams with high shot volume but low xG per shot.",
            negative="Shot quality has no effect on performance sustainability.",
            direction="Positive: high quality → more sustainable results.",
            markets_affected=["Match result", "Total goals", "Total shots"],
            variables_tested=["xg_per_shot", "shot_volume", "points_next_5", "goals_next_5"],
            data_requirements=["matches", "xg_data", "shot_data"],
            method="Median split on xG per shot; compare sustainability of results over next 5 matches.",
            tags=["xg", "shot-quality", "shots", "sustainability"],
        ),
        Hypothesis(
            id="xg-delta-by-matchday",
            category="xg_anomalies",
            title="xG Delta by Matchday",
            hypothesis="xG differential (home xG - away xG) is a stronger predictor of result in later matchdays (15+) than early ones.",
            negative="xG differential predictive power does not vary by matchday.",
            direction="Positive: xG delta more predictive in later matchdays.",
            markets_affected=["Match result", "Asian handicap", "Total goals"],
            variables_tested=["xg_delta", "matchday", "result", "interaction_term"],
            data_requirements=["matches", "xg_data"],
            method="Logistic regression with interaction term (xg_delta × matchday); compare early vs late predictive power.",
            tags=["xg", "matchday", "predictive-power", "interaction"],
        ),
        Hypothesis(
            id="midweek-away-favoured-sides",
            category="scheduling",
            title="Midweek Away Games for Favoured Sides",
            hypothesis="Favoured sides (top half of the league) playing midweek away games underperform expectations — the classic 'rainy Tuesday in Stoke' effect. Short rest + travel + hostile midweek atmosphere reduces performance.",
            negative="Midweek away games have no effect on favoured sides' performance.",
            direction="Negative: midweek away → favoured sides underperform (fewer points, narrower wins).",
            markets_affected=["Match result", "Asian handicap", "Total goals"],
            variables_tested=["is_midweek", "is_away", "league_position", "points_won", "goal_difference"],
            data_requirements=["matches", "league_table", "fixture_congestion"],
            method="Welch's t-test + Cohen's d; compare favoured sides' midweek away results vs weekend home/away results. Control for opponent strength.",
            tags=["scheduling", "midweek", "away", "favoured", "stoke-effect"],
        ),
        Hypothesis(
            id="travel-distance-amplifies-midweek",
            category="scheduling",
            title="Travel Distance Amplifies Midweek Effect",
            hypothesis="The midweek away disadvantage for favoured sides is more pronounced the longer the journey. Teams travelling >200 miles midweek underperform those travelling <50 miles.",
            negative="Travel distance has no effect on midweek away performance.",
            direction="Negative: longer travel + midweek away → worse performance.",
            markets_affected=["Match result", "Asian handicap", "Total goals", "Team totals"],
            variables_tested=["travel_km", "is_midweek", "is_away", "points_won", "goals_scored"],
            data_requirements=["matches", "travel_matrix", "league_table"],
            method="Two-way ANOVA or regression with interaction term (travel × midweek); Cohen's d for long vs short travel midweek.",
            tags=["scheduling", "travel", "midweek", "away", "interaction"],
        ),
        Hypothesis(
            id="league-position-form-overlay",
            category="market_pricing",
            title="League Position and Form as Research Overlay",
            hypothesis="Overlaying pre-match league position and recent form (last 5 games) on existing research findings improves predictive power. Teams in the top half with strong form behave differently than bottom-half teams with poor form.",
            negative="League position and form do not modulate existing research findings.",
            direction="Positive: position + form overlay improves prediction.",
            markets_affected=["Match result", "Asian handicap", "Total goals", "All existing research markets"],
            variables_tested=["league_position", "form_last_5", "existing_finding", "interaction_term"],
            data_requirements=["matches", "league_table", "form_data"],
            method="For each existing significant finding, add league position and form as interaction terms. Test if the effect is stronger in certain position/form segments.",
            tags=["methodology", "overlay", "position", "form", "meta-analysis"],
        ),
        Hypothesis(
            id="midweek-home-advantage-erosion",
            category="scheduling",
            title="Midweek Home Advantage Erosion",
            hypothesis="Home advantage is reduced in midweek matches. Lower attendance and less hostile atmospheres diminish the home edge.",
            negative="Home advantage is consistent regardless of day of week.",
            direction="Negative: midweek → reduced home advantage.",
            markets_affected=["Match result", "Asian handicap", "Draw"],
            variables_tested=["is_midweek", "home_win_rate", "attendance", "home_goals"],
            data_requirements=["matches", "attendance_data"],
            method="Compare home win rates: weekend vs midweek. Control for team quality and opponent.",
            tags=["scheduling", "midweek", "home-advantage", "atmosphere"],
        ),
        Hypothesis(
            id="favoured-sides-away-fatigue-interaction",
            category="scheduling",
            title="Favoured Sides Away Fatigue Interaction",
            hypothesis="Favoured sides playing away after a big win (3+ goal margin) in their previous match are more likely to underperform in midweek due to squad rotation and complacency.",
            negative="Previous big win has no effect on next-match midweek performance.",
            direction="Negative: big win + midweek away → underperformance.",
            markets_affected=["Match result", "Asian handicap", "Total goals"],
            variables_tested=["big_win_previous", "is_midweek", "is_away", "points_won", "goals_scored"],
            data_requirements=["matches", "league_table"],
            method="Three-way interaction: big win × midweek × away. Welch's t-test on relevant subgroups.",
            tags=["scheduling", "fatigue", "big-win", "midweek", "away", "favoured"],
        ),
    ]


def load_queue() -> list[Hypothesis]:
    """Load queue from disk, or create default if not exists."""
    if not QUEUE_PATH.exists():
        queue = get_default_queue()
        save_queue(queue)
        return queue
    data = json.loads(QUEUE_PATH.read_text())
    return [Hypothesis(**h) for h in data]


def save_queue(queue: list[Hypothesis]) -> None:
    """Save queue to disk."""
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = [
        {
            "id": h.id,
            "category": h.category,
            "title": h.title,
            "hypothesis": h.hypothesis,
            "negative": h.negative,
            "direction": h.direction,
            "markets_affected": h.markets_affected,
            "variables_tested": h.variables_tested,
            "data_requirements": h.data_requirements,
            "method": h.method,
            "status": h.status,
            "last_tested": h.last_tested,
            "result": h.result,
            "effect_size": h.effect_size,
            "p_value": h.p_value,
            "sample_size": h.sample_size,
            "tags": h.tags,
        }
        for h in queue
    ]
    QUEUE_PATH.write_text(json.dumps(data, indent=2))


def get_next_hypothesis() -> Optional[Hypothesis]:
    """Get the next untested hypothesis, rotating by category."""
    queue = load_queue()
    untested = [h for h in queue if h.status == "untested"]
    if not untested:
        return None
    # Rotate by category: pick the category with fewest tested hypotheses
    categories = {}
    for h in queue:
        if h.status == "tested":
            categories[h.category] = categories.get(h.category, 0) + 1
    # Find the category with fewest tested
    min_count = min(categories.values()) if categories else 0
    for h in untested:
        cat_count = categories.get(h.category, 0)
        if cat_count == min_count:
            return h
    return untested[0]


def mark_tested(
    hypothesis_id: str,
    status: str,
    result: str,
    effect_size: Optional[float] = None,
    p_value: Optional[float] = None,
    sample_size: Optional[int] = None,
) -> None:
    """Mark a hypothesis as tested with results."""
    queue = load_queue()
    for h in queue:
        if h.id == hypothesis_id:
            h.status = status
            h.last_tested = date.today().isoformat()
            h.result = result
            h.effect_size = effect_size
            h.p_value = p_value
            h.sample_size = sample_size
            break
    save_queue(queue)


def get_tested_count() -> int:
    """Return number of tested hypotheses."""
    queue = load_queue()
    return sum(1 for h in queue if h.status == "tested")


def get_total_count() -> int:
    """Return total number of hypotheses in queue."""
    queue = load_queue()
    return len(queue)
