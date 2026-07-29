# Second Order Research — Research Roadmap v1.0

**Document Owner:** Lead Research Analyst & Technical Architect  
**Status:** Draft for Review  
**Date:** 2026-07-29  
**Classification:** Internal — Proprietary Methodology

---

# 1. Proposed System Architecture

## 1.1 Design Philosophy
Modular, pipeline-oriented architecture. Each module has a single responsibility, documented inputs/outputs, and can be developed, tested, and iterated independently.

## 1.2 Module Breakdown

| Module | Purpose | Technology | Output |
|--------|---------|------------|--------|
| Collection Scheduler | Orchestrates periodic data pulls | cron / systemd timers | Trigger events, logs |
| Fixtures Harvester | Pulls upcoming fixtures, lineups, officials | football-data.org API, scraping | fixtures_raw |
| Results Harvester | Pulls final match data (scores, events) | API-Football / StatsBomb / scraping | results_raw |
| Weather Harvester | Historical and forecast weather | Open-Meteo, Met Office API | weather_raw |
| Odds Harvester | Opening, closing, and line movement | OddsPortal scraping, Betfair API | odds_raw |
| Referee Registry | Official assignments and histories | scraping + manual curation | referees_raw |
| Travel Calculator | Haversine distances, travel time estimates | GeoPy + schedule data | travel_features |
| Rest Day Calculator | Days between fixtures per team | schedule data | rest_features |
| Pitch & Stadium Registry | Pitch type, dimensions, altitude | manual + open data | stadium_features |
| Validator | Schema checks, null audits, range checks | Python (Pandera) | validation_reports |
| Normaliser | Standardise team names, dates, timezones | Python | clean_core |
| Enricher | Join all features into match-level panel | Python/SQL | match_panel |
| Storage | Persistent storage | SQLite (dev) / PostgreSQL (prod) | database |
| Hypothesis Registry | Formal storage of tested hypotheses | YAML + database | hypothesis_entries |
| Statistical Engine | T-tests, regression, effect sizes, CI | Statsmodels / SciPy | statistical_outputs |
| Backtester | Simulates staking on identified edges | Python | backtest_results |
| EV Calculator | Estimates expected value from backtests | Python | ev_estimates |
| Reporter | Generates markdown/HTML reports | Jinja2 | research_notes |
| Dashboard | Subscriber/internal web views | Streamlit (internal), custom (sub) | web_views |

## 1.3 Technology Stack Rationale

- Python 3.11+: Primary language.
- SQLite (Phase 1) → PostgreSQL (Phase 2).
- Pandas / Polars: Data manipulation.
- Pydantic: Schema validation throughout pipelines.
- Statsmodels / SciPy: Statistical rigour.
- Git: Version control for code, data lineage docs, and hypotheses.
- Markdown + Jinja2: Research documentation.
- Streamlit: Rapid internal dashboarding.
- Docker (later): Reproducible environments.

---

# 2. Data Sources

## 2.1 Free Sources

| Data Category | Source | Reliability |
|---------------|--------|-------------|
| Fixtures & Results | football-data.org API | High |
| Match Events | StatsBomb Open Data | High |
| Weather | Open-Meteo | High |
| Stadium Info | Wikipedia + manual curation | Medium |
| Referee Assignments | Premier League / EFL sites | Medium |
| Historical Odds | football-data.co.uk | Medium |
| Travel Distances | GeoPy + stadium coordinates | High (once built) |
| Squads & Duty | Transfermarkt scraping | Medium |

## 2.2 Paid Sources (Phase 2 Evaluation)

| Data Category | Source | Cost | Notes |
|---------------|--------|------|-------|
| Premium Odds | Betfair Exchange API | Free with approved app | Best for genuine closing odds |
| Complete Event Data | StatsBomb / Opta / Wyscout | £1k–£10k+/year | Industry standard |

**Recommendation:** Defer paid sources until free data proves a hypothesis direction.

---

# 3. Initial Database Schema (SQLite / PostgreSQL)

## 3.1 Core Entities

### stadiums
```
stadium_id TEXT PRIMARY KEY
team_id TEXT
team_name TEXT
stadium_name TEXT
city TEXT
country TEXT
latitude FLOAT
longitude FLOAT
altitude_m INT
pitch_type TEXT
pitch_dimensions TEXT
last_verified DATE
source_notes TEXT
```

### referees
```
referee_id TEXT PRIMARY KEY
full_name TEXT
nationality TEXT
league_primary TEXT
career_start_year INT
avg_cards_per_game FLOAT
avg_fouls_per_game FLOAT
avg_home_win_pct FLOAT
last_updated DATE
source_notes TEXT
```

### teams
```
team_id TEXT PRIMARY KEY
team_name TEXT
short_name TEXT
league TEXT
home_stadium_id TEXT REFERENCES stadiums(stadium_id)
founded_year INT
stadium_capacity INT
last_updated DATE
source_notes TEXT
```

### matches
```
match_id TEXT PRIMARY KEY
competition TEXT
season TEXT
match_date DATE
kickoff_time TIME
home_team_id TEXT REFERENCES teams(team_id)
away_team_id TEXT REFERENCES teams(team_id)
referee_id TEXT REFERENCES referees(referee_id)
stadium_id TEXT REFERENCES stadiums(stadium_id)
attendance INT
temperature_c FLOAT
humidity_pct FLOAT
wind_speed_kph FLOAT
precipitation_mm FLOAT
weather_condition TEXT
result_home_goals INT
result_away_goals INT
result_half_home INT
result_half_away INT
data_quality_flag TEXT
source_notes TEXT
```

### match_events
```
event_id TEXT PRIMARY KEY
match_id TEXT REFERENCES matches(match_id)
minute INT
second INT
event_type TEXT
event_team TEXT
player_id TEXT
player_name TEXT
assist_player_id TEXT
assist_player_name TEXT
card_type TEXT
shot_type TEXT
shot_outcome TEXT
foul_type TEXT
notes TEXT
```

### match_odds
```
odds_id TEXT PRIMARY KEY
match_id TEXT REFERENCES matches(match_id)
bookmaker TEXT
market_type TEXT
opening_odds FLOAT
closing_odds FLOAT
odds_movement_pct FLOAT
implied_probability FLOAT
captured_at TIMESTAMP
source_notes TEXT
```

### travel_matrix
```
travel_id TEXT PRIMARY KEY
home_team_id TEXT REFERENCES teams(team_id)
away_team_id TEXT REFERENCES teams(team_id)
distance_km FLOAT
estimated_time_mins INT
derivation_method TEXT
last_updated DATE
```

### rest_days
```
rest_id TEXT PRIMARY KEY
match_id TEXT REFERENCES matches(match_id)
team_id TEXT REFERENCES teams(team_id)
days_since_last_match INT
matches_in_last_14d INT
matches_in_last_30d INT
is_midweek BOOLEAN
travel_sequence TEXT
```

### hypothesis_registry
```
hypothesis_id TEXT PRIMARY KEY
title TEXT
description TEXT
null_hypothesis TEXT
expected_direction TEXT
markets_affected TEXT[]
variables_tested TEXT[]
sample_size INT
data_period TEXT
methodology TEXT
confidence_score FLOAT
status TEXT
last_tested DATE
follow_up TEXT
created_at TIMESTAMP
updated_at TIMESTAMP
tags TEXT[]
test_family TEXT
power FLOAT
correction_applied TEXT
negative_result_treated_as TEXT
```

---

# 4. Folder Structure

```
~/SecondOrderResearch/
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   ├── raw/
│   │   ├── football-data-org/
│   │   ├── statsbomb-open/
│   │   ├── open-meteo/
│   │   ├── football-data-co-uk/
│   │   └── scraping/
│   ├── staging/
│   │   ├── fixtures/
│   │   ├── results/
│   │   ├── weather/
│   │   ├── odds/
│   │   └── merged/
│   ├── warehouse/
│   │   ├── stadiums.parquet
│   │   ├── referees.parquet
│   │   ├── matches.parquet
│   │   ├── match_events.parquet
│   │   ├── match_odds.parquet
│   │   ├── travel_matrix.parquet
│   │   └── rest_days.parquet
│   └── exports/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── logging_config.py
│   ├── collection/
│   │   ├── fixtures.py
│   │   ├── results.py
│   │   ├── weather.py
│   │   ├── odds.py
│   │   ├── referee.py
│   │   ├── stadium.py
│   │   ├── transfermarkt.py
│   │   └── scheduler.py
│   ├── pipeline/
│   │   ├── validator.py
│   │   ├── normaliser.py
│   │   ├── enricher.py
│   │   └── storage.py
│   ├── features/
│   │   ├── travel.py
│   │   ├── rest.py
│   │   ├── referee_history.py
│   │   ├── team_form.py
│   │   └── market_movement.py
│   ├── analysis/
│   │   ├── hypothesis.py
│   │   ├── regression.py
│   │   ├── effect_size.py
│   │   ├── backtesting.py
│   │   └── ev_calculator.py
│   ├── reporting/
│   │   ├── research_note.py
│   │   ├── weekly_brief.py
│   │   ├── monthly_review.py
│   │   └── dashboard.py
│   └── utils/
│       ├── geo.py
│       ├── time.py
│       ├── json_helpers.py
│       └── retry.py
├── research/
│   ├── hypotheses.yaml
│   ├── library/
│   │   ├── 2024-08-15-ref-wind-corners.md
│   │   └── ...
│   ├── weekly/
│   │   └── 2024-W33.md
│   └── monthly/
├── tests/
│   ├── test_collection.py
│   ├── test_pipeline.py
│   ├── test_features.py
│   └── test_analysis.py
├── scripts/
│   ├── backfill_historical.py
│   ├── daily_update.py
│   ├── validate_pipeline.py
│   └── run_hypothesis.py
├── docs/
│   ├── data-sources.md
│   ├── schema-design.md
│   ├── statistical-methods.md
│   ├── api-keys.md
│   └── glossary.md
└── notebooks/
    ├── 01-exploratory-fixtures.ipynb
    ├── 02-exploratory-weather.ipynb
    └── 03-hypothesis-testing.ipynb
```

---

# 5. Automation Roadmap

## Phase 1 — Foundation (Weeks 1–4)
- Configure project skeleton and Git repository.
- Implement collection/scheduler.py.
- Build fixtures, results, weather, stadium harvesters.
- Build pipeline/validator.py and pipeline/storage.py.
- Create initial database with schema from Section 3.

## Phase 2 — Enrichment (Weeks 5–8)
- Implement travel.py (GeoPy haversine matrix).
- Implement rest.py (rest days, congestion sequences).
- Implement referee_history.py (per-referee baselines).
- Build enricher.py to join all features into match panel.
- Backfill 3 seasons of UK league data.

## Phase 3 — Analysis & Hypothesis (Weeks 9–12)
- Implement hypothesis.py (formal registry and runner).
- Implement regression.py, effect_size.py, backtesting.py, ev_calculator.py.
- Deploy first 5 hypotheses through full pipeline.
- Produce first internal research note.

## Phase 4 — Reporting & Scale (Weeks 13–16)
- Implement reporting modules (research_note.py, weekly_brief.py, monthly_review.py).
- Build internal Streamlit dashboard.
- Extend data collection to opening odds and referee assignments.

## Phase 5 — Production Hardening (Month 5+)
- Migrate to PostgreSQL.
- Containerise with Docker.
- Implement CI/CD for pipeline validation.
- Extend to additional European leagues.

---

# 6. Top 20 Research Hypotheses

## Tier 1 — Immediate (Highest Feasibility + Promise)

| Rank | Hypothesis |
|------|------------|
| 1 | Referees with above-league-average foul/card ratio inflate total cards market |
| 2 | Away teams with <3 rest days see increased corners conceded |
| 3 | High wind speed (>30kph) reduces total corners and increases goal kicks/throw-ins |
| 4 | International break reduces fouls by teams with most capped players |
| 5 | Odds movement >10% toward under predicts below-market corner totals |

## Tier 2 — Short Term (Requires minor enrichment)

| Rank | Hypothesis |
|------|------------|
| 6 | Artificial pitches increase shot frequency by 5–8% |
| 7 | Long away sequences (>1000km) increase opponent fouls in first 15 minutes |
| 8 | Midweek fixtures produce more cards than weekend fixtures |
| 9 | High humidity (>80%) reduces passing accuracy, increasing shots on target conceded |
| 10 | Referees averaging >35 fouls/game inflate total fouls market |

## Tier 3 — Medium Term (Requires squad/news data)

| Rank | Hypothesis |
|------|------------|
| 11 | Managerial change within 30 days increases opponent shots on target |
| 12 | Teams with average age >29 commit fewer fouls but more cards |
| 13 | Holiday periods reduce defensive intensity, increasing corners and shots |
| 14 | Promoted teams underperform fouls baseline by 10% in top flight |
| 15 | Stadium altitude >500m reduces corner frequency |

## Tier 4 — Advanced (Requires odds/xG data)

| Rank | Hypothesis |
|------|------------|
| 16 | Opening odds <3.0 on under corners correlate with market inefficiency drop |
| 17 | Rain >5mm reduces corner frequency by 5–10% |
| 18 | Back-to-back away fixtures increase card counts via travel stress |
| 19 | xG overperformance residuals >0.3 predict lower shot counts next match |
| 20 | Foreign referees in domestic leagues show 8% higher card rates |

---

# 7. Recommended MVP

**Goal:** Prove the research pipeline end-to-end with one statistically rigorous finding within 4 weeks.

**Scope:**
- Database: SQLite with matches, match_events, stadiums, referees, travel_matrix, rest_days.
- Data: 2 full seasons (2023/24, 2024/25) of English Football League + Premier League.
- Collection: football-data.org API + StatsBomb Open Data + Open-Meteo + manual stadium registry.
- Hypothesis: Referee foul-card ratio → Total Cards (Rank 1 above).
- Analysis: Two-sample t-test + effect size + 95% CI.
- Report: Single-page internal research note.

**Success Criteria:**
- Pipeline runs from raw API → clean match panel in <1 hour.
- Hypothesis test is reproducible from a single Python script.
- Result includes p-value, Cohen's d, 95% CI, and sample size.
- Research note documents all assumptions and data quality flags.

---

# 8. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API rate limits block backfill | Medium | High | Schedule backfill over multiple days. |
| StatsBomb gaps for lower leagues | Medium | Medium | Use FBref fallback; document limitations. |
| Referee assignment data unreliable | Medium | Medium | Manual cross-check; flag estimated data. |
| Team name inconsistency across sources | High | Medium | Normaliser with fuzzy matching + manual override. |
| Confirmation bias in hypothesis selection | Medium | High | Rank hypotheses before analysis; attempt falsification. |
| Small sample sizes for rare conditions | Medium | Medium | Pre-specify minimum n (n<30 = inconclusive). |
| Market efficiency makes edges fleeting | High | Medium | Test for persistence over time (out-of-sample). |
| Regulatory issues with scraping | Low | High | Legal review before automating OddsPortal/Transfermarkt. |

---

# 9. Unknowns

1. StatsBomb coverage for Championship/League 1/2 unconfirmed until attempted.
2. Historical opening odds granularity may require paid sources.
3. Stadium-level weather vs nearest airport station difference unknown.
4. Referee tendency stability across seasons untested.
5. Optimal sample period for second-order variables not yet established.
6. Magnitude of edge needed to overcome bookmaker margin unknown.
7. UK-specific pattern generalisability to other European leagues untested.

---

# 10. Suggested First Month's Work

## Week 1 — Environment & Foundation
- Create ~/SecondOrderResearch/ folder structure.
- Initialise Git repo; create README.md, ARCHITECTURE.md.
- Set up Python virtual environment; install core deps.
- Build config.py and logging_config.py.
- Manually populate stadiums table for ≈90 UK teams.
- Document API keys and data source URLs.

## Week 2 — Collection & Ingestion
- Build fixtures.py + initial backfill for 2023/24 + 2024/25.
- Build results.py + StatsBomb downloader.
- Build weather.py + historical pull for all matches in scope.
- Build validator.py + schema definitions.
- Run first full ingestion; review validation reports; fix gaps.

## Week 3 — Enrichment & Panel
- Build travel.py (haversine matrix for all team pairs).
- Build rest.py (rest days, congestion, sequence flags).
- Build enricher.py (join matches + events + weather + travel + rest).
- Generate matches.parquet and match_events.parquet.
- Conduct exploratory data quality audit.

## Week 4 — MVP Hypothesis Execution
- Implement hypothesis script for Referee foul-card ratio → Total Cards.
- Run statistical tests; capture full output.
- Draft internal research note per template.
- Review results against falsification criteria.
- Present findings for review; determine next hypothesis queue.

---

**End of Research Roadmap v1.0**

*Note: No coding should begin until this roadmap has been reviewed and approved.*