"""Metrics, progress and techstack components for Pixel Readme Kit."""
from typing import Optional, Any, List, Dict
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import measure_mono_text_width, clamp_text_to_width
from generator.components.base import escape_xml, validate_svg

def generate_metrics(metrics=None, cards=None, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders 1 to 4 metric KPI cards in a full-width SVG row.
    metrics / cards: list of dicts with: label, value, delta (optional), trend (optional), status (optional)
    """
    if metrics is None and cards is not None:
        metrics = cards
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    success = c["success"]
    warning = c["warning"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if not metrics:
        metrics = [{"label": "SYSTEM METRIC", "value": "100%", "delta": "+0%", "trend": "neutral"}]

    card_list = metrics[:4]
    n = len(card_list)
    usable_w = width - 2
    gap = 12
    card_w = (usable_w - (n - 1) * gap) // n
    h = 92
    y = 3

    cards_svg = []
    for i, m in enumerate(card_list):
        x = 1 + i * (card_w + gap)
        label = escape_xml(m.get("label", f"METRIC {i+1}").upper())
        val = escape_xml(m.get("value", "--"))
        delta = m.get("delta")
        trend = str(m.get("trend", "")).lower()
        status = m.get("status")

        # Trend styling
        if trend == "up":
            trend_col = success
            trend_icon = "▲ "
        elif trend == "down":
            trend_col = warning
            trend_icon = "▼ "
        else:
            trend_col = text_dim
            trend_icon = "● " if delta else ""

        # Style-specific card hull
        if st == "tactical":
            hull = f"""
    <polygon points="{x+8},{y} {x+card_w},{y} {x+card_w},{y+h-8} {x+card_w-8},{y+h} {x},{y+h} {x},{y+8}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
    <polygon points="{x+card_w-12},{y+3} {x+card_w-3},{y+3} {x+card_w-3},{y+12}" fill="{acc}"/>
    <line x1="{x+10}" y1="{y+h-1}" x2="{x+card_w-10}" y2="{y+h-1}" stroke="{prim}" stroke-width="1.5" stroke-dasharray="4 2"/>
"""
        elif st == "minimal":
            hull = f"""
    <rect x="{x}" y="{y}" width="{card_w}" height="{h}" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <line x1="{x}" y1="{y}" x2="{x+card_w}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <rect x="{x+card_w-6}" y="{y+6}" width="2" height="2" fill="{prim}"/>
"""
        else:  # cyberpunk
            hull = f"""
    <rect x="{x}" y="{y}" width="{card_w}" height="{h}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
    <line x1="{x}" y1="{y+8}" x2="{x}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x}" y1="{y}" x2="{x+8}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w-8}" y1="{y}" x2="{x+card_w}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w}" y1="{y}" x2="{x+card_w}" y2="{y+8}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x}" y1="{y+h-8}" x2="{x}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x}" y1="{y+h}" x2="{x+8}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w-8}" y1="{y+h}" x2="{x+card_w}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w}" y1="{y+h-8}" x2="{x+card_w}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <rect x="{x+6}" y="{y+6}" width="2" height="2" fill="{acc}"/>
"""

        status_markup = ""
        if status:
            stat_clean = escape_xml(status.upper())
            stat_w = max(56, int(measure_mono_text_width(stat_clean, 10) + 16))
            status_markup = f"""<rect x="{x+card_w-stat_w-12}" y="{y+10}" width="{stat_w}" height="13" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{x+card_w-12-stat_w//2}" y="{y+20}" fill="{acc}" text-anchor="middle" class="font-mono-tag">{stat_clean}</text>"""
            label_disp = clamp_text_to_width(label, card_w - stat_w - 30, 11)
        else:
            label_disp = clamp_text_to_width(label, card_w - 28, 11)

        val_str = str(val)
        val_len = len(val_str)
        if val_len > 12:
            val_fs = 14
        elif val_len > 8:
            val_fs = 18
        elif val_len > 6:
            val_fs = 21
        else:
            val_fs = 26
        val_disp = clamp_text_to_width(val_str, card_w - 28, val_fs)

        delta_markup = ""
        if delta:
            d_clean = escape_xml(delta)
            d_disp = clamp_text_to_width(d_clean, card_w - 68, 11)
            delta_markup = f'<text x="{x+14}" y="{y+76}" fill="{trend_col}" class="font-mono-sub">{trend_icon}{d_disp}</text>'

        # Mini sparkline decoration in bottom right of card
        sp_x = x + card_w - 54
        sp_y = y + 74
        sparkline = f"""
    <path d="M {sp_x} {sp_y+4} L {sp_x+10} {sp_y-2} L {sp_x+20} {sp_y+6} L {sp_x+30} {sp_y-6} L {sp_x+40} {sp_y}" fill="none" stroke="{prim}" stroke-width="1.2" stroke-opacity="0.4"/>
    <circle cx="{sp_x+40}" cy="{sp_y}" r="2" fill="{acc}"/>
"""

        cards_svg.append(f"""  <g id="metric-card-{i}">
    {hull}
    <text x="{x+14}" y="{y+22}" fill="{text_dim}" class="font-mono-lbl">{label_disp}</text>
    {status_markup}
    <text x="{x+14}" y="{y+54}" fill="{title_front}" font-size="{val_fs}" class="font-mono-val">{val_disp}</text>
    {delta_markup}
    {sparkline}
  </g>""")

    joined_cards = "\n".join(cards_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h+6}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono-lbl {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }}
      .font-mono-val {{ font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 26px; font-weight: 900; letter-spacing: -0.5px; }}
      .font-mono-sub {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
      .font-mono-tag {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; }}
    </style>
  </defs>
{joined_cards}
</svg>"""

    validate_svg(svg)
    return svg

def generate_progress(value=50, label="SYSTEM PROGRESS", sub=None, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders a segmented sci-fi HUD progress bar with dithering and status readout.
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    try:
        val_clean = max(0, min(100, int(round(float(value)))))
    except Exception:
        val_clean = 50

    lbl_clean = escape_xml(label)
    sub_raw = sub if sub is not None else f"RUNTIME PROGRESS // {val_clean}% COMPLETE"
    sub_clean = escape_xml(sub_raw)

    lbl_disp = clamp_text_to_width(f"■ {lbl_clean}", width - 95, 11)
    sub_disp = clamp_text_to_width(sub_clean, width - 200, 11)

    total_segments = 32
    filled_segments = int(round(total_segments * (val_clean / 100)))

    h = 68
    track_x = 14
    track_y = 28
    track_w = width - 28
    track_h = 14

    seg_gap = 2
    seg_w = (track_w - (total_segments - 1) * seg_gap) / total_segments

    segments_svg = []
    for s in range(total_segments):
        sx = track_x + s * (seg_w + seg_gap)
        if s < filled_segments - 1:
            col = prim
            op = "1.0"
        elif s == filled_segments - 1:
            col = acc  # Active front block
            op = "1.0"
        else:
            col = border
            op = "0.2"

        segments_svg.append(f'<rect x="{sx:.1f}" y="{track_y}" width="{seg_w:.1f}" height="{track_h}" fill="{col}" fill-opacity="{op}"/>')

    joined_segments = "\n    ".join(segments_svg)

    # Style hull
    if st == "tactical":
        hull = f"""
  <polygon points="1,2 {width-1},2 {width-1},{h-10} {width-10},{h-1} 10,{h-1} 1,{h-10}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
  <polygon points="1,2 14,2 1,15" fill="{prim}"/>
  <polygon points="{width-1},2 {width-14},2 {width-1},15" fill="{acc}"/>
"""
    elif st == "minimal":
        hull = f"""
  <rect x="1" y="2" width="{width-2}" height="{h-3}" fill="{panel}" stroke="{border}" stroke-width="1"/>
  <line x1="1" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="2"/>
"""
    else:  # cyberpunk
        hull = f"""
  <rect x="1" y="2" width="{width-2}" height="{h-3}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="{width-7}" y="2" width="6" height="6" fill="{acc}"/>
  <rect x="1" y="{h-7}" width="6" height="6" fill="{acc}"/>
  <rect x="{width-7}" y="{h-7}" width="6" height="6" fill="{prim}"/>
"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-prog-lbl {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }}
      .font-prog-val {{ font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 12px; font-weight: 900; }}
      .font-prog-sub {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
    </style>
  </defs>
  {hull}
  <!-- Label & Percentage Header -->
  <text x="14" y="19" fill="{title_front}" class="font-prog-lbl">{lbl_disp}</text>
  <rect x="{width-74}" y="7" width="60" height="15" fill="{panel}" stroke="{acc}" stroke-width="1"/>
  <text x="{width-44}" y="19" fill="{acc}" text-anchor="middle" class="font-prog-val">{val_clean}%</text>

  <!-- Track & Segments -->
  <rect x="{track_x-1}" y="{track_y-1}" width="{track_w+2}" height="{track_h+2}" fill="none" stroke="{border}" stroke-width="1"/>
  <g id="segments">
    {joined_segments}
  </g>

  <!-- Subtext & Milestone Ticks -->
  <text x="14" y="56" fill="{text_dim}" class="font-prog-sub">{sub_disp}</text>
  <text x="{width-14}" y="56" fill="{text_dim}" text-anchor="end" class="font-prog-sub">0% ── 50% ── 100%</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_techstack(items=None, columns=5, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders a sci-fi HUD matrix of technology cards with embedded 20x20 pixel vector icons.
    items: list of string names e.g. ["python", "cpp", "docker", "git", "linux"]
    """
    from generator.icons import get_tech_icon_svg

    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if items is None:
        tech_list = ["python", "cpp", "rust", "docker", "git"]
    elif isinstance(items, str):
        tech_list = [x.strip() for x in items.split(",") if x.strip()]
    else:
        tech_list = list(items)

    cols = max(2, min(int(columns), 8))
    rows = (len(tech_list) + cols - 1) // cols

    usable_w = width - 2
    gap_x = 10
    gap_y = 10
    card_w = (usable_w - (cols - 1) * gap_x) // cols
    card_h = 40
    total_h = 10 + rows * (card_h + gap_y)

    items_svg = []
    for idx, item in enumerate(tech_list):
        r = idx // cols
        col = idx % cols
        x = 1 + col * (card_w + gap_x)
        y = 6 + r * (card_h + gap_y)

        if isinstance(item, dict):
            raw_name = str(item.get("name") or item.get("id") or item.get("icon") or "ITEM")
            icon_key = str(item.get("icon") or raw_name)
            sub_label = str(item.get("label", "")) if item.get("label") else None
        else:
            raw_name = str(item)
            icon_key = raw_name
            sub_label = None

        clean_name = escape_xml(raw_name.upper())
        icon_inner = get_tech_icon_svg(icon_key)

        label_markup = ""
        if sub_label:
            lbl_clean = escape_xml(sub_label.upper())
            lbl_disp = clamp_text_to_width(lbl_clean, card_w // 2 - 10, 10)
            sub_w = measure_mono_text_width(lbl_disp, 10)
            max_name_w = max(40, card_w - 42 - int(sub_w) - 10)
            clean_disp = clamp_text_to_width(clean_name, max_name_w, 11)
            label_markup = f'<text x="{x+card_w-8}" y="{y+25}" fill="{text_dim}" text-anchor="end" class="font-tech-sub">{lbl_disp}</text>'
        else:
            clean_disp = clamp_text_to_width(clean_name, card_w - 44, 11)

        if st == "tactical":
            card_bg = f"""<polygon points="{x+6},{y} {x+card_w},{y} {x+card_w},{y+card_h-6} {x+card_w-6},{y+card_h} {x},{y+card_h} {x},{y+6}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{x+card_w-4}" y1="{y+2}" x2="{x+card_w-2}" y2="{y+4}" stroke="{acc}" stroke-width="1.5"/>"""
        elif st == "minimal":
            card_bg = f"""<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <line x1="{x}" y1="{y}" x2="{x+card_w}" y2="{y}" stroke="{prim}" stroke-width="1.5"/>"""
        else:  # cyberpunk
            card_bg = f"""<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{x}" y1="{y+4}" x2="{x}" y2="{y}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="{x}" y1="{y}" x2="{x+4}" y2="{y}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="{x+card_w-4}" y1="{y+card_h}" x2="{x+card_w}" y2="{y+card_h}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="{x+card_w}" y1="{y+card_h-4}" x2="{x+card_w}" y2="{y+card_h}" stroke="{prim}" stroke-width="1.5"/>"""

        items_svg.append(f"""  <g id="tech-{idx}">
    {card_bg}
    <g transform="translate({x+10}, {y+10})" color="{prim}">
      {icon_inner}
    </g>
    <text x="{x+36}" y="{y+25}" fill="{text_main}" class="font-tech-name">{clean_disp}</text>
    {label_markup}
  </g>""")

    joined_items = "\n".join(items_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-tech-name {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }}
      .font-tech-sub {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; }}
    </style>
  </defs>
{joined_items}
</svg>"""

    validate_svg(svg)
    return svg

