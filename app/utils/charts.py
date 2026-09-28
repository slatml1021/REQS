"""Small, dependency-free chart helpers used by the printable report."""

from html import escape


METHOD_LABELS = {"ahp": "AHP", "wiegers": "Wiegers", "volere": "Volere"}
PALETTE = {"ahp": "#1d4ed8", "wiegers": "#0f766e", "volere": "#b45309"}


def score_bars(results: list[dict]) -> str:
    """Return accessible inline SVG bars for WeasyPrint and web-safe PDF output."""
    if not results:
        return "<p class=\"muted\">Grafik için henüz hesaplanmış puan yok.</p>"
    width, row_height = 700, 32
    height = max(70, len(results) * row_height + 38)
    rows = []
    for index, result in enumerate(results):
        y = 28 + index * row_height
        score = min(100, max(0, float(result["normalized_score"])))
        label = escape(f"{result['requirement_key']} - {METHOD_LABELS.get(result['method'], result['method'])}")
        color = PALETTE.get(result["method"], "#64748b")
        rows.append(
            f'<text x="0" y="{y + 12}" class="chart-label">{label}</text>'
            f'<rect x="220" y="{y}" width="{score * 4.2:.1f}" height="18" rx="4" fill="{color}"/>'
            f'<text x="645" y="{y + 13}" class="chart-value">{score:.2f}</text>'
        )
    return (
        f'<svg class="score-chart" viewBox="0 0 {width} {height}" role="img" '
        'aria-label="Önceliklendirme puan grafiği">'
        '<style>.chart-label{font:11px DejaVu Sans,sans-serif;fill:#1e293b}.chart-value{font:11px DejaVu Sans,sans-serif;fill:#1e293b}</style>'
        + "".join(rows)
        + "</svg>"
    )
