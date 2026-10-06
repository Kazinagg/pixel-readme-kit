"""Callout and GitHub alert components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme
from generator.layout import measure_mono_text_width, clamp_text_to_width, wrap_text_to_lines
from generator.components.base import escape_xml, validate_svg

GITHUB_ALERT_COLORS = {
    "NOTE": "#2f81f7",
    "TIP": "#238636",
    "IMPORTANT": "#8957e5",
    "WARNING": "#d29922",
    "CAUTION": "#f85149",
    "CRITICAL": "#f85149",
    "SUCCESS": "#238636",
    "INFO": "#8957e5",
}

def generate_callout(style="cyberpunk", primary=None, accent=None,
                     callout_type="note", title="SYSTEM SPECIFICATION",
                     subtitle="Dual-theme contrast > 7:1 // Monospace typography",
                     is_quote=False, width=850, height=None, mode="auto", preset=None,
                     badge_color=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    c_type_upper = str(callout_type).strip().upper() if callout_type else "NOTE"
    if badge_color:
        b_str = str(badge_color).strip()
        if b_str.startswith("#"):
            badge_col = b_str
        elif b_str.lower() == "theme":
            badge_col = prim
        elif b_str.upper() in GITHUB_ALERT_COLORS:
            badge_col = GITHUB_ALERT_COLORS[b_str.upper()]
        else:
            badge_col = b_str
    elif primary is not None:
        badge_col = prim
    else:
        badge_col = GITHUB_ALERT_COLORS.get(c_type_upper, prim)

    title_clean = escape_xml(title)
    sub_raw = str(subtitle).strip() if subtitle else ""
    tag_clean = escape_xml(callout_type.upper())
    st = style.lower()
    has_sub = bool(sub_raw)

    if is_quote:
        if st == "tactical":
            dash_w = "8,4"
            tag_str = f"▲ {tag_clean} // HAZARD"
            bw = max(144, int(measure_mono_text_width(tag_str, 10) + 24))
            badge = f'<polygon points="6 6, 12 6, 4 18, 0 18" fill="{badge_col}" opacity="0.6"/><polygon points="16 6, 22 6, 14 18, 8 18" fill="{badge_col}" opacity="0.6"/><polygon points="28 8, {28+bw-7} 8, {28+bw} 15, {28+bw} 27, {28+bw-7} 34, 28 34" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><text x="{28 + bw//2}" y="24" fill="{badge_col}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 28 + bw + 14
        elif st == "minimal":
            dash_w = "5,4"
            tag_str = f"{tag_clean} // MINIMAL"
            bw = max(115, int(measure_mono_text_width(tag_str, 9.5) + 20))
            badge = f'<rect x="8" y="8" width="{bw}" height="24" fill="{panel}" stroke="{badge_col}" stroke-width="1"/><text x="{8 + bw//2}" y="23" fill="{badge_col}" font-size="9.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 8 + bw + 14
        else:
            dash_w = "6,4"
            tag_str = f"{tag_clean} // 0x01"
            bw = max(120, int(measure_mono_text_width(tag_str, 10) + 32))
            badge = f'<rect x="8" y="8" width="{bw}" height="24" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><circle cx="20" cy="20" r="3.5" fill="{badge_col}"/><text x="{20 + (bw-12)//2}" y="24" fill="{badge_col}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 8 + bw + 14

        avail_w = max(100, width - text_x - 20)
        title_disp = clamp_text_to_width(title_clean, avail_w, 11)
        sub_lines = wrap_text_to_lines(sub_raw, avail_w, 11, max_lines=2) if has_sub else []

        def_h = 56 if len(sub_lines) > 1 else 42
        h = height if height else def_h

        if st == "tactical":
            top_rail = f'<line x1="0" y1="2" x2="{width-12}" y2="2" stroke="{badge_col}" stroke-width="2"/><line x1="{width-12}" y1="2" x2="{width-1}" y2="13" stroke="{badge_col}" stroke-width="2"/><line x1="{width-1}" y1="13" x2="{width-1}" y2="{h-4}" stroke="{badge_col}" stroke-width="2"/>'
            arrow_poly = f'<polygon points="{width-10} {h-5}, {width-2} {h-5}, {width-6} {h-1}" fill="{badge_col}"/>'
        elif st == "minimal":
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{badge_col}" stroke-width="1.5"/><path d="M {width-1} 2 L {width-1} 14" fill="none" stroke="{badge_col}" stroke-width="1.5"/><rect x="{width-4}" y="2" width="4" height="4" fill="{acc}"/>'
            arrow_poly = ""
        else:
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{badge_col}" stroke-width="2"/><line x1="{width-1}" y1="2" x2="{width-1}" y2="{h-4}" stroke="{badge_col}" stroke-width="2"/><rect x="{width-6}" y="2" width="5" height="5" fill="{badge_col}"/>'
            arrow_poly = ""

        if not has_sub:
            text_block = f'<text x="{text_x}" y="25" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>'
        elif len(sub_lines) == 1:
            text_block = f"""<text x="{text_x}" y="20" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="33" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>"""
        else:
            text_block = f"""<text x="{text_x}" y="19" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="32" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>
  <text x="{text_x}" y="45" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[1])}</text>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Background Glass (Flush left to connect with markdown quote border) -->
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>
  <!-- Top Rail -->
  {top_rail}
  <!-- Badge -->
  {badge}
  <!-- Title & Subtitle (Properly offset past badge edge) -->
  {text_block}
  <!-- DASHED BOTTOM LINE: Bridges into live markdown text -->
  <line x1="0" y1="{h-1}" x2="{width-5}" y2="{h-1}" stroke="{badge_col}" stroke-width="1.5" stroke-dasharray="{dash_w}" opacity="0.75"/>
  {arrow_poly}
</svg>"""

    else:
        # Autonomous Closed Callout (48px or 62px)
        if st == "tactical":
            tag_str = f"▲ {tag_clean} // HAZARD"
            bw = max(148, int(measure_mono_text_width(tag_str, 11) + 24))
            badge = f'<polygon points="34 10, {34+bw-7} 10, {34+bw} 17, {34+bw} 31, {34+bw-7} 38, 34 38" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><text x="{34 + bw//2}" y="28" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 34 + bw + 14
        elif st == "minimal":
            tag_str = f"{tag_clean} // MINIMAL"
            bw = max(130, int(measure_mono_text_width(tag_str, 11) + 20))
            badge = f'<rect x="16" y="11" width="{bw}" height="26" fill="{panel}" stroke="{badge_col}" stroke-width="1"/><text x="{16 + bw//2}" y="28" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 16 + bw + 14
        else:
            tag_str = f"{tag_clean} // 0x01"
            bw = max(140, int(measure_mono_text_width(tag_str, 11) + 36))
            badge = f'<rect x="14" y="10" width="{bw}" height="28" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><circle cx="26" cy="24" r="3.5" fill="{badge_col}"/><text x="{26 + (bw-12)//2}" y="28" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 14 + bw + 14

        avail_w = max(100, width - text_x - 45)
        title_disp = clamp_text_to_width(title_clean, avail_w, 11)
        sub_lines = wrap_text_to_lines(sub_raw, avail_w, 11, max_lines=2) if has_sub else []

        def_h = 62 if len(sub_lines) > 1 else 48
        h = height if height else def_h
        mid_y = h // 2

        if st == "tactical":
            body = f'<polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{badge_col}" stroke-width="1.5"/>'
            accents = f'<polygon points="10 8, 16 8, 8 20, 2 20" fill="{badge_col}" opacity="0.6"/><polygon points="20 8, 26 8, 18 20, 12 20" fill="{badge_col}" opacity="0.6"/><circle cx="{width-25}" cy="{mid_y}" r="8" fill="none" stroke="{badge_col}" stroke-width="1.5"/><polygon points="{width-28} {mid_y}, {width-22} {mid_y-4}, {width-22} {mid_y+4}" fill="{badge_col}"/>'
        elif st == "minimal":
            body = f'<rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
            accents = f'<path d="M 5 12 L 5 5 L 14 5" fill="none" stroke="{badge_col}" stroke-width="1.5"/><path d="M {width-5} 12 L {width-5} 5 L {width-14} 5" fill="none" stroke="{badge_col}" stroke-width="1.5"/>'
        else:
            body = f'<rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{badge_col}" stroke-width="1.5"/><rect x="2" y="2" width="5" height="5" fill="{badge_col}"/><rect x="{width-7}" y="2" width="5" height="5" fill="{badge_col}"/><rect x="2" y="{h-7}" width="5" height="5" fill="{badge_col}"/><rect x="{width-7}" y="{h-7}" width="5" height="5" fill="{badge_col}"/>'
            accents = f'<rect x="{width-35}" y="{mid_y - 10}" width="20" height="20" fill="{panel}"/><text x="{width-25}" y="{mid_y + 4}" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">ℹ</text>'

        if not has_sub:
            text_block = f'<text x="{text_x}" y="28" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>'
        elif len(sub_lines) == 1:
            text_block = f"""<text x="{text_x}" y="22" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="36" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>"""
        else:
            text_block = f"""<text x="{text_x}" y="20" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="34" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>
  <text x="{text_x}" y="48" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[1])}</text>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Body Chassis -->
  {body}
  <!-- Badges & Accents -->
  {badge}
  {accents}
  <!-- Text Content (Properly offset past badge edge) -->
  {text_block}
</svg>"""

    validate_svg(svg)
    return svg


