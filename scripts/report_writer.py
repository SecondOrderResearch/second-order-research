"""Generate public and technical markdown reports from hypothesis test results."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

from src.config import RESEARCH_DIR


def generate_technical_report(
    hypothesis_id: str,
    title: str,
    hypothesis: str,
    negative: str,
    direction: str,
    data_source: str,
    sample: str,
    features: str,
    method: str,
    results: list[dict],
    interpretation: str,
    conclusion: str,
    lessons: list[str],
    status: str,
    effect_size: Optional[float] = None,
    p_value: Optional[float] = None,
    sample_size: Optional[int] = None,
    published: Optional[str] = None,
) -> str:
    """Generate a technical research library entry in markdown."""
    lines = [
        "# Research Library Entry",
        "",
        f"**Published:** {published or date.today().isoformat()}",
        "",
        f"**ID:** {hypothesis_id}  ",
        f"**Title:** {title}  ",
        f"**Status:** {status}  ",
        f"**Pre-registered:** Yes  ",
        f"**Hypothesis:** {hypothesis}  ",
        f"**Null hypothesis:** {negative}  ",
        f"**Direction:** {direction}  ",
        f"**Data source:** {data_source}  ",
        f"**Sample:** {sample}  ",
        f"**Features:** {features}  ",
        f"**Method:** {method}  ",
        "",
    ]

    if effect_size is not None:
        lines.append(f"**Effect size:** Cohen's d = {effect_size:.3f}  ")
    if p_value is not None:
        lines.append(f"**P-value:** {p_value:.4f}  ")
    if sample_size is not None:
        lines.append(f"**Sample size:** {sample_size}  ")

    lines.extend([
        "",
        "## Results",
        "",
        "| Contrast | n_treatment | n_control | mean_treatment | mean_control | mean_shift_pct | cohens_d | p_value | ci_95_low | ci_95_high | significant_holm |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ])

    for r in results:
        lines.append(
            f"| {r['name']} | {r.get('n_treatment', '')} | {r.get('n_control', '')} | "
            f"{r.get('mean_treatment', '')} | {r.get('mean_control', '')} | "
            f"{r.get('mean_shift_pct', '')} | {r.get('cohens_d', '')} | "
            f"{r.get('p_value', '')} | {r.get('ci_95_low', '')} | "
            f"{r.get('ci_95_high', '')} | {r.get('significant', '')} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        interpretation,
        "",
        "## Conclusion",
        "",
        conclusion,
        "",
        "## Lessons",
        "",
    ])
    for lesson in lessons:
        lines.append(f"- {lesson}")

    lines.append("")
    return "\n".join(lines)


def generate_public_report(
    title: str,
    hypothesis: str,
    direction: str,
    results: list[dict],
    interpretation: str,
    markets_affected: list[str],
    confidence: str,
    status: str,
    effect_size: Optional[float] = None,
    p_value: Optional[float] = None,
    published: Optional[str] = None,
) -> str:
    """Generate a public-facing report in markdown."""
    # Build bottom line from results
    bottom_lines = []
    for r in results[:3]:
        if str(r.get("significant", "")) == "True":
            shift = r.get("mean_shift_pct", "")
            metric = r["name"].replace("_", " ").title()
            if shift:
                bottom_lines.append(f"- {metric}: {shift}% shift (significant after correction)")

    if not bottom_lines:
        bottom_lines.append("- No contrasts reached statistical significance after correction")
        if status == "Rejected":
            bottom_lines.append("- **No betting edge identified — do not trade this angle**")

    lines = [
        f"# {title}",
        "",
        f"**Published:** {published or date.today().isoformat()}",
        "",
        f"*{hypothesis}*",
        "",
        "## Bottom Line Up Front",
        "",
    ]
    lines.extend(bottom_lines)
    lines.extend([
        "",
        f"**Direction:** {direction}  ",
        f"**Status:** {status}  ",
        "",
        "## The Read",
        "",
        interpretation,
        "",
        "## Key Numbers",
        "",
    ])

    for r in results[:3]:
        lines.append(f"- **{r['name'].replace('_', ' ').title()}**: {r.get('mean_shift_pct', 'N/A')} shift, Cohen's d = {r.get('cohens_d', 'N/A')}, p = {r.get('p_value', 'N/A')}")

    lines.extend([
        "",
        "## Market Inefficiency",
        "",
    ])

    if status == "Rejected":
        lines.append(
            "None. The pre-registered hypothesis was rejected after multiple-comparison "
            "correction — any apparent pattern in this data is indistinguishable from noise, "
            "and the market needs no adjustment for it."
        )
    else:
        lines.append(
            "The market does not fully price this effect, creating opportunities in the following markets:"
        )

    lines.extend([
        "",
        "## Betting Actions",
        "",
    ])

    if status == "Rejected":
        lines.append("No actions — there is no edge to trade on this finding.")
    else:
        lines.append("| Market | Trigger | Action |")
        lines.append("|---|---|---|")
        for market in markets_affected:
            lines.append(f"| {market} | Condition met | Bet accordingly |")

    lines.extend([
        "",
        "## Confidence",
        "",
        f"**{confidence}**",
        "",
    ])

    return "\n".join(lines)


def save_report(hypothesis_id: str, content: str, report_type: str = "public") -> Path:
    """Save a report to the research library."""
    today = date.today().isoformat()
    if report_type == "public":
        filename = f"{today}-{hypothesis_id}.md"
    else:
        filename = f"{today}-{hypothesis_id}-technical.md"
    path = RESEARCH_DIR / "library" / filename
    path.write_text(content, encoding="utf-8")
    return path
