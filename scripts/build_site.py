"""Build a static site for Second Order Research from the research/ markdown tree."""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

REPO = Path(__file__).resolve().parent.parent
SITE_DIR = REPO / "site"
OUT_DIR = REPO / "docs"
TEMPLATE_DIR = SITE_DIR / "templates"
ASSETS_DIR = SITE_DIR / "assets"
CHARTS_MODULE = ASSETS_DIR / "charts.py"

import sys
sys.path.append(str(ASSETS_DIR))
from charts import bar_chart, pipeline_diagram  # noqa: E402

RESEARCH_DIR = REPO / "research"
DEEPER_LIBRARY_DIR = RESEARCH_DIR / "library"
README_PATH = REPO / "README.md"


def _md_to_html(md_text: str, strip_top_heading: bool = False) -> str:
    if strip_top_heading:
        lines = md_text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("# "):
                md_text = "\n".join(lines[:i] + lines[i + 1 :])
                break
    return markdown.markdown(
        md_text,
        extensions=[
            "tables",
            "fenced_code",
            "codehilite",
        ],
        output_format="html",
    )


def _collect_md_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"))


def _entry_slug(path: Path) -> str:
    return path.stem


def _entry_title(path: Path, default: str) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("**Title:**"):
            candidate = line.split("**Title:**", 1)[1].strip().strip("*")
            if candidate and candidate != "Research Library Entry":
                return candidate
        if line.startswith("# ") and not line.startswith("## "):
            candidate = line.lstrip("# ").strip()
            if candidate and candidate != "Research Library Entry":
                return candidate
    return default or path.stem


def _entry_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("**Status:**"):
            return line.split("**Status:**", 1)[1].strip().strip("*")
    return None


def _entry_published(path: Path) -> str | None:
    """Extract published date, prefer explicit **Published:** else filename YYYY-MM-DD."""
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("**Published:**"):
            return line.split("**Published:**", 1)[1].strip().strip("*")
    # Fall back to filename prefix
    m = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
    return m.group(1) if m else None


def _published_display(published: str | None) -> str:
    """Format 2026-08-31 -> '31 Aug 2026'."""
    if not published:
        return ""
    try:
        d = datetime.strptime(published[:10], "%Y-%m-%d")
        return d.strftime("%-d %b %Y")
    except ValueError:
        return published


def _render_public_entries() -> list[dict]:
    entries: list[dict] = []
    for path in _collect_md_files(DEEPER_LIBRARY_DIR):
        html = _md_to_html(path.read_text(encoding="utf-8"), strip_top_heading=True)
        published = _entry_published(path)
        entries.append(
            {
                "slug": _entry_slug(path),
                "title": _entry_title(path, path.stem),
                "status": _entry_status(path) or "Unknown",
                "published": published or "",
                "published_display": _published_display(published),
                "body_html": html,
            }
        )
    # Sort newest-first by published date (undated last, keep alpha order)
    entries.sort(key=lambda e: e["published"] or "0000-00-00", reverse=True)
    return entries


def build_site() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "library").mkdir(exist_ok=True)
    (OUT_DIR / "latest").mkdir(exist_ok=True)
    (OUT_DIR / "founders").mkdir(exist_ok=True)
    shutil.copytree(ASSETS_DIR, OUT_DIR / "assets", dirs_exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
    )
    base = env.get_template("base.html")

    public_entries = _render_public_entries()
    latest_entries = public_entries[-5:]
    readme_html = _md_to_html(README_PATH.read_text(encoding="utf-8"))

    methodology_chart = pipeline_diagram(
        [
            "Hypothesis",
            "Pre-register",
            "Collect",
            "Correct",
            "Falsify",
            "Publish",
        ],
        title="Second Order Research Pipeline",
    )

    # Homepage — only latest 5 entries
    home = base.render(
        page="home",
        title="Second Order Research",
        readme_html=readme_html,
        public_entries=latest_entries,
        methodology_chart=methodology_chart,
    )
    (OUT_DIR / "index.html").write_text(home, encoding="utf-8")

    # Public library index
    lib_index = base.render(
        page="library",
        title="Research Library",
        public_entries=public_entries,
    )
    (OUT_DIR / "library" / "index.html").write_text(lib_index, encoding="utf-8")

    # Individual public library pages
    for entry in public_entries:
        page = base.render(
            page="entry",
            title=entry["title"],
            body_html=entry["body_html"],
            public_entries=public_entries,
        )
        (OUT_DIR / "library" / f"{entry['slug']}.html").write_text(page, encoding="utf-8")

    # Latest research — full content of all reports
    latest_index = base.render(
        page="latest",
        title="Latest Research",
        public_entries=public_entries,
    )
    (OUT_DIR / "latest" / "index.html").write_text(latest_index, encoding="utf-8")

    # Founders
    founders = env.get_template("founders.html")
    founders_page = founders.render(
        page="founders",
        title="Founders",
        public_entries=public_entries,
    )
    (OUT_DIR / "founders" / "index.html").write_text(founders_page, encoding="utf-8")

    print(f"Site built: {OUT_DIR}")


if __name__ == "__main__":
    build_site()
