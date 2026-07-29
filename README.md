# Second Order Research

Independent sports market intelligence focused on identifying persistent inefficiencies within football betting markets through the study of second-order variables.

**Status:** Week 1 Foundation in progress  
**Hypothesis under test:** Referee foul/card ratio × away travel distance interaction on total corners  
**Data:** 2022/23–2024/25 English Football League + Premier League  
**Methodology:** Pre-registered contrasts, Holm-Bonferroni correction, out-of-sample holdout

---

## Current Build State

| Week | Target | Status |
|------|--------|--------|
| Week 1 | Foundation setup | In progress |
| Week 2 | Data collection + enrichment | Planned |
| Week 3 | Statistical engine | Planned |
| Week 4 | MVP hypothesis execution | Planned |

## Quick Start

```bash
# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env and add API keys
```

## Documentation

- `Research_Roadmap.md` — Full plan, schema, hypotheses, risks, and methodology
- `docs/` — Data sources, API keys, statistical methods, glossary

## Structure

```
src/           Collection, pipeline, features, analysis, reporting
data/          raw → staging → warehouse → exports
research/      Hypothesis registry, library, weekly/monthly reports
scripts/       Operational scripts
notebooks/     Exploratory analysis
tests/         Unit and integration tests
```

## License

Internal — Proprietary Methodology






