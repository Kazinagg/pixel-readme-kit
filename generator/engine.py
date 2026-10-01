"""
Core SVG Generation Engine for Pixel Readme Kit v2.2
Produces pixel-perfect, 100% valid XML SVG assets for the 3 Global Styles:
- Cyberpunk (Cyan #00C8D7 / Purple #A855F7)
- Tactical Military (Amber #F59E0B / Orange #EA580C)
- Minimal Glass (Tokyo Blue #4F8BFF / Purple #A855F7)

Full suite of rich HUD details:
- 3D Pixel Typography with layered drop-shadows
- 360° Animated Radar, CRT Scanlines, Spectrum Equalizers, Laser Scans
- 45° Chamfered hulls, corner hooks, and direct table flush boundaries (x=1..849)
- Camo proxy compliant (0 parser errors)
"""

import html
import json
import os
import xml.etree.ElementTree as ET
from generator.font_engine import render_3d_text, calculate_px_size

def load_preset(preset_name_or_path):
    """
    Loads custom color palette from a JSON file or named preset in presets/.
    """
    if not preset_name_or_path:
        return None
    path = str(preset_name_or_path).strip()
    if os.path.isfile(path):
        target_path = path
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cand1 = os.path.join(base_dir, "..", "presets", f"{path}.json")
        cand2 = os.path.join(base_dir, "..", "presets", path)
        if os.path.isfile(cand1):
            target_path = cand1
        elif os.path.isfile(cand2):
            target_path = cand2
        elif os.path.isfile(f"{path}.json"):
            target_path = f"{path}.json"
        else:
            return None
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

THEME_PALETTES = {
    "cyberpunk": {
        "dark": {
            "bg": "rgba(10, 14, 23, 0.85)",
            "panel": "rgba(15, 23, 38, 0.82)",
            "border": "rgba(30, 41, 59, 0.85)",
            "primary": "#00C8D7",
            "accent": "#A855F7",
            "title_front": "#00C8D7",
            "title_mid": "#006B74",
            "title_dark": "#002B2F",
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#00D26A",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F6F8FA",
            "panel": "#EAEFF5",
            "border": "#D0D7DE",
            "primary": "#0969DA",
            "accent": "#8250DF",
            "title_front": "#0969DA",
            "title_mid": "#0550AE",
            "title_dark": "#033D8B",
            "text_main": "#1F2328",
            "text_dim": "#57606A",
            "success": "#1A7F37",
            "warning": "#9A6700",
            "grid_op": "0.10"
        }
    },
    "tactical": {
        "dark": {
            "bg": "rgba(20, 14, 6, 0.88)",
            "panel": "rgba(30, 22, 10, 0.82)",
            "border": "rgba(50, 36, 16, 0.85)",
            "primary": "#F59E0B",
            "accent": "#EA580C",
            "title_front": "#F59E0B",
            "title_mid": "#92400E",
            "title_dark": "#451A03",
            "text_main": "#FFFBEB",
            "text_dim": "#D97706",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#FFFBEB",
            "panel": "#FEF3C7",
            "border": "#FDE68A",
            "primary": "#B45309",
            "accent": "#C2410C",
            "title_front": "#B45309",
            "title_mid": "#78350F",
            "title_dark": "#451A03",
            "text_main": "#1F2937",
            "text_dim": "#6B7280",
            "success": "#15803D",
            "warning": "#B45309",
            "grid_op": "0.10"
        }
    },
    "minimal": {
        "dark": {
            "bg": "rgba(15, 18, 30, 0.85)",
            "panel": "rgba(22, 27, 46, 0.80)",
            "border": "rgba(41, 46, 66, 0.85)",
            "primary": "#4F8BFF",
            "accent": "#A855F7",
            "title_front": "#4F8BFF",
            "title_mid": "#2563EB",
            "title_dark": "#1E3A8A",
            "text_main": "#F1F5F9",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#1D4ED8",
            "accent": "#6D28D9",
            "title_front": "#1D4ED8",
            "title_mid": "#1E40AF",
            "title_dark": "#0F172A",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.10"
        }
    }
}

STYLE_PALETTES = {
    k: v["dark"] for k, v in THEME_PALETTES.items()
}

def escape_xml(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=True)

def validate_svg(svg_content):
    """Validates that SVG content parses cleanly as XML without errors."""
    try:
        ET.fromstring(svg_content)
        return True
    except ET.ParseError as e:
        raise ValueError(f"Generated SVG has invalid XML syntax: {e}\nSVG Content:\n{svg_content}")

def is_light_color(hex_str):
    if not hex_str or not isinstance(hex_str, str):
        return False
    clean = hex_str.lstrip('#')
    if len(clean) == 6:
        try:
            r, g, b = int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return brightness > 150
        except Exception:
            return False
    return False

def darken_hex(hex_str, factor=0.4):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 6:
        try:
            r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return "#050B14"
    return "#050B14"

def get_shadow_colors(primary_hex, style="cyberpunk"):
    base = STYLE_PALETTES.get(style.lower(), STYLE_PALETTES["cyberpunk"])
    if primary_hex is None or primary_hex.lower() == base["primary"].lower():
        return base["title_mid"], base["title_dark"]
    return darken_hex(primary_hex, 0.45), darken_hex(primary_hex, 0.15)

def resolve_theme(style, mode="auto", primary=None, accent=None, preset=None):
    st = style.lower() if style else "cyberpunk"
    pal = THEME_PALETTES.get(st, THEME_PALETTES["cyberpunk"])
    dark_vals = dict(pal["dark"])
    light_vals = dict(pal["light"])

    if preset:
        preset_data = load_preset(preset)
        if preset_data:
            p_prim = preset_data.get("primary")
            p_acc = preset_data.get("accent") or preset_data.get("secondary")
            p_succ = preset_data.get("success")
            p_warn = preset_data.get("warning")
            p_bg = preset_data.get("bg_glass") or preset_data.get("bg")
            p_panel = preset_data.get("bg_panel") or preset_data.get("panel")
            p_border = preset_data.get("border_subtle") or preset_data.get("border_slate") or preset_data.get("border")

            if p_prim and not primary:
                primary = p_prim
            if p_acc and not accent:
                accent = p_acc
            if p_succ:
                dark_vals["success"] = p_succ
                light_vals["success"] = darken_hex(p_succ, 0.7) if is_light_color(p_succ) else p_succ
            if p_warn:
                dark_vals["warning"] = p_warn
                light_vals["warning"] = darken_hex(p_warn, 0.7) if is_light_color(p_warn) else p_warn
            if p_bg:
                dark_vals["bg"] = p_bg
            if p_panel:
                dark_vals["panel"] = p_panel
            if p_border:
                dark_vals["border"] = p_border

    if primary:
        dark_vals["primary"] = primary
        dark_vals["title_front"] = primary
        dark_vals["title_mid"] = darken_hex(primary, 0.45)
        dark_vals["title_dark"] = darken_hex(primary, 0.15)
        light_vals["primary"] = darken_hex(primary, 0.7) if is_light_color(primary) else primary
        light_vals["title_front"] = light_vals["primary"]
        light_vals["title_mid"] = darken_hex(light_vals["primary"], 0.6)
        light_vals["title_dark"] = darken_hex(light_vals["primary"], 0.3)

    if accent:
        dark_vals["accent"] = accent
        light_vals["accent"] = darken_hex(accent, 0.7) if is_light_color(accent) else accent

    m = mode.lower() if mode else "auto"
    if m == "dark":
        return dark_vals, ""
    elif m == "light":
        return light_vals, ""
    elif m == "transparent":
        res = dict(dark_vals)
        res["bg"] = "none"
        res["panel"] = "none"
        return res, ""
    else:  # "auto" (default: CSS variables + @media)
        colors = {
            "bg": "var(--bg-glass)",
            "panel": "var(--bg-panel)",
            "border": "var(--border-chassis)",
            "primary": "var(--primary)",
            "accent": "var(--accent)",
            "title_front": "var(--title-front)",
            "title_mid": "var(--title-mid)",
            "title_dark": "var(--title-dark)",
            "text_main": "var(--text-main)",
            "text_dim": "var(--text-dim)",
            "success": "var(--status)",
            "warning": "var(--warning)",
            "grid_op": "var(--grid-op)"
        }
        css_vars = f"""
      :root {{
        --bg-glass: {light_vals['bg']};
        --bg-panel: {light_vals['panel']};
        --border-chassis: {light_vals['border']};
        --primary: {light_vals['primary']};
        --accent: {light_vals['accent']};
        --title-front: {light_vals['title_front']};
        --title-mid: {light_vals['title_mid']};
        --title-dark: {light_vals['title_dark']};
        --text-main: {light_vals['text_main']};
        --text-dim: {light_vals['text_dim']};
        --status: {light_vals['success']};
        --warning: {light_vals['warning']};
        --grid-op: {light_vals['grid_op']};
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          --bg-glass: {dark_vals['bg']};
          --bg-panel: {dark_vals['panel']};
          --border-chassis: {dark_vals['border']};
          --primary: {dark_vals['primary']};
          --accent: {dark_vals['accent']};
          --title-front: {dark_vals['title_front']};
          --title-mid: {dark_vals['title_mid']};
          --title-dark: {dark_vals['title_dark']};
          --text-main: {dark_vals['text_main']};
          --text-dim: {dark_vals['text_dim']};
          --status: {dark_vals['success']};
          --warning: {dark_vals['warning']};
          --grid-op: {dark_vals['grid_op']};
        }}
      }}
      @media (hover: hover) {{
        .btn-hover:hover, a:hover polygon, a:hover rect {{
          filter: drop-shadow(0 0 6px var(--primary, {dark_vals['primary']}));
          cursor: pointer;
          transition: filter 0.2s ease;
        }}
      }}
"""
        return colors, css_vars

def resolve_colors(style, primary=None, accent=None, mode="auto", preset=None):
    c, _ = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    return c["primary"], c["accent"], c["bg"]


def normalize_specs(specs=None, spec1=None, spec2=None, spec3=None, default_color=None):
    """
    Normalizes specifications (level-3 header telemetry tags).
    Accepts:
    - spec1, spec2, spec3 strings
    - specs: list of tuples/strings, or pipe/semicolon/newline-delimited string
    Returns list of tuples: [(label, value, color), ...] with at most 3 items.
    If nothing is specified, returns an empty list [].
    """
    items = []
    # 1. Check individual spec1, spec2, spec3
    for s in (spec1, spec2, spec3):
        if s and str(s).strip():
            items.append(str(s).strip())

    # 2. Check specs if items is empty
    if not items and specs:
        if isinstance(specs, str):
            delim = "|" if "|" in specs else (";" if ";" in specs else "\n")
            raw_items = [p.strip() for p in specs.split(delim) if p.strip()]
            items.extend(raw_items)
        elif isinstance(specs, (list, tuple)):
            for item in specs:
                if item:
                    items.append(item)

    normalized = []
    for item in items[:3]:
        if isinstance(item, (list, tuple)):
            lbl = str(item[0]).strip()
            val = str(item[1]).strip() if len(item) > 1 else ""
            col = str(item[2]).strip() if len(item) > 2 and item[2] else default_color
            normalized.append((lbl, val, col))
        elif isinstance(item, str):
            if ":" in item:
                parts = item.split(":", 1)
                lbl = parts[0].strip()
                val = parts[1].strip()
            else:
                lbl = item.strip()
                val = ""
            normalized.append((lbl, val, default_color))

    return normalized[:3]


# ---------------------------------------------------------------------------
# 1. HEADERS (MASTER WORKSTATIONS)
# ---------------------------------------------------------------------------

def _generate_compact_header(style="cyberpunk", primary=None, accent=None,
                             title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                             tag="SYSTEM_ACTIVE", width=850, height=None, mode="auto", preset=None,
                             tag_url=None, close_url=None):
    """
    Renders a low-profile compact banner (~84px height) optimized for mobile viewports.
    """
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    st = style.lower()
    h = height if height else 84

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)

    pixel_markup, t_w, t_h = render_3d_text(
        title, x=32, y=14, px_size=3,
        front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
        spacing=2, max_width=width - 240, allow_wrap=False
    )

    y_sub = 14 + t_h + 6
    if y_sub > h - 18:
        h = y_sub + 22

    tag_w = min(200, max(120, len(tag) * 8 + 24))
    tag_x = width - tag_w - 24
    status_widget = f"""  <rect x="{tag_x}" y="24" width="{tag_w}" height="32" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
  <text x="{tag_x + tag_w//2}" y="44" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>"""

    if st == "tactical":
        hull = f"""  <polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <polygon points="2 12, 14 2, 2 2" fill="{prim}"/>
  <polygon points="{width-2} {h-12}, {width-14} {h-2}, {width-2} {h-2}" fill="{acc}"/>
  <g fill="{prim}" opacity="0.6">
    <polygon points="20 6, 26 6, 18 14, 12 14"/>
    <polygon points="30 6, 36 6, 28 14, 22 14"/>
  </g>"""
    elif st == "minimal":
        hull = f"""  <rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1"/>
  <line x1="2" y1="2" x2="{width-2}" y2="2" stroke="{prim}" stroke-width="2"/>
  <rect x="6" y="6" width="3" height="3" fill="{prim}"/>
  <rect x="{width-9}" y="6" width="3" height="3" fill="{acc}"/>"""
    else:  # cyberpunk
        hull = f"""  <rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="2" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="{width-8}" y="2" width="6" height="6" fill="{acc}"/>
  <rect x="2" y="{h-8}" width="6" height="6" fill="{acc}"/>
  <rect x="{width-8}" y="{h-8}" width="6" height="6" fill="{prim}"/>
  <line x1="2" y1="18" x2="8" y2="18" stroke="{prim}" stroke-width="1"/>
  <line x1="{width-8}" y1="{h-18}" x2="{width-2}" y2="{h-18}" stroke="{acc}" stroke-width="1"/>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
{hull}
  {pixel_markup}
  <text x="34" y="{y_sub + 12}" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">■ {sub_clean}</text>
{status_widget}
</svg>"""

    validate_svg(svg)
    return svg

def generate_header(style="cyberpunk", primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                    specs=None, spec1=None, spec2=None, spec3=None,
                    tag="SYSTEM_ACTIVE", width=850, height=None, mode="auto", preset=None,
                    tag_url=None, close_url=None, compact=False):
    if compact and str(compact).lower() in ("true", "1", "yes", "compact"):
        return _generate_compact_header(
            style=style, primary=primary, accent=accent, title=title, subtitle=subtitle,
            tag=tag, width=width, height=height, mode=mode, preset=preset,
            tag_url=tag_url, close_url=close_url
        )

    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    warning = c["warning"]
    grid_op = c["grid_op"]
    front_color = c["title_front"]
    mid_shadow = c["title_mid"]
    dark_shadow = c["title_dark"]

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)
    st = style.lower()

    # Dynamic subtitle box width
    sub_w = min(480, max(260, int(len(subtitle) * 7.5) + 36))

    # Normalize specs (max 3 items, [] if omitted)
    norm_specs = normalize_specs(specs=specs, spec1=spec1, spec2=spec2, spec3=spec3, default_color=None)

    if st == "tactical":
        y_title = 50
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=None,
            front_color=front_color, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=480, allow_wrap=True
        )
        y_sub = y_title + t_h + 8
        sub_bottom = y_sub + 24

        spec_lines = []
        if norm_specs:
            y_specs_start = sub_bottom + 25
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                val_col = spec[2] if (len(spec) > 2 and spec[2]) else text_main
                y = y_specs_start + i * 20
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="11" class="font-mono">&gt; {escape_xml(lbl)}: <tspan fill="{val_col}">{escape_xml(val)}</tspan></text>
""")
            last_spec_y = y_specs_start + (len(norm_specs[:3]) - 1) * 20
            content_bottom = last_spec_y + 6
        else:
            content_bottom = sub_bottom

        specs_markup = "".join(spec_lines)

        needed_h = content_bottom + 36
        calc_h = max(220, needed_h)
        h = max(height or 0, calc_h)

        reticle_cy = max(105, min(h - 80, (h // 2) - 5))

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      @keyframes targetScan {{
        0% {{ transform: translateX(0px); opacity: 0; }}
        15% {{ opacity: 0.85; }}
        85% {{ opacity: 0.85; }}
        100% {{ transform: translateX({width-120}px); opacity: 0; }}
      }}
      @keyframes pulseLock {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.45; transform: scale(0.96); }}
      }}
      @keyframes chevronBlink {{
        0%, 100% {{ opacity: 0.95; }}
        50% {{ opacity: 0.35; }}
      }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .laser-scan {{ animation: targetScan 4s ease-in-out infinite; }}
      .reticle-pulse {{ transform-origin: 750px {reticle_cy}px; animation: pulseLock 2s infinite ease-in-out; }}
      .chevron-pulse {{ animation: chevronBlink 1.6s infinite steps(1); }}
    </style>
  </defs>

  <!-- 1. 45° CHAMFERED CHASSIS -->
  <polygon points="20 4, {width-20} 4, {width-4} 20, {width-4} {h-20}, {width-20} {h-4}, 20 {h-4}, 4 {h-20}, 4 20"
           fill="{bg}" stroke="{border}" stroke-width="2"/>
  
  <polygon points="24 10, {width-24} 10, {width-10} 24, {width-10} {h-24}, {width-24} {h-10}, 24 {h-10}, 10 {h-24}, 10 24"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.75"/>

  <!-- HAZARD STRIPES TOP-LEFT -->
  <g fill="{prim}" class="chevron-pulse">
    <polygon points="30 14, 38 14, 26 26, 18 26"/>
    <polygon points="44 14, 52 14, 40 26, 32 26"/>
    <polygon points="58 14, 66 14, 54 26, 46 26"/>
  </g>

  <!-- TACTICAL TITLE BAR -->
  <text x="80" y="24" fill="{prim}" font-size="11" font-weight="bold" letter-spacing="1.5" class="font-mono">
    // TACTICAL.HUD // SEC_CLASS_ALPHA // SYSTEM_READY // {tag_clean}
  </text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE -->
  <rect x="42" y="{y_sub}" width="{sub_w}" height="24" fill="{panel}" stroke="{acc}" stroke-width="1"/>
  <text x="54" y="{y_sub+16}" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">
    [TARGET] {sub_clean}
  </text>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- RIGHT SIDE: TARGET LOCK-ON CROSSHAIR RETICLE -->
  <g class="reticle-pulse">
    <circle cx="750" cy="{reticle_cy}" r="45" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8,4"/>
    <circle cx="750" cy="{reticle_cy}" r="24" fill="none" stroke="{acc}" stroke-width="1.5"/>
    <circle cx="750" cy="{reticle_cy}" r="4" fill="{acc}"/>
    <line x1="750" y1="{reticle_cy - 55}" x2="750" y2="{reticle_cy - 30}" stroke="{prim}" stroke-width="2"/>
    <line x1="750" y1="{reticle_cy + 30}" x2="750" y2="{reticle_cy + 55}" stroke="{prim}" stroke-width="2"/>
    <line x1="695" y1="{reticle_cy}" x2="720" y2="{reticle_cy}" stroke="{prim}" stroke-width="2"/>
    <line x1="780" y1="{reticle_cy}" x2="805" y2="{reticle_cy}" stroke="{prim}" stroke-width="2"/>
    <path d="M 725 {reticle_cy - 25} L 720 {reticle_cy - 25} L 720 {reticle_cy - 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 775 {reticle_cy - 25} L 780 {reticle_cy - 25} L 780 {reticle_cy - 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 725 {reticle_cy + 25} L 720 {reticle_cy + 25} L 720 {reticle_cy + 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 775 {reticle_cy + 25} L 780 {reticle_cy + 25} L 780 {reticle_cy + 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <text x="750" y="{reticle_cy + 63}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">TARGET LOCK</text>
  </g>

  <!-- SWEEPING TARGET LASER -->
  <g class="laser-scan">
    <line x1="50" y1="10" x2="50" y2="{h-10}" stroke="{acc}" stroke-width="1.5" opacity="0.8"/>
    <circle cx="50" cy="20" r="3" fill="{acc}"/>
    <circle cx="50" cy="{h-20}" r="3" fill="{acc}"/>
  </g>
</svg>"""

    elif st == "minimal":
        y_title = 36
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=None,
            front_color=front_color, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=500, allow_wrap=True
        )
        y_sub = y_title + t_h + 8
        sub_bottom = y_sub + 22

        spec_lines = []
        if norm_specs:
            y_specs_start = sub_bottom + 22
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                val_col = spec[2] if (len(spec) > 2 and spec[2]) else text_main
                y = y_specs_start + i * 18
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="10" class="font-mono">// {escape_xml(lbl)}: <tspan fill="{val_col}">{escape_xml(val)}</tspan></text>
""")
            last_spec_y = y_specs_start + (len(norm_specs[:3]) - 1) * 18
            content_bottom = last_spec_y + 4
        else:
            content_bottom = sub_bottom

        specs_markup = "".join(spec_lines)

        min_default_h = 135 if not norm_specs else (140 + len(norm_specs[:3]) * 18)
        needed_h = content_bottom + 34
        calc_h = max(min_default_h, needed_h)
        h = max(height or 0, calc_h)

        eq_y = max(35, min(h - 75, (h // 2) - 25))

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      @keyframes eqBar1 {{ 0%, 100% {{ height: 12px; y: 28px; }} 50% {{ height: 32px; y: 8px; }} }}
      @keyframes eqBar2 {{ 0%, 100% {{ height: 28px; y: 12px; }} 50% {{ height: 10px; y: 30px; }} }}
      @keyframes eqBar3 {{ 0%, 100% {{ height: 18px; y: 22px; }} 50% {{ height: 36px; y: 4px; }} }}
      @keyframes eqBar4 {{ 0%, 100% {{ height: 34px; y: 6px; }} 50% {{ height: 14px; y: 26px; }} }}
      @keyframes eqBar5 {{ 0%, 100% {{ height: 22px; y: 18px; }} 50% {{ height: 8px; y: 32px; }} }}
      @keyframes neonBreath {{ 0%, 100% {{ opacity: 0.9; }} 50% {{ opacity: 0.45; }} }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .eq1 {{ animation: eqBar1 1.2s infinite ease-in-out; }}
      .eq2 {{ animation: eqBar2 0.9s infinite ease-in-out; }}
      .eq3 {{ animation: eqBar3 1.4s infinite ease-in-out; }}
      .eq4 {{ animation: eqBar4 1.1s infinite ease-in-out; }}
      .eq5 {{ animation: eqBar5 1.5s infinite ease-in-out; }}
      .breath {{ animation: neonBreath 3s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- BACKGROUND GLASS -->
  <rect x="4" y="4" width="{width-8}" height="{h-8}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="8" y="8" width="{width-16}" height="{h-16}" fill="none" stroke="{prim}" stroke-width="1.5" class="breath"/>

  <!-- CORNER PIXEL ACCENTS -->
  <rect x="4" y="4" width="8" height="3" fill="{prim}"/>
  <rect x="4" y="4" width="3" height="8" fill="{prim}"/>
  <rect x="{width-12}" y="4" width="8" height="3" fill="{prim}"/>
  <rect x="{width-7}" y="4" width="3" height="8" fill="{prim}"/>
  <rect x="4" y="{h-7}" width="8" height="3" fill="{prim}"/>
  <rect x="4" y="{h-12}" width="3" height="8" fill="{prim}"/>
  <rect x="{width-12}" y="{h-7}" width="8" height="3" fill="{prim}"/>
  <rect x="{width-7}" y="{h-12}" width="3" height="8" fill="{prim}"/>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE CHIP -->
  <g transform="translate(42, {y_sub})">
    <rect x="0" y="0" width="{sub_w}" height="22" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="12" y="15" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">⚡ {sub_clean}</text>
  </g>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- EQUALIZER BARS (RIGHT SIDE) -->
  <g transform="translate({width-120}, {eq_y})">
    <rect x="0" y="28" width="8" height="12" fill="{prim}" class="eq1"/>
    <rect x="14" y="12" width="8" height="28" fill="{acc}" class="eq2"/>
    <rect x="28" y="22" width="8" height="18" fill="#06B6D4" class="eq3"/>
    <rect x="42" y="6" width="8" height="34" fill="{warning}" class="eq4"/>
    <rect x="56" y="18" width="8" height="22" fill="{success}" class="eq5"/>
    <text x="32" y="52" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">LIVE_AUDIO</text>
  </g>
</svg>"""

    else:
        # Cyberpunk Workstation (Default Flagship: 360° Animated Radar, CRT Scanline, 20px Grid, Equalizer)
        y_title = 60
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=None,
            front_color=front_color, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=480, allow_wrap=True
        )
        y_sub = y_title + t_h + 8
        sub_bottom = y_sub + 28

        teletype_block = ""
        if norm_specs:
            teletype_svg = []
            y_teletype_start = max(182, sub_bottom + 28)
            default_colors = [prim, acc, success]
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                col = spec[2] if (len(spec) > 2 and spec[2]) else default_colors[i % 3]
                y_pos = y_teletype_start + i * 20
                teletype_svg.append(f"""
    <text x="42" y="{y_pos}" fill="{success}" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="{y_pos}" fill="{text_main}" font-size="11" class="font-mono">{escape_xml(lbl)}:</text>
    <text x="210" y="{y_pos}" fill="{col}" font-size="11" font-weight="bold" class="font-mono">{escape_xml(val)}</text>
""")

            last_y = y_teletype_start + (len(norm_specs[:3]) - 1) * 20
            eq_offset = last_y - 210
            content_bottom = last_y + 12
            teletype_block = f"""
  <!-- TELETYPE TELEMETRY LINES -->
  <g>
    {''.join(teletype_svg)}
    <rect x="500" y="{last_y - 10}" width="8" height="12" fill="{prim}" class="cursor-blink"/>
  </g>

  <!-- MINI SPECTRUM EQUALIZER -->
  <g transform="translate(525, {eq_offset})">
    <rect x="0" y="198" width="5" height="6" fill="{prim}" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="{acc}" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="#FF0055" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="{warning}" class="w4"/>
  </g>
"""
        else:
            content_bottom = sub_bottom

        min_default_h = 260
        needed_h = content_bottom + 48
        calc_h = max(min_default_h, needed_h)
        h = max(height or 0, calc_h)

        grid_lines = []
        for x in range(0, width + 1, 20):
            grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{prim}" stroke-width="1"/>')
        for y in range(0, h + 1, 20):
            grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{prim}" stroke-width="1"/>')

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes ledFlicker {{
        0%, 100% {{ fill: {success}; }}
        50% {{ fill: #004411; }}
      }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.35; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY({h}px); opacity: 0; }}
      }}
      @keyframes waveBar1 {{ 0%, 100% {{ height: 6px; y: 198px; }} 50% {{ height: 20px; y: 184px; }} }}
      @keyframes waveBar2 {{ 0%, 100% {{ height: 18px; y: 186px; }} 50% {{ height: 8px; y: 196px; }} }}
      @keyframes waveBar3 {{ 0%, 100% {{ height: 12px; y: 192px; }} 50% {{ height: 22px; y: 182px; }} }}
      @keyframes waveBar4 {{ 0%, 100% {{ height: 22px; y: 182px; }} 50% {{ height: 10px; y: 194px; }} }}
      .font-mono {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      }}
      .cursor-blink {{
        animation: blink 1s infinite steps(1);
      }}
      .status-led {{
        animation: ledFlicker 1.8s infinite steps(1);
      }}
      .scan-line {{
        animation: crtScanline 6s linear infinite;
      }}
      .w1 {{ animation: waveBar1 1.1s infinite ease-in-out; }}
      .w2 {{ animation: waveBar2 0.8s infinite ease-in-out; }}
      .w3 {{ animation: waveBar3 1.3s infinite ease-in-out; }}
      .w4 {{ animation: waveBar4 0.9s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. TRANSLUCENT GLASS BACKGROUND -->
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>

  <!-- 2. MATRIX RETRO GRID PATTERN -->
  <g opacity="{grid_op}">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{prim}" stroke-width="2" class="scan-line"/>

  <!-- 4. OUTER CHASSIS / BORDER -->
  <rect x="6" y="6" width="{width-12}" height="{h-12}" fill="none" stroke="{border}" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{h-24}" fill="none" stroke="{prim}" stroke-width="2" opacity="0.85"/>

  <!-- CORNER ACCENT BRACKETS -->
  <rect x="6" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="6" y="{h-12}" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="{h-30}" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="{h-12}" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="{h-30}" width="6" height="24" fill="{prim}"/>

  <!-- TOP CONSOLE STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="{panel}"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="{prim}" stroke-width="1.5" opacity="0.6"/>

  <circle cx="28" cy="25" r="4" fill="{success}" class="status-led"/>
  <text x="38" y="29" fill="{success}" font-size="11" font-weight="bold" class="font-mono">SYS: ONLINE // 0x00</text>

  <rect x="175" y="19" width="2" height="12" fill="{border}"/>
  <text x="188" y="29" fill="{text_dim}" font-size="11" class="font-mono">HUD: ACTIVE_SYS</text>

  <rect x="360" y="19" width="2" height="12" fill="{border}"/>
  <text x="372" y="29" fill="{text_dim}" font-size="11" class="font-mono">MODE: {st.upper()}_HUD</text>

  <!-- Tag right-anchored to never collide with window controls -->
  {f'<a href="{escape_xml(tag_url)}" target="_blank" class="btn-hover">' if tag_url else ''}<text x="{width-95}" y="29" fill="{warning}" font-size="11" font-weight="bold" text-anchor="end" class="font-mono">{tag_clean}</text>{'</a>' if tag_url else ''}

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="{border}"/>
  <text x="{width-80}" y="28" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="{border}"/>
  <text x="{width-59}" y="29" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">□</text>
  {f'<a href="{escape_xml(close_url)}" target="_blank" class="btn-hover">' if close_url else ''}<rect x="{width-41}" y="19" width="16" height="12" fill="#FF0055"/><text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>{'</a>' if close_url else ''}

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE: ROLE & SPECIALIZATION -->
  <g transform="translate(42, {y_sub})">
    <rect x="0" y="0" width="{sub_w}" height="26" fill="{panel}" stroke="{acc}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="{sub_w-4}" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{acc}"/>
    <rect x="{sub_w-4}" y="22" width="6" height="6" fill="{acc}"/>
    <text x="12" y="18" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ {sub_clean}
    </text>
  </g>

  {teletype_block}

  <!-- RIGHT SIDE: RETRO SCI-FI WORKBENCH / MONITOR HUD (RADAR) -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="{panel}" stroke="{border}" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>

    <!-- Concentric Range Rings -->
    <circle cx="85" cy="70" r="50" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{prim}" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{prim}" stroke-width="1" opacity="0.3"/>

    <!-- 360° Rotating Radar Beam -->
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="{success}" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="{warning}"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>

    <!-- Pulsing Radar Target Blips -->
    <circle cx="110" cy="50" r="3" fill="#FF0055">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="65" cy="85" r="2.5" fill="{success}">
      <animate attributeName="opacity" values="0.1;0.9;0.1" dur="3s" repeatCount="indefinite"/>
    </circle>

    <!-- Radar Telemetry Label -->
    <text x="85" y="132" fill="{success}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">RADAR: ACTIVE (360°)</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{h-26}" x2="{width-14}" y2="{h-26}" stroke="{border}" stroke-width="1"/>
  <text x="24" y="{h-15}" fill="{text_dim}" font-size="9" class="font-mono">HUD_ARCH: V3.0 // DUAL_THEME: PASS // SMART_LAYOUT</text>
  <text x="{width-24}" y="{h-15}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">READY // ID: 0xDEADBEEF</text>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 2. FOOTERS (CLOSING PLATES)
# ---------------------------------------------------------------------------

def generate_footer(style="cyberpunk", primary=None, accent=None,
                    status="SESSION_ACTIVE // STANDBY", nav_text="RETURN TO TOP",
                    sub_text=None, width=850, height=76, mode="auto", preset=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    status_clean = escape_xml(status)
    nav_clean = escape_xml(nav_text)
    st = style.lower()

    clean_nav = nav_clean.strip()
    if not clean_nav.startswith("▲") and not clean_nav.startswith("["):
        clean_nav = f"▲ {clean_nav} ▲"

    if st == "tactical":
        sub_default = "GRID: 34-BRAVO // CHECKSUM: 0x9AF4B // SENSORS: PASSIVE_SCAN // AUTH: VERIFIED"
        sub_disp = escape_xml(sub_text if sub_text else sub_default)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Tactical Heavy 45° Chamfer Hull -->
  <polygon points="18 2, {width-18} 2, {width-2} 18, {width-2} {height-18}, {width-18} {height-2}, 18 {height-2}, 2 {height-18}, 2 18"
           fill="{bg}" stroke="{border}" stroke-width="2"/>
  <polygon points="20 5, {width-20} 5, {width-5} 20, {width-5} {height-20}, {width-20} {height-5}, 20 {height-5}, 5 {height-20}, 5 20"
           fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>

  <!-- Top Tactical Hazard Rail -->
  <polygon points="26 8, 32 8, 24 18, 18 18" fill="{prim}" opacity="0.85"/>
  <polygon points="36 8, 42 8, 34 18, 28 18" fill="{prim}" opacity="0.85"/>
  <polygon points="46 8, 52 8, 44 18, 38 18" fill="{prim}" opacity="0.85"/>
  <text x="64" y="16" fill="{acc}" font-size="11" font-weight="bold" letter-spacing="1.5" class="font-mono">SEC_DEFCON_1 // FIELD_TERMINATION_PROTOCOL</text>
  <line x1="390" y1="13" x2="{width-210}" y2="13" stroke="{prim}" stroke-width="1" stroke-dasharray="8,4" opacity="0.4"/>
  <text x="{width-200}" y="16" fill="{acc}" font-size="11" font-weight="bold" class="font-mono">[SEC_CLEAR]</text>

  <!-- Left Main Status Readout -->
  <polygon points="24 26, 116 26, 122 32, 122 42, 116 48, 24 48" fill="rgba(245, 158, 11, 0.22)" stroke="{prim}" stroke-width="1.5"/>
  <text x="70" y="40" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">▲ ARMED ▲</text>
  <text x="132" y="42" fill="{prim}" font-size="12" font-weight="bold" class="font-mono">{status_clean}</text>

  <!-- Sub-diagnostic Telemetry -->
  <text x="24" y="63" fill="{acc}" font-size="11" class="font-mono">{sub_disp}</text>

  <!-- Center Chevron Cascade -->
  <g transform="translate({width//2 - 25}, 36)">
    <polygon points="0 0, 7 5, 0 10" fill="{prim}" opacity="0.5"/>
    <polygon points="12 0, 19 5, 12 10" fill="{prim}" opacity="0.8"/>
    <polygon points="24 0, 31 5, 24 10" fill="{prim}" opacity="1"/>
    <polygon points="36 0, 43 5, 36 10" fill="{prim}" opacity="0.8"/>
    <polygon points="48 0, 55 5, 48 10" fill="{prim}" opacity="0.5"/>
  </g>

  <!-- Right Tactical Return Button -->
  <g transform="translate({width-195}, 22)" class="btn-hover">
    <polygon points="12 0, 172 0, 182 10, 182 32, 172 42, 0 42, 0 12" fill="rgba(245, 158, 11, 0.2)" stroke="{prim}" stroke-width="1.5"/>
    <text x="91" y="24" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{clean_nav}</text>
    <text x="91" y="36" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">[ ELEVATION: 000 ]</text>
  </g>
</svg>"""

    elif st == "minimal":
        sub_default = "LATENCY: 0.04ms • ALL SYSTEMS GREEN • MIT LICENSE 2026"
        sub_disp = escape_xml(sub_text if sub_text else sub_default)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Hairline Glass Footer Chassis -->
  <rect x="1" y="2" width="{width-2}" height="{height-4}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="2" width="{width-2}" height="2" fill="{prim}" opacity="0.9"/>
  <!-- Corner Hairline Hooks -->
  <path d="M 6 16 L 6 6 L 16 6" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-6} 16 L {width-6} 6 L {width-16} 6" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 6 {height-16} L 6 {height-6} L 16 {height-6}" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-6} {height-16} L {width-6} {height-6} L {width-16} {height-6}" fill="none" stroke="{prim}" stroke-width="1.5"/>

  <!-- Top Micro-Header Line -->
  <text x="24" y="16" fill="{text_dim}" font-size="11" class="font-mono">// TERMINAL_SESSION // KERNEL v3.0</text>
  <line x1="220" y1="13" x2="{width-220}" y2="13" stroke="{border}" stroke-width="1"/>
  <text x="{width-24}" y="16" fill="{text_dim}" font-size="11" text-anchor="end" class="font-mono">END_OF_PAGE</text>

  <!-- Main Status Row -->
  <circle cx="28" cy="38" r="4" fill="{prim}"/>
  <circle cx="28" cy="38" r="7" fill="none" stroke="{prim}" stroke-width="1" opacity="0.4"/>
  <text x="44" y="42" fill="{text_main}" font-size="11.5" font-weight="bold" class="font-mono">STATUS: <tspan fill="{prim}">{status_clean}</tspan></text>

  <!-- Secondary Telemetry Line -->
  <text x="24" y="62" fill="{text_dim}" font-size="11" class="font-mono">{sub_disp}</text>

  <!-- Center Spectrum Waveform -->
  <g transform="translate({width//2 - 20}, 32)">
    <rect x="0" y="4" width="3" height="12" fill="{prim}" opacity="0.6"/>
    <rect x="6" y="1" width="3" height="18" fill="{acc}" opacity="0.8"/>
    <rect x="12" y="7" width="3" height="9" fill="{prim}" opacity="0.5"/>
    <rect x="18" y="0" width="3" height="20" fill="{acc}" opacity="1"/>
    <rect x="24" y="5" width="3" height="11" fill="{prim}" opacity="0.7"/>
    <rect x="30" y="2" width="3" height="16" fill="{acc}" opacity="0.8"/>
    <rect x="36" y="6" width="3" height="10" fill="{prim}" opacity="0.5"/>
  </g>

  <!-- Right Clean Return Button -->
  <g class="btn-hover">
    <rect x="{width-180}" y="24" width="160" height="34" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
    <text x="{width-100}" y="45" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{clean_nav}</text>
  </g>
</svg>"""

    else:
        # Cyberpunk Chassis
        sub_default = '<tspan fill="' + acc + '">RUNTIME:</tspan> BUFFER_CLEARED <tspan fill="rgba(148, 163, 184, 0.4)">|</tspan> <tspan fill="' + acc + '">PACKET_LOSS:</tspan> 0.00% <tspan fill="rgba(148, 163, 184, 0.4)">|</tspan> <tspan fill="' + acc + '">LINK_QUALITY:</tspan> 100%_LOCKED'
        sub_disp = sub_text if sub_text else sub_default
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: #1E293B; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>
  <!-- Cyberpunk Heavy Chassis -->
  <rect x="1" y="2" width="{width-2}" height="{height-4}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="4" y="5" width="{width-8}" height="{height-10}" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>

  <!-- 4 Corner Pixel Brackets 6x6 -->
  <rect x="1" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="{width-7}" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="1" y="{height-8}" width="6" height="6" fill="{acc}"/>
  <rect x="{width-7}" y="{height-8}" width="6" height="6" fill="{acc}"/>

  <!-- Top Micro-Rail -->
  <line x1="12" y1="9" x2="{width-12}" y2="9" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <text x="14" y="16" fill="{acc}" font-size="11" font-weight="bold" class="font-mono">[SYS_EOF: 0x00FF]</text>
  <text x="{width-14}" y="16" fill="{acc}" font-size="11" font-weight="bold" text-anchor="end" class="font-mono">// BUS_SPEED: 64Gbps //</text>

  <!-- Left Main Status Readout -->
  <circle cx="26" cy="35" r="4.5" fill="{prim}" class="led"/>
  <circle cx="26" cy="35" r="1.5" fill="#FFFFFF"/>
  <rect x="38" y="26" width="76" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="76" y="38" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">SYS_STATUS</text>
  <text x="124" y="40" fill="{prim}" font-size="12" font-weight="bold" class="font-mono">{status_clean}</text>

  <!-- Secondary Diagnostics Sub-line -->
  <text x="24" y="61" fill="{text_dim}" font-size="11" class="font-mono">{sub_disp}</text>

  <!-- Center PCB Pulse / Mini Matrix -->
  <g transform="translate({width//2 - 35}, 30)">
    <line x1="0" y1="6" x2="70" y2="6" stroke="{border}" stroke-width="2"/>
    <line x1="0" y1="6" x2="35" y2="6" stroke="{prim}" stroke-width="2"/>
    <circle cx="0" cy="6" r="3" fill="{prim}"/>
    <circle cx="70" cy="6" r="3" fill="{prim}"/>
    <rect x="25" y="0" width="20" height="12" fill="{bg}" stroke="{prim}" stroke-width="1"/>
    <text x="35" y="9" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">EOF</text>
  </g>

  <!-- Right Return To Top Button -->
  <g transform="translate({width-195}, 22)" class="btn-hover">
    <rect x="0" y="0" width="180" height="36" fill="rgba(0, 200, 215, 0.16)" stroke="{prim}" stroke-width="1.5"/>
    <rect x="0" y="0" width="3" height="3" fill="{prim}"/>
    <rect x="177" y="0" width="3" height="3" fill="{prim}"/>
    <rect x="0" y="33" width="3" height="3" fill="{prim}"/>
    <rect x="177" y="33" width="3" height="3" fill="{prim}"/>
    <text x="90" y="21" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{clean_nav}</text>
    <text x="90" y="31" fill="{text_dim}" font-size="11" text-anchor="middle" class="font-mono">[ CLICK TO RETURN ]</text>
  </g>

  <!-- Bottom Grounding Notch -->
  <line x1="20" y1="{height-3}" x2="{width-20}" y2="{height-3}" stroke="{prim}" stroke-width="1" opacity="0.4"/>
  <polygon points="{width//2 - 25} {height-3}, {width//2 + 25} {height-3}, {width//2 + 18} {height-1}, {width//2 - 18} {height-1}" fill="{prim}"/>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 3. CALLOUTS & QUOTE HEADERS
# ---------------------------------------------------------------------------

def generate_callout(style="cyberpunk", primary=None, accent=None,
                     callout_type="note", title="SYSTEM SPECIFICATION",
                     subtitle="Dual-theme contrast > 7:1 // Monospace typography",
                     is_quote=False, width=850, height=None, mode="auto", preset=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    title_clean = escape_xml(title)
    sub_raw = str(subtitle).strip() if subtitle else ""
    tag_clean = escape_xml(callout_type.upper())
    st = style.lower()
    has_sub = bool(sub_raw)

    sub_lines = []
    if has_sub:
        if len(sub_raw) > 105 and " " in sub_raw:
            words = sub_raw.split()
            l1, l2 = [], []
            c_len = 0
            for w in words:
                if c_len + len(w) + 1 <= 100 or not l1:
                    l1.append(w)
                    c_len += len(w) + 1
                else:
                    l2.append(w)
            sub_lines = [" ".join(l1), " ".join(l2)]
        else:
            sub_lines = [sub_raw]

    if is_quote:
        # Quote Header Callout (Open Left Edge + Dashed Bottom)
        def_h = 56 if len(sub_lines) > 1 else 42
        h = height if height else def_h
        if st == "tactical":
            dash_w = "8,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-12}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-12}" y1="2" x2="{width-1}" y2="13" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="13" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/>'
            badge = f'<polygon points="6 6, 12 6, 4 18, 0 18" fill="{prim}" opacity="0.6"/><polygon points="16 6, 22 6, 14 18, 8 18" fill="{prim}" opacity="0.6"/><polygon points="28 8, 165 8, 172 15, 172 27, 165 34, 28 34" fill="{panel}" stroke="{prim}" stroke-width="1.5"/><text x="96" y="24" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} // HAZARD</text>'
            text_x = 186
            arrow_poly = f'<polygon points="{width-10} {h-5}, {width-2} {h-5}, {width-6} {h-1}" fill="{prim}"/>'
        elif st == "minimal":
            dash_w = "5,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="1.5"/><path d="M {width-1} 2 L {width-1} 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-4}" y="2" width="4" height="4" fill="{acc}"/>'
            badge = f'<rect x="8" y="8" width="115" height="24" fill="{panel}" stroke="{prim}" stroke-width="1"/><text x="65" y="23" fill="{prim}" font-size="9.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // MINIMAL</text>'
            text_x = 136
            arrow_poly = ""
        else:
            dash_w = "6,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="2" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/><rect x="{width-6}" y="2" width="5" height="5" fill="{prim}"/>'
            badge = f'<rect x="8" y="8" width="120" height="24" fill="{panel}" stroke="{prim}" stroke-width="1.5"/><circle cx="20" cy="20" r="3.5" fill="{prim}"/><text x="73" y="24" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // 0x01</text>'
            text_x = 142
            arrow_poly = ""

        if not has_sub:
            text_block = f'<text x="{text_x}" y="25" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>'
        elif len(sub_lines) == 1:
            text_block = f"""<text x="{text_x}" y="20" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
  <text x="{text_x}" y="33" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>"""
        else:
            text_block = f"""<text x="{text_x}" y="19" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
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
  <line x1="0" y1="{h-1}" x2="{width-5}" y2="{h-1}" stroke="{prim}" stroke-width="1.5" stroke-dasharray="{dash_w}" opacity="0.75"/>
  {arrow_poly}
</svg>"""

    else:
        # Autonomous Closed Callout (48px or 62px)
        def_h = 62 if len(sub_lines) > 1 else 48
        h = height if height else def_h
        mid_y = h // 2
        if st == "tactical":
            body = f'<polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>'
            badge = f'<polygon points="34 10, 175 10, 182 17, 182 31, 175 38, 34 38" fill="{panel}" stroke="{prim}" stroke-width="1.5"/><text x="105" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} // HAZARD</text>'
            accents = f'<polygon points="10 8, 16 8, 8 20, 2 20" fill="{prim}" opacity="0.6"/><polygon points="20 8, 26 8, 18 20, 12 20" fill="{prim}" opacity="0.6"/><circle cx="{width-25}" cy="{mid_y}" r="8" fill="none" stroke="{prim}" stroke-width="1.5"/><polygon points="{width-28} {mid_y}, {width-22} {mid_y-4}, {width-22} {mid_y+4}" fill="{prim}"/>'
            text_x = 196
        elif st == "minimal":
            body = f'<rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
            badge = f'<rect x="16" y="11" width="130" height="26" fill="{panel}" stroke="{prim}" stroke-width="1"/><text x="81" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // MINIMAL</text>'
            accents = f'<path d="M 5 12 L 5 5 L 14 5" fill="none" stroke="{prim}" stroke-width="1.5"/><path d="M {width-5} 12 L {width-5} 5 L {width-14} 5" fill="none" stroke="{prim}" stroke-width="1.5"/>'
            text_x = 158
        else:
            body = f'<rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{prim}" stroke-width="1.5"/><rect x="2" y="2" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="2" width="5" height="5" fill="{prim}"/><rect x="2" y="{h-7}" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="{h-7}" width="5" height="5" fill="{prim}"/>'
            badge = f'<rect x="14" y="10" width="140" height="28" fill="{panel}" stroke="{prim}" stroke-width="1.5"/><circle cx="26" cy="24" r="3.5" fill="{prim}"/><text x="88" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // 0x01</text>'
            accents = f'<rect x="{width-35}" y="{mid_y - 10}" width="20" height="20" fill="{panel}"/><text x="{width-25}" y="{mid_y + 4}" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">ℹ</text>'
            text_x = 168

        if not has_sub:
            text_block = f'<text x="{text_x}" y="28" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>'
        elif len(sub_lines) == 1:
            text_block = f"""<text x="{text_x}" y="22" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
  <text x="{text_x}" y="36" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>"""
        else:
            text_block = f"""<text x="{text_x}" y="20" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
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


# ---------------------------------------------------------------------------
# 4. WINDOW FRAMES (TOP & BOTTOM)
# ---------------------------------------------------------------------------

def format_tag(tag):
    t = str(tag).strip()
    if t.startswith("[") and t.endswith("]"):
        return escape_xml(t)
    return f"[{escape_xml(t)}]"

def format_bottom_tag(tag):
    t = str(tag).strip()
    if t.startswith("╚═") and t.endswith("═╝"):
        return escape_xml(t)
    inner = t
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1].strip()
    return f"╚═ [{escape_xml(inner)}] ═╝"

def generate_frame(style="cyberpunk", primary=None, accent=None,
                   frame_type="top", title="╔═ SYSTEM.CORE // RUNTIME.SYS",
                   tag="[OPEN_HUD]", width=850, height=None, mode="auto", preset=None,
                   tag_url=None, close_url=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    title_clean = escape_xml(title)
    tag_clean = format_tag(tag)
    bot_tag_clean = format_bottom_tag(tag)
    st = style.lower()
    is_top = (frame_type.lower() == "top")

    if is_top:
        h = height if height else 38
        tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" class="btn-hover">' if tag_url else ''
        tag_link_close = '</a>' if tag_url else ''
        close_link_open = f'<a href="{escape_xml(close_url)}" target="_blank" class="btn-hover">' if close_url else ''
        close_link_close = '</a>' if close_url else ''

        if st == "tactical":
            # Tactical Chamfer Top: Dual Hull, Tech Seam, Flush Downward Prongs x=1..849, LED, Buttons
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>

  <!-- DUAL TACTICAL CHASSIS -->
  <polygon points="12 4, {width-12} 4, {width-1} 15, {width-1} 32, 1 32, 1 15"
           fill="{bg}" stroke="{border}" stroke-width="2"/>
  <polygon points="14 7, {width-14} 7, {width-4} 16, {width-4} 29, 4 29, 4 16"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <line x1="20" y1="32" x2="{width-20}" y2="32" stroke="{prim}" stroke-width="1" stroke-dasharray="6,4" opacity="0.6"/>

  <!-- DOWNWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="26" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="32" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="26" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="32" width="4" height="6" fill="{prim}"/>

  <!-- Status LED -->
  <circle cx="24" cy="18" r="4" fill="{prim}" class="led"/>

  <!-- Title Text -->
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">
    {title_clean}
  </text>

  <!-- Right Status Tag -->
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-127}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>{tag_link_close}

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/>
  <text x="{width-64}" y="21" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/>
  <text x="{width-47}" y="22" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/>
  <text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
</svg>"""

        elif st == "minimal":
            # Minimal Glass Table Monolith Top (Hugging Ticks ┌ ┐)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>
  <path d="M 4 14 L 4 4 L 14 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 14 L {width-4} 4 L {width-14} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <line x1="8" y1="{h-2}" x2="{width-8}" y2="{h-2}" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <circle cx="24" cy="18" r="4" fill="{prim}"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_clean}</text>
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>{tag_link_close}
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-64}" y="21" fill="{text_dim}" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-47}" y="22" fill="{text_dim}" font-size="10" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/><text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" class="font-mono">×</text>{close_link_close}
</svg>"""

        else:
            # Cyberpunk Brackets Top (Downward prongs on x=1 and x=849)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="4" width="{width-2}" height="28" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="3" y="6" width="{width-6}" height="24" fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <rect x="1" y="4" width="5" height="5" fill="{prim}"/>
  <rect x="{width-6}" y="4" width="5" height="5" fill="{prim}"/>
  <!-- Downward Embracing Prongs (Flush x=1 and x={width-1}) -->
  <line x1="1" y1="24" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="32" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="24" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="32" width="4" height="6" fill="{prim}"/>
  <circle cx="24" cy="18" r="4" fill="{prim}" class="led"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_clean}</text>
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>{tag_link_close}
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-64}" y="21" fill="{text_dim}" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-47}" y="22" fill="{text_dim}" font-size="10" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/><text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" class="font-mono">×</text>{close_link_close}
</svg>"""

    else:
        # Bottom Frames
        h = height if height else 24
        if st == "tactical":
            # Tactical Chamfer Bottom: Upward Prongs Flush x=1..849, Chamfer Body, Center Buffer
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- UPWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="0" x2="1" y2="10" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="10" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>

  <polygon points="1 10, {width-1} 10, {width-12} 20, 12 20" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <line x1="12" y1="20" x2="{width-12}" y2="20" stroke="{prim}" stroke-width="2"/>

  <!-- Center Status Buffer Readout -->
  <rect x="{width//2 - 105}" y="4" width="210" height="16" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">
    {bot_tag_clean}
  </text>
</svg>"""

        elif st == "minimal":
            # Minimal Glass Table Monolith Bottom (Hugging Ticks └ ┘)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>
  <path d="M 4 8 L 4 18 L 14 18" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 8 L {width-4} 18 L {width-14} 18" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <line x1="8" y1="2" x2="{width-8}" y2="2" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" letter-spacing="1.5" text-anchor="middle" class="font-mono">{bot_tag_clean}</text>
</svg>"""

        else:
            # Cyberpunk Brackets Bottom (Upward prongs on x=1 and x=849)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- UPWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="0" x2="1" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="1" y1="12" x2="{width-1}" y2="12" stroke="{border}" stroke-width="3"/>
  <line x1="6" y1="12" x2="{width-6}" y2="12" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <path d="M 1 12 L 1 20 L 16 20" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="1" y="17" width="4" height="4" fill="{prim}"/>
  <path d="M {width-1} 12 L {width-1} 20 L {width-16} 20" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-5}" y="17" width="4" height="4" fill="{prim}"/>
  <rect x="{width//2 - 105}" y="4" width="210" height="16" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{bot_tag_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 5. CHIPS & PILLS
# ---------------------------------------------------------------------------

def estimate_chip_width(text, font_size=10, char_w=7.0):
    w = 0
    for char in text:
        code = ord(char)
        if code > 0x2000 or char in "⚡●▲■◆★🏛️🧬":
            w += font_size * 1.35
        else:
            w += char_w
    return max(w, 20)


def generate_chip(style="cyberpunk", primary=None, accent=None,
                  chip_type="closed", text="CHIP_LABEL", width=None, height=26, mode="auto", preset=None,
                  decay_dir="right"):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    text_clean = escape_xml(text)
    st = style.lower()
    ct = chip_type.lower()
    dd = (decay_dir or "right").lower()
    text_w = estimate_chip_width(text)

    if st == "tactical":
        if ct == "decay":
            if dd == "both":
                slash_zone = 26
                left_pad = slash_zone + 10
                right_pad = 10
                box_l = slash_zone + 2
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + slash_zone + 2
                w = width if width is not None else calc_w
                text_x = int(w / 2)
                l1_t, l1_b = 2, 2
                l2_t, l2_b = l1_t + 6, l1_b + 6
                l3_t, l3_b = l2_t + 6, l2_b + 6
                l4_t, l4_b = l3_t + 6, l3_b + 6
                r1_t, r1_b = box_r + 4, box_r + 4
                r2_t, r2_b = r1_t + 6, r1_b + 6
                r3_t, r3_b = r2_t + 6, r2_b + 6
                r4_t, r4_b = r3_t + 6, r3_b + 6
                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="{box_l+5} 1, {box_r-5} 1, {box_r} 6, {box_r} 20, {box_r-5} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{bg}"/>
  <polygon points="{box_l+5} 1, {box_r-5} 1, {box_r} 6, {box_r} 20, {box_r-5} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{l1_t+3} 9, {l1_t+5} 9, {l1_b+3} 17, {l1_b+1} 17" fill="{prim}" opacity="0.2"/>
  <polygon points="{l2_t+2.5} 6, {l2_t+5} 6, {l2_b+2.5} 20, {l2_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{l3_t+3} 3, {l3_t+6} 3, {l3_b+3} 23, {l3_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{l4_t} 1, {l4_t+3.5} 1, {l4_b+3.5} 25, {l4_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{r1_t} 1, {r1_t+3.5} 1, {r1_b+3.5} 25, {r1_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{r2_t} 3, {r2_t+3} 3, {r2_b+3} 23, {r2_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{r3_t} 6, {r3_t+2.5} 6, {r3_b+2.5} 20, {r3_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{r4_t} 9, {r4_t+2} 9, {r4_b+2} 17, {r4_b} 17" fill="{prim}" opacity="0.2"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                slash_zone = 26
                left_pad = slash_zone + 14
                right_pad = 16
                box_l = slash_zone + 2
                calc_w = int(left_pad + text_w + right_pad)
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                l1_t, l1_b = 2, 2
                l2_t, l2_b = l1_t + 6, l1_b + 6
                l3_t, l3_b = l2_t + 6, l2_b + 6
                l4_t, l4_b = l3_t + 6, l3_b + 6
                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="{box_l+5} 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{bg}"/>
  <polygon points="{box_l+5} 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{l1_t+3} 9, {l1_t+5} 9, {l1_b+3} 17, {l1_b+1} 17" fill="{prim}" opacity="0.2"/>
  <polygon points="{l2_t+2.5} 6, {l2_t+5} 6, {l2_b+2.5} 20, {l2_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{l3_t+3} 3, {l3_t+6} 3, {l3_b+3} 23, {l3_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{l4_t} 1, {l4_t+3.5} 1, {l4_b+3.5} 25, {l4_b} 25" fill="{prim}" opacity="0.9"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            else:
                # Tactical Hazard Slash Decay Right (default)
                left_pad = 22  # Chamfer (7px) + arrow (8..13px) + padding
                right_pad = 14 # Padding before 45° slant
                box_bot_r = int(left_pad + text_w + right_pad)
                box_top_r = box_bot_r + 14
                s1_t, s1_b = box_top_r + 5, box_bot_r + 5
                s2_t, s2_b = s1_t + 9, s1_b + 9
                s3_t, s3_b = s2_t + 8, s2_b + 8
                s4_t, s4_b = s3_t + 8, s3_b + 8
                calc_w = s4_t + 6
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {box_top_r} 1, {box_bot_r} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {box_top_r} 1, {box_bot_r} 25, 7 25, 1 19, 1 7" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="8 13, 13 9, 13 17" fill="{prim}"/>
  <polygon points="{s1_t} 1, {s1_t+4} 1, {s1_b+4} 25, {s1_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{s2_t} 3, {s2_t+3.5} 3, {s2_b+3.5} 23, {s2_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{s3_t} 6, {s3_t+3} 6, {s3_b+3} 20, {s3_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{s4_t} 9, {s4_t+2} 9, {s4_b+2} 17, {s4_b} 17" fill="{prim}" opacity="0.2"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Tactical Targeting Reticle Pulse
            left_pad = 26  # Chamfer (7px) + reticle (cx=14, r=4.5) + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes targetPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      .laser {{ animation: targetPulse 1.2s infinite ease-in-out; }}
    </style>
  </defs>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="14" cy="13" r="4.5" fill="none" stroke="{prim}" stroke-width="1"/>
  <circle cx="14" cy="13" r="2.5" fill="{prim}" class="laser"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Tactical Closed 45° Chamfer
            left_pad = 24  # Chamfer + arrow (10..15) + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)
            mid_x = int(w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{mid_x-2} 1, {mid_x+2} 1, {mid_x} 4" fill="{prim}"/>
  <polygon points="{mid_x-2} 25, {mid_x+2} 25, {mid_x} 22" fill="{prim}"/>
  <polygon points="10 13, 15 9, 15 17" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    elif st == "minimal":
        if ct == "decay":
            # Minimal Glass Micro-Stipple Dissolution
            left_pad = 16  # Corner bracket (4..8) + padding
            right_pad = 14
            box_r = int(left_pad + text_w + right_pad)
            dash_end = box_r + 16
            c1, c2, c3, c4 = box_r + 7, box_r + 14, box_r + 21, box_r + 28
            calc_w = box_r + 34
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{box_r}" y1="1" x2="{dash_end}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{box_r}" y1="25" x2="{dash_end}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <g fill="{prim}">
    <circle cx="{c1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{c1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{c1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{c1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{c2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{c2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{c2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{c3}" cy="10" r="1" opacity="0.35"/><circle cx="{c3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{c4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{c4}" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Minimal Glass Breathing Beacon
            left_pad = 26  # Beacon cx=15, r=3 + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes breatheBeacon {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.25; }} }}
      .breathe {{ animation: breatheBeacon 2s infinite ease-in-out; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 8 L {w-4} 4 L {w-8} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 18 L {w-4} 22 L {w-8} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="15" cy="13" r="3" fill="{prim}" class="breathe"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Minimal Glass Closed Hairline
            left_pad = 24  # Dot cx=15 + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 8 L {w-4} 4 L {w-8} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 18 L {w-4} 22 L {w-8} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="15" cy="13" r="2" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    else:
        # Cyberpunk Chips
        if ct == "decay":
            # Pixel Matrix Dither Decay
            left_pad = 18  # Corner pixels + vertical bar (7..10) + padding
            right_pad = 14
            box_r = int(left_pad + text_w + right_pad)
            d1, d2, d3, d4, d5 = box_r + 2, box_r + 8, box_r + 14, box_r + 20, box_r + 24
            calc_w = box_r + 28
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="22" width="3" height="3" fill="{prim}"/>
  <rect x="7" y="8" width="3" height="10" fill="{prim}"/>
  <g fill="{prim}">
    <rect x="{d1}" y="3" width="3" height="3"/><rect x="{d1}" y="9" width="3" height="3"/><rect x="{d1}" y="15" width="3" height="3"/><rect x="{d1}" y="20" width="3" height="3"/>
    <rect x="{d2}" y="5" width="2" height="2"/><rect x="{d2}" y="12" width="2" height="2"/><rect x="{d2}" y="18" width="2" height="2"/>
    <rect x="{d3}" y="7" width="2" height="2" opacity="0.7"/><rect x="{d3}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{d4}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{d5}" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Cyberpunk Blinking Square LED Beacon
            left_pad = 25  # LED cx=14, r=3.5 + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.4s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <circle cx="14" cy="13" r="3.5" fill="{prim}" class="led"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Cyberpunk Closed Corner Pixels
            left_pad = 22  # Corner pixels + bar (8..12) + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="8" y="8" width="4" height="10" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 6. DIVIDERS & SPLITTERS
# ---------------------------------------------------------------------------

def generate_divider(style="cyberpunk", primary=None, accent=None, width=850, height=28, mode="auto", preset=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    st = style.lower()

    if st == "tactical":
        # Pulsing Aiming Laser Divider
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
      @keyframes laserPulse {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.35; }} }}
      .laser {{ animation: laserPulse 1.4s infinite ease-in-out; }}
    </style>
  </defs>
  <line x1="20" y1="14" x2="350" y2="14" stroke="{prim}" stroke-width="1.5"/>
  <line x1="500" y1="14" x2="{width-20}" y2="14" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="12 14, 20 8, 20 20" fill="{prim}"/>
  <polygon points="{width-12} 14, {width-20} 8, {width-20} 20" fill="{prim}"/>
  <polygon points="360 4, 490 4, 498 14, 490 24, 360 24, 352 14" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <text x="425" y="17" fill="{prim}" text-anchor="middle" class="font-mono laser">▲ TACTICAL // LASER ▲</text>
</svg>"""

    elif st == "minimal":
        # Frequency Spectrum Equalizer Divider
        bars = []
        for i in range(15):
            bx = 365 + i * 8
            bh = 6 + (i * 7 % 18)
            by = 14 - bh // 2
            col = prim if i % 2 == 0 else acc
            bars.append(f'<rect x="{bx}" y="{by}" width="4" height="{bh}" fill="{col}" class="s-bar"/>')
        bars_markup = "".join(bars)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 8px; font-weight: bold; letter-spacing: 1px; }}
      @keyframes barPulse {{ 0%, 100% {{ transform: scaleY(0.4); opacity: 0.5; }} 50% {{ transform: scaleY(1.2); opacity: 1; }} }}
      .s-bar {{ transform-origin: center; animation: barPulse 1.6s infinite ease-in-out; }}
    </style>
  </defs>
  <line x1="20" y1="14" x2="345" y2="14" stroke="{border}" stroke-width="1.5"/>
  <line x1="505" y1="14" x2="{width-20}" y2="14" stroke="{border}" stroke-width="1.5"/>
  <line x1="60" y1="14" x2="330" y2="14" stroke="{prim}" stroke-width="1" opacity="0.6" stroke-dasharray="12,4"/>
  <line x1="520" y1="14" x2="{width-60}" y2="14" stroke="{prim}" stroke-width="1" opacity="0.6" stroke-dasharray="12,4"/>
  <path d="M 20 8 L 20 14 L 32 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="20" y="12" width="4" height="4" fill="{acc}"/>
  <path d="M {width-20} 8 L {width-20} 14 L {width-32} 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-24}" y="12" width="4" height="4" fill="{acc}"/>
  <text x="240" y="11" fill="{prim}" text-anchor="middle" opacity="0.7" class="font-mono">// 44.1 kHz //</text>
  <text x="610" y="11" fill="{prim}" text-anchor="middle" opacity="0.7" class="font-mono">// SPECTRUM_HUD //</text>
  <rect x="355" y="2" width="140" height="24" fill="{bg}" stroke="{border}" stroke-width="1"/>
  {bars_markup}
</svg>"""

    else:
        # Cyberpunk PCB Trace Flow Divider
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; letter-spacing: 1px; }}
      @keyframes pcbTrace {{ 0% {{ stroke-dashoffset: 400; }} 100% {{ stroke-dashoffset: 0; }} }}
      .packet {{ stroke-dasharray: 40, 200; animation: pcbTrace 2.8s infinite linear; }}
    </style>
  </defs>
  <line x1="10" y1="14" x2="{width-10}" y2="14" stroke="{border}" stroke-width="2"/>
  <line x1="10" y1="14" x2="{width-10}" y2="14" stroke="{prim}" stroke-width="2" class="packet"/>
  <circle cx="20" cy="14" r="4" fill="{prim}"/><circle cx="{width-20}" cy="14" r="4" fill="{prim}"/>
  <rect x="{width//2 - 90}" y="4" width="180" height="20" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <text x="{width//2}" y="17" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">[PCB: DATA_PACKET_FLOW]</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_splitter(style="cyberpunk", primary=None, accent=None,
                      label="[MODULE: SUB_SYSTEM]", width=850, height=22, mode="auto", preset=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    lbl_clean = escape_xml(label)
    st = style.lower()

    if st == "tactical":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="330" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <line x1="520" y1="11" x2="{width-1}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="1 11, 8 7, 8 15" fill="{prim}"/>
  <polygon points="{width-1} 11, {width-8} 7, {width-8} 15" fill="{prim}"/>
  <polygon points="340 3, 510 3, 516 11, 510 19, 340 19, 334 11" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="425" y="14" fill="{prim}" text-anchor="middle" class="font-mono">▲ {lbl_clean} ▲</text>
</svg>"""

    elif st == "minimal":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="340" y2="11" stroke="{border}" stroke-width="1"/>
  <line x1="510" y1="11" x2="{width-1}" y2="11" stroke="{border}" stroke-width="1"/>
  <rect x="350" y="2" width="150" height="18" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="425" y="14" fill="{prim}" text-anchor="middle" class="font-mono">{lbl_clean}</text>
</svg>"""

    else:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="330" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <line x1="520" y1="11" x2="{width-1}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="8" width="6" height="6" fill="{prim}"/>
  <rect x="{width-7}" y="8" width="6" height="6" fill="{prim}"/>
  <rect x="340" y="2" width="170" height="18" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <text x="425" y="14" fill="{prim}" text-anchor="middle" class="font-mono">{lbl_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
# DATA VISUALIZATION WIDGETS (v4.0)
# ==============================================================================

def generate_metrics(metrics=None, cards=None, style="cyberpunk", primary=None, accent=None, mode="auto", preset=None, width=850):
    """
    Renders 1 to 4 metric KPI cards in a full-width SVG row.
    metrics / cards: list of dicts with: label, value, delta (optional), trend (optional), status (optional)
    """
    if metrics is None and cards is not None:
        metrics = cards
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    success = c["success"]
    warning = c["warning"]
    st = style.lower()

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
            status_markup = f"""<rect x="{x+card_w-68}" y="{y+10}" width="56" height="13" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{x+card_w-40}" y="{y+20}" fill="{acc}" text-anchor="middle" class="font-mono-tag">{stat_clean}</text>"""

        delta_markup = ""
        if delta:
            d_clean = escape_xml(delta)
            delta_markup = f'<text x="{x+14}" y="{y+76}" fill="{trend_col}" class="font-mono-sub">{trend_icon}{d_clean}</text>'

        # Mini sparkline decoration in bottom right of card
        sp_x = x + card_w - 54
        sp_y = y + 74
        sparkline = f"""
    <path d="M {sp_x} {sp_y+4} L {sp_x+10} {sp_y-2} L {sp_x+20} {sp_y+6} L {sp_x+30} {sp_y-6} L {sp_x+40} {sp_y}" fill="none" stroke="{prim}" stroke-width="1.2" stroke-opacity="0.4"/>
    <circle cx="{sp_x+40}" cy="{sp_y}" r="2" fill="{acc}"/>
"""

        cards_svg.append(f"""  <g id="metric-card-{i}">
    {hull}
    <text x="{x+14}" y="{y+22}" fill="{text_dim}" class="font-mono-lbl">{label}</text>
    {status_markup}
    <text x="{x+14}" y="{y+54}" fill="{title_front}" class="font-mono-val">{val}</text>
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

def generate_progress(value=50, label="SYSTEM PROGRESS", sub=None, style="cyberpunk", primary=None, accent=None, mode="auto", preset=None, width=850):
    """
    Renders a segmented sci-fi HUD progress bar with dithering and status readout.
    """
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    st = style.lower()

    try:
        val_clean = max(0, min(100, int(round(float(value)))))
    except Exception:
        val_clean = 50

    lbl_clean = escape_xml(label)
    sub_clean = escape_xml(sub if sub is not None else f"RUNTIME PROGRESS // {val_clean}% COMPLETE")

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
  <text x="14" y="19" fill="{title_front}" class="font-prog-lbl">■ {lbl_clean}</text>
  <rect x="{width-74}" y="7" width="60" height="15" fill="{panel}" stroke="{acc}" stroke-width="1"/>
  <text x="{width-44}" y="19" fill="{acc}" text-anchor="middle" class="font-prog-val">{val_clean}%</text>

  <!-- Track & Segments -->
  <rect x="{track_x-1}" y="{track_y-1}" width="{track_w+2}" height="{track_h+2}" fill="none" stroke="{border}" stroke-width="1"/>
  <g id="segments">
    {joined_segments}
  </g>

  <!-- Subtext & Milestone Ticks -->
  <text x="14" y="56" fill="{text_dim}" class="font-prog-sub">{sub_clean}</text>
  <text x="{width-14}" y="56" fill="{text_dim}" text-anchor="end" class="font-prog-sub">0% ── 50% ── 100%</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_techstack(items=None, columns=5, style="cyberpunk", primary=None, accent=None, mode="auto", preset=None, width=850):
    """
    Renders a sci-fi HUD matrix of technology cards with embedded 20x20 pixel vector icons.
    items: list of string names e.g. ["python", "cpp", "docker", "git", "linux"]
    """
    from generator.icons import get_tech_icon_svg

    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    st = style.lower()

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
            label_markup = f'<text x="{x+card_w-8}" y="{y+25}" fill="{text_dim}" text-anchor="end" class="font-tech-sub">{lbl_clean}</text>'

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
    <text x="{x+36}" y="{y+25}" fill="{text_main}" class="font-tech-name">{clean_name}</text>
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

def generate_timeline(items=None, milestones=None, style="cyberpunk", primary=None, accent=None, mode="auto", preset=None, width=850):
    """
    Renders a vertical PCB data bus timeline with milestones and status nodes.
    items / milestones: list of dicts with: title, date, status ("COMPLETED"|"IN_PROGRESS"|"PLANNED"), desc
    """
    if items is None and milestones is not None:
        items = milestones
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    success = c["success"]
    st = style.lower()

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

        milestones_svg.append(f"""  <g id="milestone-{i}">
    {conn}
    {node_shape}
    {c_hull}
    <!-- Milestone Header -->
    <rect x="{card_x+12}" y="{card_y+9}" width="60" height="14" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="{card_x+42}" y="{card_y+20}" fill="{text_dim}" text-anchor="middle" class="font-time-date">{d}</text>
    <text x="{card_x+82}" y="{card_y+20}" fill="{title_front}" class="font-time-title">{t}</text>
    <text x="{card_x+card_w-14}" y="{card_y+20}" fill="{node_col}" text-anchor="end" class="font-time-stat">{stat_lbl}</text>
    <!-- Milestone Description -->
    <text x="{card_x+14}" y="{card_y+40}" fill="{text_dim}" class="font-time-desc">{desc}</text>
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

def generate_social(style="cyberpunk", primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT RETRO HUD READMES",
                    repo="Kazinagg/pixel-readme-kit", tags="PYTHON,SVG,HUD,RETRO",
                    width=1280, height=640, mode="auto", preset=None):
    """
    Renders an OpenGraph Social Preview Card (1280x640) for GitHub repositories.
    """
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    st = style.lower()

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    repo_clean = escape_xml(repo.upper())

    # 3D Pixel Title at px_size=7 (or 6 if long)
    px_size = 6 if len(title) > 14 else 7
    pixel_markup, t_w, t_h = render_3d_text(
        title, x=80, y=170, px_size=px_size,
        front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
        spacing=2, max_width=750, allow_wrap=True
    )

    y_sub = 170 + t_h + 24
    sub_w = min(720, max(320, int(len(subtitle) * 11) + 48))

    # Parse technology/feature tags
    if not tags:
        tag_list = ["GITHUB", "OPEN-SOURCE", "v4.0"]
    elif isinstance(tags, str):
        tag_list = [t.strip().upper() for t in tags.split(",") if t.strip()]
    else:
        tag_list = [str(t).strip().upper() for t in tags if t]
    tag_chips = []
    curr_x = 80
    for t_item in tag_list[:5]:
        tw = int(len(t_item) * 9.5) + 28
        tag_chips.append(f"""
    <g transform="translate({curr_x}, 530)">
      <rect x="0" y="0" width="{tw}" height="34" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
      <rect x="0" y="0" width="4" height="34" fill="{prim}"/>
      <text x="{tw//2 + 2}" y="22" fill="{acc}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">{escape_xml(t_item)}</text>
    </g>
""")
        curr_x += tw + 16
    chips_markup = "".join(tag_chips)

    # Chassis styling
    if st == "tactical":
        chassis = f"""
  <polygon points="24 6, {width-24} 6, {width-6} 24, {width-6} {height-24}, {width-24} {height-6}, 24 {height-6}, 6 {height-24}, 6 24"
           fill="{bg}" stroke="{border}" stroke-width="2.5"/>
  <polygon points="32 14, {width-32} 14, {width-14} 32, {width-14} {height-32}, {width-32} {height-14}, 32 {height-14}, 14 {height-32}, 14 32"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.6"/>
  <!-- Corner Hazard Chevrons -->
  <polygon points="40 18, 54 18, 36 36, 22 36" fill="{prim}"/>
  <polygon points="62 18, 76 18, 58 36, 44 36" fill="{prim}"/>
"""
        reticle = f"""
  <g transform="translate(1020, 320)">
    <circle cx="0" cy="0" r="140" fill="none" stroke="{border}" stroke-width="2"/>
    <circle cx="0" cy="0" r="90" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="6 4"/>
    <circle cx="0" cy="0" r="40" fill="{panel}" stroke="{acc}" stroke-width="1.5"/>
    <line x1="-160" y1="0" x2="160" y2="0" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8 4"/>
    <line x1="0" y1="-160" x2="0" y2="160" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8 4"/>
    <text x="0" y="5" fill="{prim}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">LOCK-ON</text>
  </g>
"""
    elif st == "minimal":
        chassis = f"""
  <rect x="8" y="8" width="{width-16}" height="{height-16}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <line x1="8" y1="8" x2="{width-8}" y2="8" stroke="{prim}" stroke-width="4"/>
  <rect x="14" y="14" width="8" height="8" fill="{prim}"/>
  <rect x="{width-22}" y="14" width="8" height="8" fill="{acc}"/>
  <rect x="14" y="{height-22}" width="8" height="8" fill="{acc}"/>
  <rect x="{width-22}" y="{height-22}" width="8" height="8" fill="{prim}"/>
"""
        reticle = f"""
  <g transform="translate(1020, 320)">
    <rect x="-110" y="-110" width="220" height="220" fill="none" stroke="{border}" stroke-width="1.5"/>
    <rect x="-80" y="-80" width="160" height="160" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="-110" y1="0" x2="110" y2="0" stroke="{acc}" stroke-width="2"/>
    <line x1="0" y1="-110" x2="0" y2="110" stroke="{acc}" stroke-width="2"/>
    <circle cx="0" cy="0" r="6" fill="{prim}"/>
  </g>
"""
    else:  # cyberpunk
        chassis = f"""
  <rect x="8" y="8" width="{width-16}" height="{height-16}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="8" y="8" width="16" height="16" fill="{prim}"/>
  <rect x="{width-24}" y="8" width="16" height="16" fill="{acc}"/>
  <rect x="8" y="{height-24}" width="16" height="16" fill="{acc}"/>
  <rect x="{width-24}" y="{height-24}" width="16" height="16" fill="{prim}"/>
  <line x1="8" y1="48" x2="24" y2="48" stroke="{prim}" stroke-width="2"/>
  <line x1="{width-24}" y1="{height-48}" x2="{width-8}" y2="{height-48}" stroke="{acc}" stroke-width="2"/>
"""
        reticle = f"""
  <g transform="translate(1020, 320)">
    <circle cx="0" cy="0" r="140" fill="none" stroke="{border}" stroke-width="2"/>
    <circle cx="0" cy="0" r="100" fill="none" stroke="{prim}" stroke-width="2" stroke-dasharray="10 6"/>
    <circle cx="0" cy="0" r="60" fill="{panel}" stroke="{acc}" stroke-width="2"/>
    <line x1="-150" y1="0" x2="150" y2="0" stroke="{prim}" stroke-width="1.5"/>
    <line x1="0" y1="-150" x2="0" y2="150" stroke="{prim}" stroke-width="1.5"/>
    <circle cx="45" cy="-45" r="5" fill="{prim}"/>
    <circle cx="-55" cy="35" r="4" fill="{acc}"/>
  </g>
"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>

  {chassis}

  <!-- TOP REPOSITORY HEADER -->
  <rect x="80" y="56" width="380" height="34" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
  <text x="96" y="78" fill="{prim}" font-size="13" font-weight="bold" letter-spacing="1px" class="font-mono">■ REPOSITORY // {repo_clean}</text>
  <rect x="470" y="56" width="140" height="34" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
  <text x="540" y="78" fill="{acc}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">PUBLIC // v4.0</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE CALLOUT -->
  <rect x="80" y="{y_sub}" width="{sub_w}" height="42" fill="{panel}" stroke="{acc}" stroke-width="1.5"/>
  <text x="100" y="{y_sub + 27}" fill="{text_main}" font-size="15" font-weight="bold" class="font-mono">▶ {sub_clean}</text>

  <!-- TECH / FEATURE TAGS ROW -->
  {chips_markup}

  <!-- RIGHT SIDE RETICLE -->
  {reticle}

  <!-- WATERMARK -->
  <text x="{width-80}" y="{height-40}" fill="{text_dim}" font-size="12" font-weight="bold" text-anchor="end" class="font-mono">PIXEL-README-KIT // 1280x640 OPENGRAPH</text>
</svg>"""

    validate_svg(svg)
    return svg

