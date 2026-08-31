"""Inline SVG chart helpers for Second Order Research site."""

from __future__ import annotations

from typing import Sequence


def _clean(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap_svg(content: str, width: int, height: int, title: str | None = None) -> str:
    title_block = ""
    if title:
        title_block = f'<title>{_clean(title)}</title>\n'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="svgTitle">
  {title_block}
  {content}
</svg>"""


def bar_chart(
    values: Sequence[float],
    labels: Sequence[str],
    width: int = 640,
    height: int = 360,
    title: str | None = None,
) -> str:
    if len(values) != len(labels):
        raise ValueError("values and labels must have the same length")
    if not values:
        return _wrap_svg("", width, height, title)

    max_value = max(values)
    min_value = min(values)
    span = max_value - min_value if max_value != min_value else 1
    padding = 48
    chart_width = width - padding * 2
    chart_height = height - padding * 2
    bar_count = len(values)
    bar_gap = 12
    bar_width = max(12, (chart_width - bar_gap * (bar_count + 1)) // bar_count)
    actual_chart_width = bar_count * bar_width + (bar_count - 1) * bar_gap
    offset_x = padding + (chart_width - actual_chart_width) // 2

    bars: list[str] = []
    for idx, (value, label) in enumerate(zip(values, labels)):
        bar_height = ((value - min_value) / span) * chart_height
        x = offset_x + idx * (bar_width + bar_gap)
        y = padding + chart_height - bar_height
        bars.append(
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" rx="6" fill="#0f4c81" opacity="0.9"/>'
        )
        bars.append(
            f'<text x="{x + bar_width / 2}" y="{height - 18}" text-anchor="middle" font-size="12" fill="#374151">{_clean(label)}</text>'
        )
        bars.append(
            f'<text x="{x + bar_width / 2}" y="{y - 10}" text-anchor="middle" font-size="12" fill="#1f2933">{value:.2f}</text>'
        )

    axis = (
        f'<line x1="{padding}" y1="{padding + chart_height}" x2="{width - padding}" y2="{padding + chart_height}" stroke="#e5e7eb" stroke-width="1"/>'
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{padding + chart_height}" stroke="#e5e7eb" stroke-width="1"/>'
    )
    svg_content = axis + "\n".join(bars)
    return _wrap_svg(svg_content, width, height, title)


def pipeline_diagram(
    stages: Sequence[str],
    width: int = 720,
    height: int = 260,
    title: str | None = None,
) -> str:
    if not stages:
        return _wrap_svg("", width, height, title)

    padding = 56
    chart_width = width - padding * 2
    chart_height = height - padding * 2
    box_width = 140
    box_height = 56
    gap = max(24, (chart_width - len(stages) * box_width) // (len(stages) + 1))
    arrow_width = 24
    usable_width = len(stages) * box_width + (len(stages) - 1) * (gap + arrow_width)
    start_x = padding + (chart_width - usable_width) // 2
    center_y = padding + chart_height // 2

    boxes: list[str] = []
    arrows: list[str] = []
    for idx, stage in enumerate(stages):
        x = start_x + idx * (box_width + gap + arrow_width)
        y = center_y - box_height // 2
        boxes.append(
            f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" rx="12" fill="#ffffff" stroke="#0f4c81" stroke-width="2"/>'
        )
        words = stage.split()
        lines: list[str] = []
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if len(trial) <= 18:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
        text_y = center_y - (len(lines) - 1) * 8
        for line_idx, line in enumerate(lines):
            lines[line_idx] = (
                f'<text x="{x + box_width / 2}" y="{text_y + line_idx * 18}" text-anchor="middle" font-size="12" fill="#1f2933">{_clean(line)}</text>'
            )
        boxes.extend(lines)
        if idx < len(stages) - 1:
            arrow_x = x + box_width + gap
            arrows.append(
                f'<path d="M {arrow_x} {center_y} L {arrow_x + arrow_width} {center_y}" stroke="#0f4c81" stroke-width="2" marker-end="url(#arrowhead)"/>'
            )

    defs = '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#0f4c81"/></marker></defs>'
    svg_content = defs + "\n".join(boxes + arrows)
    return _wrap_svg(svg_content, width, height, title)
