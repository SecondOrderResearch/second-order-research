"""Build a static site for Second Order Research from the research/ markdown tree."""

from __future__ import annotations

import shutil
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
WEEKLY_DIR = RESEARCH_DIR / "weekly"
MONTHLY_DIR = RESEARCH_DIR / "monthly"
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


def _entry_created(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("**Created:**"):
            return line.split("**Created:**", 1)[1].strip().strip("*")
    return None


def _render_public_entries() -> list[dict]:
    entries: list[dict] = []
    for path in _collect_md_files(DEEPER_LIBRARY_DIR):
        html = _md_to_html(path.read_text(encoding="utf-8"), strip_top_heading=True)
        entries.append(
            {
                "slug": _entry_slug(path),
                "title": _entry_title(path, path.stem),
                "status": _entry_status(path) or "Unknown",
                "created": _entry_created(path) or "",
                "body_html": html,
            }
        )
    return entries


def _render_deeper_entries() -> list[dict]:
    entries: list[dict] = []
    for path in _collect_md_files(DEEPER_LIBRARY_DIR):
        html = _md_to_html(path.read_text(encoding="utf-8"), strip_top_heading=True)
        entries.append(
            {
                "slug": _entry_slug(path),
                "title": _entry_title(path, path.stem),
                "status": _entry_status(path) or "Unknown",
                "created": _entry_created(path) or "",
                "body_html": html,
            }
        )
    return entries


def _render_brief_list(directory: Path, label: str) -> list[dict]:
    items: list[dict] = []
    for path in _collect_md_files(directory):
        items.append(
            {
                "slug": _entry_slug(path),
                "title": _entry_title(path, path.stem),
                "summary": path.read_text(encoding="utf-8").splitlines()[0],
            }
        )
    return items


def build_site() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "library").mkdir(exist_ok=True)
    (OUT_DIR / "deeper-research").mkdir(exist_ok=True)
    (OUT_DIR / "weekly").mkdir(exist_ok=True)
    (OUT_DIR / "monthly").mkdir(exist_ok=True)
    (OUT_DIR / "founders").mkdir(exist_ok=True)
    shutil.copytree(ASSETS_DIR, OUT_DIR / "assets", dirs_exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
    )
    base = env.get_template("base.html")

    public_entries = _render_public_entries()
    deeper_entries = _render_deeper_entries()
    weekly_list = _render_brief_list(WEEKLY_DIR, "weekly")
    monthly_list = _render_brief_list(MONTHLY_DIR, "monthly")
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

    # Homepage
    home = base.render(
        page="home",
        title="Second Order Research",
        readme_html=readme_html,
        public_entries=public_entries,
        deeper_entries=deeper_entries,
        weekly_list=weekly_list,
        monthly_list=monthly_list,
        methodology_chart=methodology_chart,
    )
    (OUT_DIR / "index.html").write_text(home, encoding="utf-8")

    # Public library index
    lib_index = base.render(
        page="library",
        title="Research Library",
        public_entries=public_entries,
        deeper_entries=deeper_entries,
        weekly_list=weekly_list,
        monthly_list=monthly_list,
    )
    (OUT_DIR / "library" / "index.html").write_text(lib_index, encoding="utf-8")

    # Individual public library pages
    for entry in public_entries:
        page = base.render(
            page="entry",
            title=entry["title"],
            body_html=entry["body_html"],
            public_entries=public_entries,
            deeper_entries=deeper_entries,
            weekly_list=weekly_list,
            monthly_list=monthly_list,
        )
        (OUT_DIR / "library" / f"{entry['slug']}.html").write_text(page, encoding="utf-8")

    # Deeper research index
    deeper_index = base.render(
        page="deeper-research",
        title="Deeper Research",
        deeper_entries=deeper_entries,
        public_entries=public_entries,
        weekly_list=weekly_list,
        monthly_list=monthly_list,
    )
    (OUT_DIR / "deeper-research" / "index.html").write_text(deeper_index, encoding="utf-8")

    for entry in deeper_entries:
        page = base.render(
            page="entry",
            title=entry["title"],
            body_html=entry["body_html"],
            public_entries=public_entries,
            deeper_entries=deeper_entries,
            weekly_list=weekly_list,
            monthly_list=monthly_list,
        )
        (OUT_DIR / "deeper-research" / f"{entry['slug']}.html").write_text(page, encoding="utf-8")

    # Weekly index
    weekly_index = base.render(
        page="weekly",
        title="Weekly Notes",
        weekly_list=weekly_list,
        public_entries=public_entries,
        deeper_entries=deeper_entries,
        monthly_list=monthly_list,
    )
    (OUT_DIR / "weekly" / "index.html").write_text(weekly_index, encoding="utf-8")

    for item in weekly_list:
        content = _md_to_html(
            (WEEKLY_DIR / f"{item['slug']}.md").read_text(encoding="utf-8")
        )
        page = base.render(
            page="entry",
            title=item["title"],
            body_html=content,
            public_entries=public_entries,
            deeper_entries=deeper_entries,
            weekly_list=weekly_list,
            monthly_list=monthly_list,
        )
        (OUT_DIR / "weekly" / f"{item['slug']}.html").write_text(page, encoding="utf-8")

    # Monthly index
    monthly_index = base.render(
        page="monthly",
        title="Monthly Reviews",
        monthly_list=monthly_list,
        public_entries=public_entries,
        deeper_entries=deeper_entries,
        weekly_list=weekly_list,
    )
    (OUT_DIR / "monthly" / "index.html").write_text(monthly_index, encoding="utf-8")

    for item in monthly_list:
        content = _md_to_html(
            (MONTHLY_DIR / f"{item['slug']}.md").read_text(encoding="utf-8")
        )
        page = base.render(
            page="entry",
            title=item["title"],
            body_html=content,
            public_entries=public_entries,
            deeper_entries=deeper_entries,
            weekly_list=weekly_list,
            monthly_list=monthly_list,
        )
        (OUT_DIR / "monthly" / f"{item['slug']}.html").write_text(page, encoding="utf-8")

    # Founders
    founders = env.get_template("founders.html")
    founders_page = founders.render(
        page="founders",
        title="Founders",
        public_entries=public_entries,
        deeper_entries=deeper_entries,
        weekly_list=weekly_list,
        monthly_list=monthly_list,
    )
    (OUT_DIR / "founders" / "index.html").write_text(founders_page, encoding="utf-8")

    print(f"Site built: {OUT_DIR}")


if __name__ == "__main__":
    build_site()
