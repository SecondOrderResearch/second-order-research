-- Second Order Research — Initial SQLite Schema
-- Core table definitions and indexes

CREATE TABLE IF NOT EXISTS stadiums (
    stadium_id TEXT PRIMARY KEY,
    team_id TEXT,
    team_name TEXT,
    stadium_name TEXT,
    city TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    altitude_m INTEGER,
    pitch_type TEXT,
    pitch_dimensions TEXT,
    last_verified DATE,
    source_notes TEXT
);

CREATE TABLE IF NOT EXISTS referees (
    referee_id TEXT PRIMARY KEY,
    full_name TEXT,
    nationality TEXT,
    league_primary TEXT,
    career_start_year INTEGER,
    avg_cards_per_game REAL,
    avg_fouls_per_game REAL,
    avg_home_win_pct REAL,
    last_updated DATE,
    source_notes TEXT
);

CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    team_name TEXT,
    short_name TEXT,
    league TEXT,
    home_stadium_id TEXT REFERENCES stadiums(stadium_id),
    founded_year INTEGER,
    stadium_capacity INTEGER,
    last_updated DATE,
    source_notes TEXT
);

CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    competition TEXT,
    season TEXT,
    match_date DATE,
    kickoff_time TIME,
    home_team_id TEXT REFERENCES teams(team_id),
    away_team_id TEXT REFERENCES teams(team_id),
    referee_id TEXT REFERENCES referees(referee_id),
    stadium_id TEXT REFERENCES stadiums(stadium_id),
    attendance INTEGER,
    temperature_c REAL,
    humidity_pct REAL,
    wind_speed_kph REAL,
    precipitation_mm REAL,
    weather_condition TEXT,
    result_home_goals INTEGER,
    result_away_goals INTEGER,
    result_half_home INTEGER,
    result_half_away INTEGER,
    data_quality_flag TEXT,
    source_notes TEXT
);

CREATE TABLE IF NOT EXISTS match_events (
    event_id TEXT PRIMARY KEY,
    match_id TEXT REFERENCES matches(match_id),
    minute INTEGER,
    second INTEGER,
    event_type TEXT,
    event_team TEXT,
    player_id TEXT,
    player_name TEXT,
    assist_player_id TEXT,
    assist_player_name TEXT,
    card_type TEXT,
    shot_type TEXT,
    shot_outcome TEXT,
    foul_type TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS match_odds (
    odds_id TEXT PRIMARY KEY,
    match_id TEXT REFERENCES matches(match_id),
    bookmaker TEXT,
    market_type TEXT,
    opening_odds REAL,
    closing_odds REAL,
    odds_movement_pct REAL,
    implied_probability REAL,
    captured_at TIMESTAMP,
    source_notes TEXT
);

CREATE TABLE IF NOT EXISTS travel_matrix (
    travel_id TEXT PRIMARY KEY,
    home_team_id TEXT REFERENCES teams(team_id),
    away_team_id TEXT REFERENCES teams(team_id),
    distance_km REAL,
    estimated_time_mins INTEGER,
    derivation_method TEXT,
    last_updated DATE
);

CREATE TABLE IF NOT EXISTS rest_days (
    rest_id TEXT PRIMARY KEY,
    match_id TEXT REFERENCES matches(match_id),
    team_id TEXT REFERENCES teams(team_id),
    days_since_last_match INTEGER,
    matches_in_last_14d INTEGER,
    matches_in_last_30d INTEGER,
    is_midweek BOOLEAN,
    travel_sequence TEXT
);

CREATE TABLE IF NOT EXISTS hypothesis_registry (
    hypothesis_id TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    null_hypothesis TEXT,
    expected_direction TEXT,
    markets_affected TEXT,
    variables_tested TEXT,
    sample_size INTEGER,
    data_period TEXT,
    methodology TEXT,
    confidence_score REAL,
    status TEXT,
    last_tested DATE,
    follow_up TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    tags TEXT,
    test_family TEXT,
    power REAL,
    correction_applied TEXT,
    negative_result_treated_as TEXT
);

CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_teams ON matches(home_team_id, away_team_id);
CREATE INDEX IF NOT EXISTS idx_matches_season ON matches(season);
CREATE INDEX IF NOT EXISTS idx_match_events_match ON match_events(match_id);
CREATE INDEX IF NOT EXISTS idx_match_odds_match ON match_odds(match_id);
CREATE INDEX IF NOT EXISTS idx_rest_days_match ON rest_days(match_id);
CREATE INDEX IF NOT EXISTS idx_travel_teams ON travel_matrix(home_team_id, away_team_id);
