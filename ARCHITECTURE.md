# Architecture Overview

## System Layers

1. **Collection** — Harvesters for fixtures, results, weather, odds, referees, stadium data
2. **Pipeline** — Ingestion, validation, normalisation, enrichment, storage
3. **Storage** — SQLite/PostgreSQL with analysis-ready Parquet warehouse
4. **Analysis** — Hypothesis registry, statistical testing, backtesting, EV calculation
5. **Reporting** — Research notes, weekly briefs, monthly reviews, dashboards

## Design Principles

- Modular, single-responsibility components
- Reproducible pipelines with logged failures
- Pre-registered hypotheses with falsification-first testing
- Multiple-testing correction applied rigorously
- Negative results stored alongside positive results
- No monolithic designs; separation of concerns






