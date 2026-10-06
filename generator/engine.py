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
from generator.font_engine import render_3d_text, calculate_px_size, calculate_smart_layout

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
            "tertiary": "#FF0055",
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
            "tertiary": "#CF222E",
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
            "tertiary": "#EF4444",
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
            "tertiary": "#B91C1C",
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
            "tertiary": "#06B6D4",
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
            "tertiary": "#0891B2",
            "title_front": "#1D4ED8",
            "title_mid": "#1E40AF",
            "title_dark": "#0F172A",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.10"
        }
    },
    "clean-mono": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.85)",
            "panel": "rgba(30, 41, 59, 0.80)",
            "border": "rgba(51, 65, 85, 0.85)",
            "primary": "#E2E8F0",
            "accent": "#94A3B8",
            "tertiary": "#CBD5E1",
            "title_front": "#F8FAFC",
            "title_mid": "#CBD5E1",
            "title_dark": "#64748B",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FFFFFF",
            "panel": "#F1F5F9",
            "border": "#CBD5E1",
            "primary": "#0F172A",
            "accent": "#475569",
            "tertiary": "#64748B",
            "title_front": "#0F172A",
            "title_mid": "#334155",
            "title_dark": "#64748B",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "corporate-blue": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.88)",
            "panel": "rgba(30, 41, 59, 0.82)",
            "border": "rgba(30, 58, 138, 0.85)",
            "primary": "#38BDF8",
            "accent": "#818CF8",
            "tertiary": "#0284C7",
            "title_front": "#38BDF8",
            "title_mid": "#0284C7",
            "title_dark": "#0369A1",
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#22C55E",
            "warning": "#EAB308",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F0F9FF",
            "panel": "#E0F2FE",
            "border": "#BAE6FD",
            "primary": "#0284C7",
            "accent": "#4F46E5",
            "tertiary": "#0369A1",
            "title_front": "#0369A1",
            "title_mid": "#075985",
            "title_dark": "#0C4A6E",
            "text_main": "#0C4A6E",
            "text_dim": "#0369A1",
            "success": "#16A34A",
            "warning": "#CA8A04",
            "grid_op": "0.08"
        }
    },
    "academic-paper": {
        "dark": {
            "bg": "rgba(24, 24, 27, 0.88)",
            "panel": "rgba(39, 39, 42, 0.82)",
            "border": "rgba(63, 63, 70, 0.85)",
            "primary": "#60A5FA",
            "accent": "#F59E0B",
            "tertiary": "#38BDF8",
            "title_front": "#93C5FD",
            "title_mid": "#3B82F6",
            "title_dark": "#1D4ED8",
            "text_main": "#F4F4F5",
            "text_dim": "#A1A1AA",
            "success": "#10B981",
            "warning": "#D97706",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FAFAF9",
            "panel": "#F5F5F4",
            "border": "#E7E5E4",
            "primary": "#1C1917",
            "accent": "#B45309",
            "tertiary": "#2563EB",
            "title_front": "#1C1917",
            "title_mid": "#44403C",
            "title_dark": "#78716C",
            "text_main": "#1C1917",
            "text_dim": "#78716C",
            "success": "#15803D",
            "warning": "#B45309",
            "grid_op": "0.06"
        }
    },
    "modern-slate": {
        "dark": {
            "bg": "rgba(15, 23, 30, 0.88)",
            "panel": "rgba(22, 33, 46, 0.82)",
            "border": "rgba(30, 41, 59, 0.85)",
            "primary": "#2DD4BF",
            "accent": "#A78BFA",
            "tertiary": "#F43F5E",
            "title_front": "#2DD4BF",
            "title_mid": "#0D9488",
            "title_dark": "#115E59",
            "text_main": "#F1F5F9",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#0F766E",
            "accent": "#6D28D9",
            "tertiary": "#BE123C",
            "title_front": "#0F766E",
            "title_mid": "#115E59",
            "title_dark": "#134E4A",
            "text_main": "#0F172A",
            "text_dim": "#475569",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    }
}

THEME_PALETTES["clean_mono"] = THEME_PALETTES["clean-mono"]
THEME_PALETTES["corporate_blue"] = THEME_PALETTES["corporate-blue"]
THEME_PALETTES["academic_paper"] = THEME_PALETTES["academic-paper"]
THEME_PALETTES["modern_slate"] = THEME_PALETTES["modern-slate"]

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

def measure_mono_text_width(text, font_size=11):
    """
    Estimates the pixel width of text rendered with monospace font (JetBrains Mono, Fira Code, etc.).
    Standard monospace character pitch is approx 0.60 to 0.62 * font_size.
    Wide/Unicode symbols (such as arrows, stars, blocks) are approx 1.1 to 1.35 * font_size.
    """
    if not text:
        return 0.0
    w = 0.0
    char_pitch = font_size * 0.61
    for ch in str(text):
        code = ord(ch)
        if code > 0x2000 or ch in "★⚡●▲▼■◆▶◀ℹ✓✗🏛️🧬":
            w += font_size * 1.25
        else:
            w += char_pitch
    return w

def clamp_text_to_width(text, max_width, font_size=11, suffix="..."):
    """
    Clamps/truncates text with a suffix if its rendered width exceeds max_width.
    """
    if not text:
        return ""
    text_str = str(text)
    if measure_mono_text_width(text_str, font_size) <= max_width:
        return text_str

    suffix_w = measure_mono_text_width(suffix, font_size)
    target_w = max(0, max_width - suffix_w)

    clamped = text_str
    while clamped and measure_mono_text_width(clamped, font_size) > target_w:
        clamped = clamped[:-1]

    return (clamped.rstrip() + suffix) if clamped else text_str[:1]

def wrap_text_to_lines(text, max_width, font_size=11, max_lines=2, suffix="..."):
    """
    Splits text across lines based on word boundaries, respecting max_width and max_lines.
    The final line is truncated with suffix if there is remaining overflow.
    """
    if not text:
        return []
    words = str(text).strip().split()
    if not words:
        return []

    lines = []
    curr_line = []

    for i, w in enumerate(words):
        test_line = " ".join(curr_line + [w])
        if measure_mono_text_width(test_line, font_size) <= max_width or not curr_line:
            curr_line.append(w)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [w]
            if len(lines) == max_lines - 1:
                # Last allowed line, accumulate rest
                remaining_words = words[i:]
                last_line = " ".join(remaining_words)
                lines.append(clamp_text_to_width(last_line, max_width, font_size, suffix=suffix))
                curr_line = []
                break

    if curr_line and len(lines) < max_lines:
        line_str = " ".join(curr_line)
        if measure_mono_text_width(line_str, font_size) > max_width:
            line_str = clamp_text_to_width(line_str, max_width, font_size, suffix=suffix)
        lines.append(line_str)
    elif curr_line and lines:
        lines[-1] = clamp_text_to_width(lines[-1] + " " + " ".join(curr_line), max_width, font_size, suffix=suffix)

    return lines

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

def resolve_theme(style, mode="auto", primary=None, accent=None, preset=None, tertiary=None):
    st = style.lower() if style else "cyberpunk"
    pal = THEME_PALETTES.get(st, THEME_PALETTES["cyberpunk"])
    dark_vals = dict(pal["dark"])
    light_vals = dict(pal["light"])

    if preset:
        preset_data = load_preset(preset)
        if preset_data:
            p_prim = preset_data.get("primary")
            p_acc = preset_data.get("accent") or preset_data.get("secondary")
            p_tert = preset_data.get("tertiary") or (preset_data.get("accent") if preset_data.get("secondary") else None)
            p_succ = preset_data.get("success")
            p_warn = preset_data.get("warning")
            p_bg = preset_data.get("bg_glass") or preset_data.get("bg")
            p_panel = preset_data.get("bg_panel") or preset_data.get("panel")
            p_border = preset_data.get("border_subtle") or preset_data.get("border_slate") or preset_data.get("border")

            if p_prim and not primary:
                primary = p_prim
            if p_acc and not accent:
                accent = p_acc
            if p_tert and not tertiary:
                tertiary = p_tert
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

    if tertiary:
        dark_vals["tertiary"] = tertiary
        light_vals["tertiary"] = darken_hex(tertiary, 0.7) if is_light_color(tertiary) else tertiary

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
            "tertiary": "var(--tertiary)",
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
        --tertiary: {light_vals['tertiary']};
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
          --tertiary: {dark_vals['tertiary']};
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

def resolve_colors(style, primary=None, accent=None, mode="auto", preset=None, tertiary=None):
    c, _ = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
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
                             tag_url=None, close_url=None, tertiary=None):
    """
    Renders a low-profile compact banner (~84px height) optimized for mobile viewports.
    """
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
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

    tag_w = min(200, max(120, int(measure_mono_text_width(tag_clean, 11) + 24)))
    tag_x = width - tag_w - 24
    status_widget = f"""  <rect x="{tag_x}" y="24" width="{tag_w}" height="32" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
  <text x="{tag_x + tag_w//2}" y="44" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>"""

    avail_sub_w = max(60, tag_x - 46)
    sub_disp = clamp_text_to_width(f"■ {sub_clean}", avail_sub_w, 11)

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
  <text x="34" y="{y_sub + 12}" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">{sub_disp}</text>
{status_widget}
</svg>"""

    validate_svg(svg)
    return svg

def generate_header(style="cyberpunk", primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                    specs=None, spec1=None, spec2=None, spec3=None,
                    tag="SYSTEM_ACTIVE", width=850, height=None, mode="auto", preset=None,
                    tag_url=None, close_url=None, compact=False, tertiary=None):
    if compact and str(compact).lower() in ("true", "1", "yes", "compact"):
        return _generate_compact_header(
            style=style, primary=primary, accent=accent, title=title, subtitle=subtitle,
            tag=tag, width=width, height=height, mode=mode, preset=preset,
            tag_url=tag_url, close_url=close_url, tertiary=tertiary
        )

    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
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

    # Dynamic subtitle box width and safe clamp
    sub_w = min(480, max(260, int(measure_mono_text_width(subtitle, 11) + 40)))
    sub_tactical = clamp_text_to_width(f"[TARGET] {sub_clean}", sub_w - 24, 11)
    sub_minimal = clamp_text_to_width(f"⚡ {sub_clean}", sub_w - 24, 11)
    sub_cyberpunk = clamp_text_to_width(f"⚡ {sub_clean}", sub_w - 24, 11)

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
                lbl_disp = clamp_text_to_width(lbl, 140, 11)
                prefix = f"&gt; {lbl_disp}: "
                avail_val_w = max(40, 480 - int(measure_mono_text_width(prefix, 11)))
                val_disp = clamp_text_to_width(val, avail_val_w, 11)
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="11" class="font-mono">&gt; {escape_xml(lbl_disp)}: <tspan fill="{val_col}">{escape_xml(val_disp)}</tspan></text>
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
    {sub_tactical}
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
                lbl_disp = clamp_text_to_width(lbl, 140, 10)
                prefix = f"// {lbl_disp}: "
                avail_val_w = max(40, 480 - int(measure_mono_text_width(prefix, 10)))
                val_disp = clamp_text_to_width(val, avail_val_w, 10)
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="10" class="font-mono">// {escape_xml(lbl_disp)}: <tspan fill="{val_col}">{escape_xml(val_disp)}</tspan></text>
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
    <text x="12" y="15" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">{sub_minimal}</text>
  </g>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- EQUALIZER BARS (RIGHT SIDE) -->
  <g transform="translate({width-120}, {eq_y})">
    <rect x="0" y="28" width="8" height="12" fill="{prim}" class="eq1"/>
    <rect x="14" y="12" width="8" height="28" fill="{acc}" class="eq2"/>
    <rect x="28" y="22" width="8" height="18" fill="{tertiary_col}" class="eq3"/>
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
                lbl_disp = clamp_text_to_width(lbl, 130, 11)
                lbl_w = measure_mono_text_width(f"{lbl_disp}:", 11)
                val_x = max(200, int(60 + lbl_w + 12))
                avail_val_w = max(40, 480 - val_x)
                val_disp = clamp_text_to_width(val, avail_val_w, 11)
                teletype_svg.append(f"""
    <text x="42" y="{y_pos}" fill="{success}" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="{y_pos}" fill="{text_main}" font-size="11" class="font-mono">{escape_xml(lbl_disp)}:</text>
    <text x="{val_x}" y="{y_pos}" fill="{col}" font-size="11" font-weight="bold" class="font-mono">{escape_xml(val_disp)}</text>
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
    <rect x="16" y="192" width="5" height="12" fill="{tertiary_col}" class="w3"/>
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
        0%, 100% {{ fill: {success}; opacity: 1; }}
        50% {{ fill: {success}; opacity: 0.2; }}
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

  <!-- CORNER ACCENT BRACKETS (PRIMARY + SECONDARY DUAL-TONE) -->
  <rect x="6" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{acc}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{acc}"/>
  <rect x="6" y="{h-12}" width="24" height="6" fill="{acc}"/>
  <rect x="6" y="{h-30}" width="6" height="24" fill="{acc}"/>
  <rect x="{width-30}" y="{h-12}" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="{h-30}" width="6" height="24" fill="{prim}"/>

  <!-- TOP CONSOLE STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="{panel}"/>
  <line x1="14" y1="36" x2="260" y2="36" stroke="{prim}" stroke-width="1.5" opacity="0.8"/>
  <line x1="260" y1="36" x2="{width-14}" y2="36" stroke="{acc}" stroke-width="1.5" opacity="0.5"/>

  <circle cx="28" cy="25" r="4" fill="{success}" class="status-led"/>
  <text x="38" y="29" fill="{success}" font-size="11" font-weight="bold" class="font-mono">SYS: ONLINE // 0x00</text>

  <rect x="175" y="19" width="2" height="12" fill="{acc}" opacity="0.7"/>
  <text x="188" y="29" fill="{text_dim}" font-size="11" class="font-mono">HUD: ACTIVE_SYS</text>

  <rect x="360" y="19" width="2" height="12" fill="{acc}" opacity="0.7"/>
  <text x="372" y="29" fill="{text_dim}" font-size="11" class="font-mono">MODE: {st.upper()}_HUD</text>

  <!-- Tag right-anchored to never collide with window controls -->
  {f'<a href="{escape_xml(tag_url)}" target="_blank" class="btn-hover">' if tag_url else ''}<text x="{width-95}" y="29" fill="{warning}" font-size="11" font-weight="bold" text-anchor="end" class="font-mono">{tag_clean}</text>{'</a>' if tag_url else ''}

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="{border}"/>
  <text x="{width-80}" y="28" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="{border}"/>
  <text x="{width-59}" y="29" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">□</text>
  {f'<a href="{escape_xml(close_url)}" target="_blank" class="btn-hover">' if close_url else ''}<rect x="{width-41}" y="19" width="16" height="12" fill="{tertiary_col}"/><text x="{width-37}" y="29" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">×</text>{'</a>' if close_url else ''}

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
      {sub_cyberpunk}
    </text>
  </g>

  {teletype_block}

  <!-- RIGHT SIDE: RETRO SCI-FI WORKBENCH / MONITOR HUD (RADAR) -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="{panel}" stroke="{border}" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>

    <!-- Radar Corner Accent Tabs in Secondary Accent -->
    <rect x="0" y="0" width="8" height="2" fill="{acc}"/>
    <rect x="0" y="0" width="2" height="8" fill="{acc}"/>
    <rect x="162" y="0" width="8" height="2" fill="{acc}"/>
    <rect x="168" y="0" width="2" height="8" fill="{acc}"/>
    <rect x="0" y="138" width="8" height="2" fill="{acc}"/>
    <rect x="0" y="132" width="2" height="8" fill="{acc}"/>
    <rect x="162" y="138" width="8" height="2" fill="{acc}"/>
    <rect x="168" y="132" width="2" height="8" fill="{acc}"/>

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
    <circle cx="110" cy="50" r="3" fill="{tertiary_col}">
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
  <text x="24" y="{h-15}" fill="{acc}" font-size="9" class="font-mono">HUD_ARCH: V4.3 <tspan fill="{text_dim}">//</tspan> DUAL_THEME: PASS <tspan fill="{text_dim}">//</tspan> SMART_LAYOUT</text>
  <text x="{width-24}" y="{h-15}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">READY // ID: 0xDEADBEEF</text>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 2. FOOTERS (CLOSING PLATES)
# ---------------------------------------------------------------------------

def generate_footer(style="cyberpunk", primary=None, accent=None,
                    status="SESSION_ACTIVE // STANDBY", nav_text="RETURN TO TOP",
                    sub_text=None, width=850, height=76, mode="auto", preset=None, tertiary=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    status_clean = escape_xml(status)
    nav_clean = escape_xml(nav_text)
    st = style.lower()

    clean_nav = nav_clean.strip()
    clean_nav = clamp_text_to_width(clean_nav, 150, 11)
    status_tactical = clamp_text_to_width(status_clean, 240, 12)
    status_minimal = clamp_text_to_width(status_clean, 300, 11.5)
    status_cyber = clamp_text_to_width(status_clean, 250, 12)

    if st == "tactical":
        sub_default = "GRID: 34-BRAVO // CHECKSUM: 0x9AF4B // SENSORS: PASSIVE_SCAN // AUTH: VERIFIED"
        sub_disp = escape_xml(sub_text if sub_text else sub_default)
        sub_disp = clamp_text_to_width(sub_disp, width - 230, 11)
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
  <polygon points="36 8, 42 8, 34 18, 28 18" fill="{acc}" opacity="0.85"/>
  <polygon points="46 8, 52 8, 44 18, 38 18" fill="{tertiary_col}" opacity="0.85"/>
  <text x="64" y="16" fill="{acc}" font-size="11" font-weight="bold" letter-spacing="1.5" class="font-mono">SEC_DEFCON_1 // FIELD_TERMINATION_PROTOCOL</text>
  <line x1="390" y1="13" x2="{width-210}" y2="13" stroke="{prim}" stroke-width="1" stroke-dasharray="8,4" opacity="0.4"/>
  <text x="{width-200}" y="16" fill="{acc}" font-size="11" font-weight="bold" class="font-mono">[SEC_CLEAR]</text>

  <!-- Left Main Status Readout -->
  <polygon points="24 26, 116 26, 122 32, 122 42, 116 48, 24 48" fill="rgba(245, 158, 11, 0.22)" stroke="{acc}" stroke-width="1.5"/>
  <text x="70" y="40" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">▲ ARMED ▲</text>
  <text x="132" y="42" fill="{prim}" font-size="12" font-weight="bold" class="font-mono">{status_tactical}</text>

  <!-- Sub-diagnostic Telemetry -->
  <text x="24" y="63" fill="{acc}" font-size="11" class="font-mono">{sub_disp}</text>

  <!-- Center Chevron Cascade -->
  <g transform="translate({width//2 - 25}, 36)">
    <polygon points="0 0, 7 5, 0 10" fill="{prim}" opacity="0.5"/>
    <polygon points="12 0, 19 5, 12 10" fill="{acc}" opacity="0.8"/>
    <polygon points="24 0, 31 5, 24 10" fill="{prim}" opacity="1"/>
    <polygon points="36 0, 43 5, 36 10" fill="{acc}" opacity="0.8"/>
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
        sub_disp = clamp_text_to_width(sub_disp, width - 230, 11)
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
  <path d="M 6 {height-16} L 6 {height-6} L 16 {height-6}" fill="none" stroke="{acc}" stroke-width="1.5"/>
  <path d="M {width-6} {height-16} L {width-6} {height-6} L {width-16} {height-6}" fill="none" stroke="{acc}" stroke-width="1.5"/>

  <!-- Top Micro-Header Line -->
  <text x="24" y="16" fill="{text_dim}" font-size="11" class="font-mono">// TERMINAL_SESSION // KERNEL v3.0</text>
  <line x1="220" y1="13" x2="{width-220}" y2="13" stroke="{border}" stroke-width="1"/>
  <text x="{width-24}" y="16" fill="{text_dim}" font-size="11" text-anchor="end" class="font-mono">END_OF_PAGE</text>

  <!-- Main Status Row -->
  <circle cx="28" cy="38" r="4" fill="{prim}"/>
  <circle cx="28" cy="38" r="7" fill="none" stroke="{prim}" stroke-width="1" opacity="0.4"/>
  <text x="44" y="42" fill="{text_main}" font-size="11.5" font-weight="bold" class="font-mono">STATUS: <tspan fill="{prim}">{status_minimal}</tspan></text>

  <!-- Secondary Telemetry Line -->
  <text x="24" y="62" fill="{text_dim}" font-size="11" class="font-mono">{sub_disp}</text>

  <!-- Center Spectrum Waveform -->
  <g transform="translate({width//2 - 20}, 32)">
    <rect x="0" y="4" width="3" height="12" fill="{prim}" opacity="0.6"/>
    <rect x="6" y="1" width="3" height="18" fill="{acc}" opacity="0.8"/>
    <rect x="12" y="7" width="3" height="9" fill="{prim}" opacity="0.5"/>
    <rect x="18" y="0" width="3" height="20" fill="{tertiary_col}" opacity="1"/>
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
        if sub_text:
            sub_disp = escape_xml(sub_text)
            sub_disp = clamp_text_to_width(sub_disp, width - 230, 11)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
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
  <circle cx="26" cy="35" r="1.5" fill="{tertiary_col}"/>
  <rect x="38" y="26" width="76" height="18" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
  <text x="76" y="38" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">SYS_STATUS</text>
  <text x="124" y="40" fill="{prim}" font-size="12" font-weight="bold" class="font-mono">{status_cyber}</text>

  <!-- Secondary Diagnostics Sub-line -->
  <text x="24" y="61" fill="{text_dim}" font-size="11" class="font-mono">{sub_disp}</text>

  <!-- Center PCB Pulse / Mini Matrix -->
  <g transform="translate({width//2 - 35}, 30)">
    <line x1="0" y1="6" x2="70" y2="6" stroke="{border}" stroke-width="2"/>
    <line x1="0" y1="6" x2="35" y2="6" stroke="{acc}" stroke-width="2"/>
    <circle cx="0" cy="6" r="3" fill="{prim}"/>
    <circle cx="70" cy="6" r="3" fill="{acc}"/>
    <rect x="25" y="0" width="20" height="12" fill="{bg}" stroke="{prim}" stroke-width="1"/>
    <text x="35" y="9" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">EOF</text>
  </g>

  <!-- Right Return To Top Button -->
  <g transform="translate({width-195}, 22)" class="btn-hover">
    <rect x="0" y="0" width="180" height="36" fill="rgba(0, 200, 215, 0.16)" stroke="{prim}" stroke-width="1.5"/>
    <rect x="0" y="0" width="4" height="4" fill="{acc}"/>
    <rect x="176" y="0" width="4" height="4" fill="{acc}"/>
    <rect x="0" y="32" width="4" height="4" fill="{acc}"/>
    <rect x="176" y="32" width="4" height="4" fill="{acc}"/>
    <text x="90" y="21" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{clean_nav}</text>
    <text x="90" y="31" fill="{acc}" font-size="11" text-anchor="middle" class="font-mono">[ CLICK TO RETURN ]</text>
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
                   tag_url=None, close_url=None, tertiary=None):
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
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

    title_disp = clamp_text_to_width(title_clean, width - 230, 12)
    tag_disp = clamp_text_to_width(tag_clean, 95, 9)
    bot_w = max(210, min(width - 60, int(measure_mono_text_width(bot_tag_clean, 9) + 24)))
    bx = (width - bot_w) // 2

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
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>

  <!-- DUAL TACTICAL CHASSIS -->
  <polygon points="12 4, {width-12} 4, {width-1} 15, {width-1} 32, 1 32, 1 15"
           fill="{bg}" stroke="{border}" stroke-width="2"/>
  <polygon points="14 7, {width-14} 7, {width-4} 16, {width-4} 29, 4 29, 4 16"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <line x1="20" y1="32" x2="{width-20}" y2="32" stroke="{acc}" stroke-width="1" stroke-dasharray="6,4" opacity="0.6"/>

  <!-- DOWNWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="26" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="32" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="26" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="32" width="4" height="6" fill="{prim}"/>

  <!-- Status LED -->
  <circle cx="24" cy="18" r="4" fill="{prim}" class="led"/>

  <!-- Title Text -->
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">
    <tspan fill="{acc}">[//]</tspan> {title_disp}
  </text>

  <!-- Right Status Tag -->
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-127}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_disp}</text>{tag_link_close}

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/>
  <text x="{width-64}" y="21" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/>
  <text x="{width-47}" y="22" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="{tertiary_col}"/>
  <text x="{width-28}" y="22" fill="{text_main}" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
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
  <path d="M {width-4} 14 L {width-4} 4 L {width-14} 4" fill="none" stroke="{acc}" stroke-width="1.5"/>
  <line x1="8" y1="{h-2}" x2="{width-8}" y2="{h-2}" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <circle cx="24" cy="18" r="4" fill="{prim}"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_disp}</text>
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_disp}</text>{tag_link_close}
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-64}" y="21" fill="{text_dim}" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-47}" y="22" fill="{text_dim}" font-size="10" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="{tertiary_col}"/><text x="{width-28}" y="22" fill="{text_main}" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
</svg>"""

        else:
            # Cyberpunk Brackets Top (Downward prongs on x=1 and x=849)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="4" width="{width-2}" height="28" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="3" y="6" width="{width-6}" height="24" fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <rect x="1" y="4" width="5" height="5" fill="{prim}"/>
  <rect x="{width-6}" y="4" width="5" height="5" fill="{acc}"/>
  <!-- Downward Embracing Prongs (Flush x=1 and x={width-1}) -->
  <line x1="1" y1="24" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="32" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="24" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="32" width="4" height="6" fill="{prim}"/>
  <circle cx="24" cy="18" r="4" fill="{prim}" class="led"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono"><tspan fill="{acc}">[//]</tspan> {title_disp}</text>
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_disp}</text>{tag_link_close}
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-64}" y="21" fill="{text_dim}" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-47}" y="22" fill="{text_dim}" font-size="10" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="{tertiary_col}"/><text x="{width-28}" y="22" fill="{text_main}" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
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
  <line x1="12" y1="20" x2="{width-12}" y2="20" stroke="{acc}" stroke-width="2"/>

  <!-- Center Status Buffer Readout -->
  <rect x="{bx}" y="4" width="{bot_w}" height="16" fill="{bg}" stroke="{acc}" stroke-width="1"/>
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
  <path d="M {width-4} 8 L {width-4} 18 L {width-14} 18" fill="none" stroke="{acc}" stroke-width="1.5"/>
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
  <path d="M 1 12 L 1 20 L 16 20" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="1" y="17" width="4" height="4" fill="{acc}"/>
  <path d="M {width-1} 12 L {width-1} 20 L {width-16} 20" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-5}" y="17" width="4" height="4" fill="{acc}"/>
  <rect x="{bx}" y="4" width="{bot_w}" height="16" fill="{bg}" stroke="{acc}" stroke-width="1"/>
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
    if width is not None:
        text_clean = clamp_text_to_width(text_clean, max(20, width - 36), 10)
    text_w = estimate_chip_width(text_clean)

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
            elif dd == "left":
                # Tactical Hazard Slash Decay Left
                slash_zone = 26
                left_pad = slash_zone + 12
                right_pad = 16
                box_l = slash_zone + 2
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + 4
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
  <polygon points="{w-14} 9, {w-9} 13, {w-14} 17" fill="{prim}"/>
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
            if dd == "both":
                dissolve_zone = 32
                box_l = dissolve_zone + 2
                left_pad = dissolve_zone + 14
                right_pad = 14
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + dissolve_zone + 4
                w = width if width is not None else calc_w
                text_x = int(w / 2)
                dash_start = box_l - 16
                dash_end = box_r + 16

                cl1, cl2, cl3, cl4 = box_l - 7, box_l - 14, box_l - 21, box_l - 28
                cr1, cr2, cr3, cr4 = box_r + 7, box_r + 14, box_r + 21, box_r + 28

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <line x1="{dash_start}" y1="1" x2="{box_l}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{dash_start}" y1="25" x2="{box_l}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{box_r}" y1="1" x2="{dash_end}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{box_r}" y1="25" x2="{dash_end}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <g fill="{prim}">
    <circle cx="{cl1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{cl2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{cl3}" cy="10" r="1" opacity="0.35"/><circle cx="{cl3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{cl4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{cl4}" cy="14" r="0.8" opacity="0.2"/>
    <circle cx="{cr1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{cr1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{cr1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{cr1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{cr2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{cr2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{cr2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{cr3}" cy="10" r="1" opacity="0.35"/><circle cx="{cr3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{cr4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{cr4}" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                dissolve_zone = 32
                box_l = dissolve_zone + 2
                left_pad = dissolve_zone + 14
                right_pad = 16
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + 4
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                dash_start = box_l - 16
                cl1, cl2, cl3, cl4 = box_l - 7, box_l - 14, box_l - 21, box_l - 28

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{bg}"/>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <line x1="{dash_start}" y1="1" x2="{box_l}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{dash_start}" y1="25" x2="{box_l}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <path d="M {w-5} 8 L {w-5} 4 L {w-9} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-5} 18 L {w-5} 22 L {w-9} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <g fill="{prim}">
    <circle cx="{cl1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{cl2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{cl3}" cy="10" r="1" opacity="0.35"/><circle cx="{cl3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{cl4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{cl4}" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            else:
                # Minimal Glass Micro-Stipple Dissolution Right (default)
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
            if dd == "both":
                dither_zone = 26
                box_l = dither_zone + 2
                left_pad = dither_zone + 12
                right_pad = 12
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + dither_zone + 4
                w = width if width is not None else calc_w
                text_x = int(w / 2)

                dl1, dl2, dl3, dl4, dl5 = box_l - 2, box_l - 8, box_l - 14, box_l - 20, box_l - 24
                dr1, dr2, dr3, dr4, dr5 = box_r + 2, box_r + 8, box_r + 14, box_r + 20, box_r + 24

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <g fill="{prim}">
    <!-- Left Dither -->
    <rect x="{dl1-3}" y="3" width="3" height="3"/><rect x="{dl1-3}" y="9" width="3" height="3"/><rect x="{dl1-3}" y="15" width="3" height="3"/><rect x="{dl1-3}" y="20" width="3" height="3"/>
    <rect x="{dl2-2}" y="5" width="2" height="2"/><rect x="{dl2-2}" y="12" width="2" height="2"/><rect x="{dl2-2}" y="18" width="2" height="2"/>
    <rect x="{dl3-2}" y="7" width="2" height="2" opacity="0.7"/><rect x="{dl3-2}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{dl4-1.5}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{dl5-1}" y="6" width="1" height="1" opacity="0.3"/>
    <!-- Right Dither -->
    <rect x="{dr1}" y="3" width="3" height="3"/><rect x="{dr1}" y="9" width="3" height="3"/><rect x="{dr1}" y="15" width="3" height="3"/><rect x="{dr1}" y="20" width="3" height="3"/>
    <rect x="{dr2}" y="5" width="2" height="2"/><rect x="{dr2}" y="12" width="2" height="2"/><rect x="{dr2}" y="18" width="2" height="2"/>
    <rect x="{dr3}" y="7" width="2" height="2" opacity="0.7"/><rect x="{dr3}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{dr4}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{dr5}" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                dither_zone = 26
                box_l = dither_zone + 2
                left_pad = dither_zone + 12
                right_pad = 18
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + 4
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                dl1, dl2, dl3, dl4, dl5 = box_l - 2, box_l - 8, box_l - 14, box_l - 20, box_l - 24

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{bg}"/>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="22" width="3" height="3" fill="{prim}"/>
  <rect x="{w-10}" y="8" width="3" height="10" fill="{prim}"/>
  <g fill="{prim}">
    <rect x="{dl1-3}" y="3" width="3" height="3"/><rect x="{dl1-3}" y="9" width="3" height="3"/><rect x="{dl1-3}" y="15" width="3" height="3"/><rect x="{dl1-3}" y="20" width="3" height="3"/>
    <rect x="{dl2-2}" y="5" width="2" height="2"/><rect x="{dl2-2}" y="12" width="2" height="2"/><rect x="{dl2-2}" y="18" width="2" height="2"/>
    <rect x="{dl3-2}" y="7" width="2" height="2" opacity="0.7"/><rect x="{dl3-2}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{dl4-1.5}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{dl5-1}" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            else:
                # Pixel Matrix Dither Decay Right (default)
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
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.4s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{acc}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{acc}"/>
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

    mid_x = width // 2
    max_lbl_w = width - 80
    lbl_disp = clamp_text_to_width(lbl_clean, max_lbl_w - 40, 9)
    text_w = measure_mono_text_width(lbl_disp, 9) + 40
    box_w = max(140, min(max_lbl_w, int(text_w)))
    x1 = mid_x - box_w // 2
    x2 = mid_x + box_w // 2
    l_end = max(1, x1 - 10)
    r_start = min(width - 1, x2 + 10)

    if st == "tactical":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="{l_end}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{r_start}" y1="11" x2="{width-1}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="1 11, 8 7, 8 15" fill="{prim}"/>
  <polygon points="{width-1} 11, {width-8} 7, {width-8} 15" fill="{prim}"/>
  <polygon points="{x1} 3, {x2} 3, {x2+6} 11, {x2} 19, {x1} 19, {x1-6} 11" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{mid_x}" y="14" fill="{prim}" text-anchor="middle" class="font-mono">▲ {lbl_disp} ▲</text>
</svg>"""

    elif st == "minimal":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="{l_end}" y2="11" stroke="{border}" stroke-width="1"/>
  <line x1="{r_start}" y1="11" x2="{width-1}" y2="11" stroke="{border}" stroke-width="1"/>
  <rect x="{x1}" y="2" width="{box_w}" height="18" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{mid_x}" y="14" fill="{prim}" text-anchor="middle" class="font-mono">{lbl_disp}</text>
</svg>"""

    else:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="{l_end}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{r_start}" y1="11" x2="{width-1}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="8" width="6" height="6" fill="{acc}"/>
  <rect x="{width-7}" y="8" width="6" height="6" fill="{acc}"/>
  <rect x="{x1}" y="2" width="{box_w}" height="18" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="{x1}" y="2" width="4" height="4" fill="{acc}"/>
  <rect x="{x2-4}" y="2" width="4" height="4" fill="{acc}"/>
  <text x="{mid_x}" y="14" fill="{prim}" text-anchor="middle" class="font-mono"><tspan fill="{acc}">//</tspan> {lbl_disp} <tspan fill="{acc}">//</tspan></text>
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

    # Repository header bar
    repo_header_str = f"■ REPOSITORY // {repo_clean}"
    repo_box_w = min(540, max(360, int(measure_mono_text_width(repo_header_str, 13) + 32)))
    repo_disp = clamp_text_to_width(repo_header_str, repo_box_w - 28, 13)
    badge2_x = 80 + repo_box_w + 14

    # 3D Pixel Title at px_size=7 (or 6 if long)
    px_size = 6 if len(title) > 14 else 7
    pixel_markup, t_w, t_h = render_3d_text(
        title, x=80, y=170, px_size=px_size,
        front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
        spacing=2, max_width=750, allow_wrap=True
    )

    y_sub = 170 + t_h + 24
    max_sub_w = 740
    sub_disp = clamp_text_to_width(sub_clean, max_sub_w - 50, 15)
    sub_w = min(max_sub_w, max(320, int(measure_mono_text_width(f"▶ {sub_disp}", 15) + 40)))

    # Parse technology/feature tags
    if not tags:
        tag_list = ["GITHUB", "OPEN-SOURCE", "v5.0"]
    elif isinstance(tags, str):
        tag_list = [t.strip().upper() for t in tags.split(",") if t.strip()]
    else:
        tag_list = [str(t).strip().upper() for t in tags if t]
    tag_chips = []
    curr_x = 80
    for t_item in tag_list[:5]:
        t_clean = escape_xml(t_item)
        tw = int(measure_mono_text_width(t_clean, 12) + 28)
        if curr_x + tw > 860:
            break
        tag_chips.append(f"""
    <g transform="translate({curr_x}, 530)">
      <rect x="0" y="0" width="{tw}" height="34" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
      <rect x="0" y="0" width="4" height="34" fill="{prim}"/>
      <text x="{tw//2 + 2}" y="22" fill="{acc}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">{t_clean}</text>
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
  <rect x="80" y="56" width="{repo_box_w}" height="34" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
  <text x="96" y="78" fill="{prim}" font-size="13" font-weight="bold" letter-spacing="1px" class="font-mono">{repo_disp}</text>
  <rect x="{badge2_x}" y="56" width="140" height="34" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
  <text x="{badge2_x + 70}" y="78" fill="{acc}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">PUBLIC // v5.0</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE CALLOUT -->
  <rect x="80" y="{y_sub}" width="{sub_w}" height="42" fill="{panel}" stroke="{acc}" stroke-width="1.5"/>
  <text x="100" y="{y_sub + 27}" fill="{text_main}" font-size="15" font-weight="bold" class="font-mono">▶ {sub_disp}</text>

  <!-- TECH / FEATURE TAGS ROW -->
  {chips_markup}

  <!-- RIGHT SIDE RETICLE -->
  {reticle}

  <!-- WATERMARK -->
  <text x="{width-80}" y="{height-40}" fill="{text_dim}" font-size="12" font-weight="bold" text-anchor="end" class="font-mono">PIXEL-README-KIT // 1280x640 OPENGRAPH</text>
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
# STAR HISTORY / GROWTH TREND CHART (v5.0 - 850x230)
# ==============================================================================

def generate_starchart(style="cyberpunk", primary=None, accent=None,
                       repo="Kazinagg/pixel-readme-kit", points=None,
                       current=None, delta="+78% past 6m", title="STAR GROWTH TRAJECTORY",
                       period="6M", width=850, height=230, mode="auto", preset=None):
    """
    Renders an authentic, vector SVG star trend chart / activity chart (850x230).
    Features:
    - Glowing polyline curve and area gradient fill
    - Dynamic coordinate grid with Y-value levels and X-period labels
    - Peak milestone marker with star count callout tag
    - Authentic HUD header plate with live/custom repository stats
    """
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    st = style.lower() if style else "cyberpunk"

    title_clean = escape_xml(title.upper())
    repo_clean = escape_xml(repo.strip())
    delta_clean = escape_xml(delta)

    # Parse points
    if points is None:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, str):
        pts = []
        for x in points.split(","):
            x = x.strip()
            if x:
                try:
                    pts.append(float(x))
                except ValueError:
                    pass
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, (list, tuple)):
        pts = [float(x) for x in points if x is not None]
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    else:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]

    cur_val = current if current else (f"{int(pts[-1]):,}" if pts else "1,650")

    # Geometry bounds
    pad_left = 75
    pad_right = 800
    chart_w = pad_right - pad_left
    pad_top = 70
    pad_bot = 185
    chart_h = pad_bot - pad_top

    min_v = 0.0
    max_v = max(pts) if pts else 1000.0
    if max_v <= 0:
        max_v = 100.0

    # Calculate coordinates
    n = len(pts)
    step_x = chart_w / (n - 1) if n > 1 else chart_w
    coords = []
    for i, val in enumerate(pts):
        cx = pad_left + i * step_x
        ratio = (val - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        cy = pad_bot - ratio * chart_h
        coords.append((cx, cy, val))

    # Polyline and area paths
    line_points_str = " ".join(f"{cx:.1f},{cy:.1f}" for cx, cy, _ in coords)
    first_x, first_y = coords[0][0], coords[0][1]
    last_x, last_y = coords[-1][0], coords[-1][1]
    area_path = f"M {first_x:.1f} {pad_bot} L " + " L ".join(f"{cx:.1f} {cy:.1f}" for cx, cy, _ in coords) + f" L {last_x:.1f} {pad_bot} Z"

    # Grid lines (4 horizontal)
    grid_lines = []
    y_labels = []
    for step in range(4):
        gy = pad_bot - step * (chart_h / 3.0)
        g_val = int(min_v + step * (max_v - min_v) / 3.0)
        v_str = f"{g_val/1000.0:.1f}k" if g_val >= 1000 else str(g_val)
        grid_lines.append(f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{pad_right}" y2="{gy:.1f}" stroke="{border}" stroke-width="1" stroke-dasharray="4 4" opacity="0.6"/>')
        y_labels.append(f'<text x="{pad_left - 10}" y="{gy + 4:.1f}" fill="{text_dim}" font-size="10" text-anchor="end" class="font-mono">{v_str}</text>')

    # Vertical ticks & X labels
    x_ticks = []
    x_labels = []
    month_names = ["M-5", "M-4", "M-3", "M-2", "M-1", "NOW"]
    for i, (cx, cy, val) in enumerate(coords):
        lbl = month_names[i] if i < len(month_names) else f"T{i+1}"
        x_ticks.append(f'<line x1="{cx:.1f}" y1="{pad_top}" x2="{cx:.1f}" y2="{pad_bot}" stroke="{border}" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.35"/>')
        x_labels.append(f'<text x="{cx:.1f}" y="{pad_bot + 18}" fill="{text_dim}" font-size="10.5" font-weight="bold" text-anchor="middle" class="font-mono">{lbl}</text>')

    # Peak Callout Tag & Data points circles
    dots = []
    callout_text = f"★ {cur_val}"
    callout_w = max(76, int(measure_mono_text_width(callout_text, 11) + 20))

    for i, (cx, cy, val) in enumerate(coords):
        if i == len(coords) - 1:
            tag_y = cy + 12 if cy < 65 else cy - 30
            tag_x = max(pad_left, min(width - callout_w - 14, cx - callout_w // 2))
            dots.append(f"""
    <!-- Peak Milestone Marker -->
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{acc}" opacity="0.25"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="{prim}"/>
    <!-- Peak Callout Tag -->
    <g transform="translate({tag_x:.1f}, {tag_y:.1f})">
      <rect x="0" y="0" width="{callout_w}" height="22" rx="3" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
      <text x="{callout_w // 2}" y="15" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{callout_text}</text>
    </g>""")
        else:
            dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{panel}" stroke="{prim}" stroke-width="1.8"/>')

    if st == "tactical":
        chassis = f"""
  <polygon points="12 1, {width-12} 1, {width-1} 12, {width-1} {height-12}, {width-12} {height-1}, 12 {height-1}, 1 {height-12}, 1 12"
           fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="1" width="12" height="12" fill="{prim}"/>
  <rect x="{width-13}" y="{height-13}" width="12" height="12" fill="{acc}"/>
  <line x1="20" y1="1" x2="60" y2="1" stroke="{prim}" stroke-width="2"/>
"""
    elif st in ("minimal", "clean-mono", "corporate-blue", "academic-paper", "modern-slate"):
        chassis = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="4" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <line x1="1" y1="1" x2="{width-1}" y2="1" stroke="{prim}" stroke-width="2"/>
"""
    else:  # cyberpunk
        chassis = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="1" width="8" height="8" fill="{prim}"/>
  <rect x="{width-9}" y="1" width="8" height="8" fill="{acc}"/>
  <rect x="1" y="{height-9}" width="8" height="8" fill="{acc}"/>
  <rect x="{width-9}" y="{height-9}" width="8" height="8" fill="{prim}"/>
"""

    # Dynamic Stats Badges
    badge1_text = f"★ {cur_val}"
    badge1_w = max(90, int(measure_mono_text_width(badge1_text, 12) + 24))
    badge2_text = delta_clean
    badge2_w = max(90, int(measure_mono_text_width(badge2_text, 11) + 24))
    badges_total_w = badge1_w + 8 + badge2_w
    badges_x = width - badges_total_w - 20

    # Dynamic Header Bar and Title / Repo Positioning
    max_hdr_w = badges_x - 32
    title_disp = f"★ {title_clean}"
    title_w = measure_mono_text_width(title_disp, 11.5)

    if title_w > max_hdr_w - 30:
        title_disp = clamp_text_to_width(title_disp, max_hdr_w - 30, 11.5)
        title_w = measure_mono_text_width(title_disp, 11.5)
        repo_markup = ""
        bar_w = int(title_w + 26)
    else:
        repo_disp = f"// {repo_clean}"
        avail_repo_w = max_hdr_w - title_w - 35
        if avail_repo_w >= 40:
            repo_disp = clamp_text_to_width(repo_disp, avail_repo_w, 11)
            repo_x = int(32 + title_w + 14)
            repo_markup = f'<text x="{repo_x}" y="35" fill="{text_dim}" font-size="11" class="font-mono">{repo_disp}</text>'
            bar_w = int(repo_x + measure_mono_text_width(repo_disp, 11) + 14)
        else:
            repo_markup = ""
            bar_w = int(title_w + 26)

    bar_w = min(max_hdr_w, max(260, bar_w))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
    <linearGradient id="grad-star-area" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{prim}" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="{prim}" stop-opacity="0.01"/>
    </linearGradient>
  </defs>

  {chassis}

  <!-- HEADER BAR -->
  <rect x="20" y="16" width="{bar_w}" height="28" fill="{panel}" stroke="{border}" stroke-width="1"/>
  <rect x="20" y="16" width="4" height="28" fill="{prim}"/>
  <text x="32" y="35" fill="{prim}" font-size="11.5" font-weight="bold" letter-spacing="0.5px" class="font-mono">{title_disp}</text>
  {repo_markup}

  <!-- STATS BADGES -->
  <g transform="translate({badges_x}, 16)">
    <rect x="0" y="0" width="{badge1_w}" height="28" fill="{panel}" stroke="{prim}" stroke-width="1"/>
    <text x="{badge1_w // 2}" y="19" fill="{prim}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">{badge1_text}</text>
    <rect x="{badge1_w + 8}" y="0" width="{badge2_w}" height="28" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{badge1_w + 8 + badge2_w // 2}" y="19" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{badge2_text}</text>
  </g>

  <!-- GRID & AXES -->
  {"".join(grid_lines)}
  {"".join(y_labels)}
  {"".join(x_ticks)}
  {"".join(x_labels)}

  <!-- CHART AREA & LINE -->
  <path d="{area_path}" fill="url(#grad-star-area)" shape-rendering="geometricPrecision"/>
  <path d="M {line_points_str.replace(' ', ' L ')}" fill="none" stroke="{prim}" stroke-width="2.5" shape-rendering="geometricPrecision"/>

  <!-- DATA VERTICES -->
  {"".join(dots)}
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
# DEVELOPER PROFILE CARD (v5.0 - 850x190)
# ==============================================================================

def generate_profile_card(style="cyberpunk", primary=None, accent=None,
                          name="ALEX DEVELOPER", role="FULLSTACK & SYSTEMS ARCHITECT",
                          bio="Building high-performance runtimes and resilient developer tooling.",
                          status="AVAILABLE FOR HIRE", location="REMOTE // UTC+3",
                          badge="LEVEL_99", width=850, height=190, mode="auto", preset=None):
    """
    Renders a flagship developer dossier / identity header card (850x190) for GitHub Profiles.
    Features:
    - Stylized cyber avatar frame with status LED ring
    - 3D Typography name header and role descriptor
    - Clean manifesto / bio summary section
    - Multi-mode theming and responsive vector geometry
    """
    c, css_vars = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    st = style.lower() if style else "cyberpunk"

    name_clean = escape_xml(name.upper())
    role_clean = escape_xml(role.upper())
    bio_clean = escape_xml(bio)
    status_clean = escape_xml(status.upper())
    loc_clean = escape_xml(location.upper())
    badge_clean = escape_xml(badge.upper())

    # 3D Name Typography - single-line with adaptive downscaling to prevent collision
    max_name_w = width - 180 - 40
    lines, calc_px = calculate_smart_layout(name, max_width=max_name_w, default_px_size=5, min_px_size=3, spacing=2, allow_wrap=False)
    single_name = lines[0] if lines else name
    pixel_name, n_w, n_h = render_3d_text(
        single_name, x=180, y=58, px_size=calc_px,
        front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
        spacing=2, max_width=max_name_w, allow_wrap=False
    )

    # Avatar geometry
    av_x, av_y, av_size = 28, 28, 134

    if st == "tactical":
        chassis = f"""
  <polygon points="14 1, {width-14} 1, {width-1} 14, {width-1} {height-14}, {width-14} {height-1}, 14 {height-1}, 1 {height-14}, 1 14"
           fill="{bg}" stroke="{border}" stroke-width="1.8"/>
  <rect x="1" y="1" width="14" height="14" fill="{prim}"/>
  <rect x="{width-15}" y="1" width="14" height="14" fill="{acc}"/>
  <rect x="1" y="{height-15}" width="14" height="14" fill="{acc}"/>
  <rect x="{width-15}" y="{height-15}" width="14" height="14" fill="{prim}"/>
"""
    elif st in ("minimal", "clean-mono", "corporate-blue", "academic-paper", "modern-slate"):
        chassis = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="4" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <line x1="1" y1="1" x2="{width-1}" y2="1" stroke="{prim}" stroke-width="3"/>
"""
    else:  # cyberpunk
        chassis = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="1" width="10" height="10" fill="{prim}"/>
  <rect x="{width-11}" y="1" width="10" height="10" fill="{acc}"/>
  <rect x="1" y="{height-11}" width="10" height="10" fill="{acc}"/>
  <rect x="{width-11}" y="{height-11}" width="10" height="10" fill="{prim}"/>
  <line x1="1" y1="36" x2="16" y2="36" stroke="{prim}" stroke-width="2"/>
  <line x1="{width-16}" y1="{height-36}" x2="{width-1}" y2="{height-36}" stroke="{acc}" stroke-width="2"/>
"""

    # Dynamic badges and status pills (top right)
    badge_disp = clamp_text_to_width(badge_clean, 120, 10.5)
    badge_w = max(70, int(measure_mono_text_width(badge_disp, 10.5) + 20))
    status_disp = clamp_text_to_width(status_clean, 160, 10)
    status_w = max(90, int(measure_mono_text_width(status_disp, 10) + 32))
    pills_gap = 8
    pills_total_w = badge_w + pills_gap + status_w
    pills_x = width - pills_total_w - 20

    # Top breadcrumb dossier (between avatar right margin x=180 and pills_x)
    avail_dossier_w = max(60, pills_x - 180 - 15)
    dossier_full = f"■ DOSSIER // {loc_clean}"
    dossier_disp = clamp_text_to_width(dossier_full, avail_dossier_w - 24, 11)
    dossier_w = max(120, min(avail_dossier_w, int(measure_mono_text_width(dossier_disp, 11) + 24)))

    # Role pill
    max_role_w = width - 180 - 30
    role_disp = clamp_text_to_width(f"▶ {role_clean}", max_role_w - 28, 12)
    role_w = max(160, min(max_role_w, int(measure_mono_text_width(role_disp, 12) + 28)))

    # Bio summary
    bio_disp = clamp_text_to_width(bio_clean, width - 180 - 30, 12)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>

  {chassis}

  <!-- AVATAR CHASSIS -->
  <g transform="translate({av_x}, {av_y})">
    <rect x="0" y="0" width="{av_size}" height="{av_size}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
    <rect x="4" y="4" width="{av_size-8}" height="{av_size-8}" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="8 4"/>
    <!-- Stylized User Silhouette Vector -->
    <circle cx="{av_size//2}" cy="50" r="24" fill="{bg}" stroke="{prim}" stroke-width="2"/>
    <path d="M 28 106 C 28 80, {av_size-28} 80, {av_size-28} 106 Z" fill="{bg}" stroke="{prim}" stroke-width="2"/>
    <circle cx="{av_size//2}" cy="50" r="12" fill="{acc}"/>
    <!-- Status LED pill -->
    <rect x="12" y="112" width="{av_size-24}" height="16" fill="{bg}" stroke="{success}" stroke-width="1"/>
    <circle cx="22" cy="120" r="3" fill="{success}"/>
    <text x="30" y="123" fill="{success}" font-size="8.5" font-weight="bold" class="font-mono">ONLINE</text>
  </g>

  <!-- TOP BREADCRUMB -->
  <rect x="180" y="24" width="{dossier_w}" height="24" fill="{panel}" stroke="{border}" stroke-width="1"/>
  <text x="192" y="40" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">{dossier_disp}</text>

  <!-- BADGE AND STATUS PILLS (TOP RIGHT) -->
  <g transform="translate({pills_x}, 24)">
    <rect x="0" y="0" width="{badge_w}" height="24" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{badge_w // 2}" y="16" fill="{acc}" font-size="10.5" font-weight="bold" text-anchor="middle" class="font-mono">{badge_disp}</text>
    <rect x="{badge_w + pills_gap}" y="0" width="{status_w}" height="24" fill="{panel}" stroke="{success}" stroke-width="1"/>
    <circle cx="{badge_w + pills_gap + 12}" y="12" r="3" fill="{success}"/>
    <text x="{badge_w + pills_gap + 12 + (status_w - 12) // 2}" y="16" fill="{success}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{status_disp}</text>
  </g>

  <!-- 3D NAME TYPOGRAPHY -->
  {pixel_name}

  <!-- ROLE PILL -->
  <g transform="translate(180, 116)">
    <rect x="0" y="0" width="{role_w}" height="26" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
    <rect x="0" y="0" width="4" height="26" fill="{prim}"/>
    <text x="14" y="17" fill="{acc}" font-size="12" font-weight="bold" class="font-mono">{role_disp}</text>
  </g>

  <!-- BIO SUMMARY -->
  <text x="182" y="166" fill="{text_main}" font-size="12" font-weight="normal" class="font-mono">{bio_disp}</text>
</svg>"""

    validate_svg(svg)
    return svg


