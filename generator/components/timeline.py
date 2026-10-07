"""Timeline milestone components for Pixel Readme Kit."""
from typing import Optional, Any, List, Dict
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import measure_mono_text_width, clamp_text_to_width
from generator.components.base import escape_xml, validate_svg

def generate_timeline(items=None, milestones=None, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders a vertical PCB data bus timeline with milestones and status nodes.
    items / milestones: list of dicts with: title, date, status ("COMPLETED"|"IN_PROGRESS"|"PLANNED"), desc
    """
    if items is None and milestones is not None:
        items = milestones
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
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if not items:
        items = [
            {"title": "PHASE 1: RESEARCH", "date": "2026-Q1", "status": "COMPLETED", "desc": "Initial prototype and vector specification"},
            {"title": "PHASE 2: CORE RUNTIME", "date": "2026-Q2", "status": "IN_PROGRESS", "desc": "Data visualization suite and multi-theming engine"},
            {"title": "PHASE 3: HUD STUDIO", "date": "2026-Q3", "status": "PLANNED", "desc": "Interactive web editor and production rollout"}
        ]

    step_h = 66
    k = len(items)
    total_h = 16 + k * step_h
    bus_x = 42

    milestones_svg = []
    for i, item in enumerate(items):
        node_y = 28 + i * step_h
        card_y = node_y - 18
        card_x = 70
        card_w = width - 72
        card_h = 52

        t = escape_xml(item.get("title", f"STAGE {i+1}").upper())
        d = escape_xml(item.get("date", "2026"))
        stat = str(item.get("status", "PLANNED")).upper()
        desc = escape_xml(item.get("desc", ""))

        if stat in ("COMPLETED", "DONE", "FINISHED"):
            node_col = success
            node_shape = f'<polygon points="{bus_x},{node_y-6} {bus_x+6},{node_y} {bus_x},{node_y+6} {bus_x-6},{node_y}" fill="{success}"/>'
            stat_lbl = "● COMPLETED"
        elif stat in ("IN_PROGRESS", "ACTIVE", "WIP"):
            node_col = acc
            node_shape = f"""<circle cx="{bus_x}" cy="{node_y}" r="6" fill="{acc}"/>
    <circle cx="{bus_x}" cy="{node_y}" r="10" fill="none" stroke="{acc}" stroke-width="1.2" stroke-dasharray="2 2"/>"""
            stat_lbl = "◉ IN_PROGRESS"
        else:
            node_col = text_dim
            node_shape = f'<circle cx="{bus_x}" cy="{node_y}" r="5" fill="{panel}" stroke="{border}" stroke-width="1.5"/>'
            stat_lbl = "○ PLANNED"

        # Connector trace from bus to card
        conn = f'<path d="M {bus_x+6} {node_y} L {card_x} {node_y}" stroke="{node_col}" stroke-width="1.5" stroke-dasharray="3 2"/>'

        # Card hull
        if st == "tactical":
            c_hull = f"""<polygon points="{card_x+6},{card_y} {card_x+card_w},{card_y} {card_x+card_w},{card_y+card_h-6} {card_x+card_w-6},{card_y+card_h} {card_x},{card_y+card_h} {card_x},{card_y+6}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{card_x+1}" y1="{card_y+1}" x2="{card_x+1}" y2="{card_y+card_h-1}" stroke="{node_col}" stroke-width="2.5"/>"""
        elif st == "minimal":
            c_hull = f"""<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <line x1="{card_x}" y1="{card_y}" x2="{card_x}" y2="{card_y+card_h}" stroke="{node_col}" stroke-width="2"/>"""
        else:  # cyberpunk
            c_hull = f"""<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{card_x}" y1="{card_y}" x2="{card_x+8}" y2="{card_y}" stroke="{node_col}" stroke-width="2"/>
    <line x1="{card_x}" y1="{card_y}" x2="{card_x}" y2="{card_y+8}" stroke="{node_col}" stroke-width="2"/>
    <rect x="{card_x+card_w-5}" y="{card_y+2}" width="3" height="3" fill="{node_col}"/>"""

        # Dynamic date width and text clamps
        dw = max(60, min(130, int(measure_mono_text_width(d, 11) + 18)))
        max_title_w = max(60, card_w - dw - 165)
        t_disp = clamp_text_to_width(t, max_title_w, 12)
        desc_disp = clamp_text_to_width(desc, card_w - 28, 11)

        milestones_svg.append(f"""  <g id="milestone-{i}">
    {conn}
    {node_shape}
    {c_hull}
    <!-- Milestone Header -->
    <rect x="{card_x+12}" y="{card_y+9}" width="{dw}" height="14" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="{card_x+12 + dw//2}" y="{card_y+20}" fill="{text_dim}" text-anchor="middle" class="font-time-date">{d}</text>
    <text x="{card_x+12 + dw + 10}" y="{card_y+20}" fill="{title_front}" class="font-time-title">{t_disp}</text>
    <text x="{card_x+card_w-14}" y="{card_y+20}" fill="{node_col}" text-anchor="end" class="font-time-stat">{stat_lbl}</text>
    <!-- Milestone Description -->
    <text x="{card_x+14}" y="{card_y+40}" fill="{text_dim}" class="font-time-desc">{desc_disp}</text>
  </g>""")

    joined_nodes = "\n".join(milestones_svg)
    bus_end_y = 28 + (k - 1) * step_h + 10

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-time-date {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
      .font-time-title {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 12px; font-weight: bold; }}
      .font-time-stat {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
      .font-time-desc {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: normal; }}
    </style>
  </defs>
  <!-- Vertical Data PCB Bus -->
  <line x1="{bus_x}" y1="14" x2="{bus_x}" y2="{bus_end_y}" stroke="{border}" stroke-width="2"/>
  <circle cx="{bus_x}" cy="14" r="3" fill="{prim}"/>
  <polygon points="{bus_x},{bus_end_y+6} {bus_x+4},{bus_end_y} {bus_x-4},{bus_end_y}" fill="{prim}"/>
{joined_nodes}
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
# SOCIAL PREVIEW CARDS (v4.0 - 1280x640 OpenGraph)
# ==============================================================================

