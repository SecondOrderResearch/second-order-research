# Data Source Anomaly — football-data.org API
**Date:** 2026-07-29  
**Status:** Blocked — requires resolution before full backfill  
**Impact:** Week 2 backfill path A deferred; fallback path B ready

## Finding
- `FOOTBALL_DATA_ORG_API_KEY` resolved from `.env` as `FOOTBALL_DATA_API_KEY` (32 chars).
- Direct API test: `GET /v4/matches?competition=PL&season=2022` returns HTTP 200, but payload is **BSA / Campeonato Brasileiro Série A** with upcoming dates (2026-07-30 to 2026-07-31), not Premier League 2022/23.
- Response metadata: `"permission":"TIER_ONE"`, `"count":3`, `"competitions":"BSA"`.
- Conclusion: either the competition filter is not being applied, or the free-tier key does not have access to PL historical fixtures via this endpoint.

## Likely causes
1. Free-tier key restricted to upcoming/limited competitions, not full PL history.
2. Season filter format incompatible with v4 API expectations.
3. Endpoint/route requires a different path for historical data.

## Decision taken
Do **not** block Week 2 on resolving football-data.org access.
Adopt **Option 2** from plan: Wikipedia + API-Football + StatsBomb Open Data for fixtures/results.
Football-data.org will be re-evaluated once a paid/upgraded key or correct endpoint is confirmed.

## Next actions
- Implement Wikipedia fixtures scraper for 2022/23–2024/25.
- Implement API-Football free-tier fallback for fixtures.
- Proceed with StatsBomb Open Data for match events.
- Document exact coverage gaps in `/research/data-quality/`.

---
*This finding is filed as a negative result in the research record: the source is available but not usable for the intended historical backfill without further qualification.*
