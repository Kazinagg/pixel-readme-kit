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
import xml.etree.ElementTree as ET
from generator.font_engine import render_3d_text, calculate_px_size

STYLE_PALETTES = {
    "cyberpunk": {
        "primary": "#00C8D7",
        "accent": "#A855F7",
        "bg": "rgba(10, 14, 23, 0.82)",
        "panel": "rgba(15, 23, 38, 0.78)",
        "border": "rgba(30, 41, 59, 0.85)",
        "success": "#00D26A",
        "warning": "#F59E0B",
        "shadow_mid": "#005577",
        "shadow_dark": "#050B14"
    },
    "tactical": {
        "primary": "#F59E0B",
        "accent": "#EA580C",
        "bg": "rgba(20, 14, 6, 0.88)",
        "panel": "rgba(30, 22, 10, 0.82)",
        "border": "rgba(50, 36, 16, 0.85)",
        "success": "#10B981",
        "warning": "#F59E0B",
        "shadow_mid": "#4A3305",
        "shadow_dark": "#0A0702"
    },
    "minimal": {
        "primary": "#4F8BFF",
        "accent": "#A855F7",
        "bg": "rgba(15, 18, 30, 0.82)",
        "panel": "rgba(22, 27, 46, 0.78)",
        "border": "rgba(41, 46, 66, 0.85)",
        "success": "#10B981",
        "warning": "#F59E0B",
        "shadow_mid": "#1A2440",
        "shadow_dark": "#0A0C14"
    }
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

def resolve_colors(style, primary=None, accent=None):
    base = STYLE_PALETTES.get(style.lower(), STYLE_PALETTES["cyberpunk"])
    prim = primary if primary else base["primary"]
    acc = accent if accent else base["accent"]
    bg = base["bg"]
    return prim, acc, bg

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
        return base["shadow_mid"], base["shadow_dark"]
    return darken_hex(primary_hex, 0.45), darken_hex(primary_hex, 0.15)


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

def generate_header(style="cyberpunk", primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                    specs=None, spec1=None, spec2=None, spec3=None,
                    tag="SYSTEM_ACTIVE", width=850, height=None):
    prim, acc, bg = resolve_colors(style, primary, accent)
    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)
    st = style.lower()
    mid_shadow, dark_shadow = get_shadow_colors(prim, st)

    # Normalize specs (max 3 items, [] if omitted)
    norm_specs = normalize_specs(specs=specs, spec1=spec1, spec2=spec2, spec3=spec3, default_color=None)

    if st == "tactical":
        h = height if height else 220
        # Determine 3D font size
        px_size = calculate_px_size(title, max_width=520, spacing=2, default_px_size=5, min_px_size=3)
        y_title = 50 if px_size <= 4 else 52
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=px_size,
            front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=520
        )
        y_sub = y_title + t_h + 8
        # Lowered specs start slightly for balanced vertical spacing
        y_specs_start = y_sub + 40

        spec_lines = []
        if norm_specs:
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                val_col = spec[2] if (len(spec) > 2 and spec[2]) else "#F8F8F2"
                y = y_specs_start + i * 20
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="11" class="font-mono">&gt; {escape_xml(lbl)}: <tspan fill="{val_col}">{escape_xml(val)}</tspan></text>
""")
        specs_markup = "".join(spec_lines)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes targetScan {{
        0% {{ transform: translateX(0px); opacity: 0; }}
        15% {{ opacity: 0.8; }}
        85% {{ opacity: 0.8; }}
        100% {{ transform: translateX({width-100}px); opacity: 0; }}
      }}
      @keyframes pulseLock {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.96); }}
      }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .laser-scan {{ animation: targetScan 4s ease-in-out infinite; }}
      .reticle-pulse {{ transform-origin: 750px 105px; animation: pulseLock 2s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. 45° CHAMFERED CHASSIS -->
  <polygon points="20 4, {width-20} 4, {width-4} 20, {width-4} {h-20}, {width-20} {h-4}, 20 {h-4}, 4 {h-20}, 4 20"
           fill="{bg}" stroke="rgba(50, 36, 16, 0.85)" stroke-width="2"/>
  
  <polygon points="24 10, {width-24} 10, {width-10} 24, {width-10} {h-24}, {width-24} {h-10}, 24 {h-10}, 10 {h-24}, 10 24"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.75"/>

  <!-- HAZARD STRIPES TOP-LEFT -->
  <g fill="{prim}" opacity="0.6">
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
  <rect x="42" y="{y_sub}" width="420" height="24" fill="rgba(30, 22, 10, 0.78)" stroke="{acc}" stroke-width="1"/>
  <text x="54" y="{y_sub+16}" fill="#FFFBEB" font-size="11" font-weight="bold" class="font-mono">
    [TARGET] {sub_clean}
  </text>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- RIGHT SIDE: TARGET LOCK-ON CROSSHAIR RETICLE -->
  <g class="reticle-pulse">
    <circle cx="750" cy="105" r="45" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8,4"/>
    <circle cx="750" cy="105" r="24" fill="none" stroke="{acc}" stroke-width="1.5"/>
    <circle cx="750" cy="105" r="4" fill="{acc}"/>
    <line x1="750" y1="50" x2="750" y2="75" stroke="{prim}" stroke-width="2"/>
    <line x1="750" y1="135" x2="750" y2="160" stroke="{prim}" stroke-width="2"/>
    <line x1="695" y1="105" x2="720" y2="105" stroke="{prim}" stroke-width="2"/>
    <line x1="780" y1="105" x2="805" y2="105" stroke="{prim}" stroke-width="2"/>
    <path d="M 725 80 L 720 80 L 720 85" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 775 80 L 780 80 L 780 85" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 725 130 L 720 130 L 720 125" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 775 130 L 780 130 L 780 125" fill="none" stroke="{prim}" stroke-width="2"/>
    <text x="750" y="168" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">TARGET LOCK</text>
  </g>

  <!-- SWEEPING TARGET LASER -->
  <g class="laser-scan">
    <line x1="50" y1="10" x2="50" y2="{h-10}" stroke="{acc}" stroke-width="1.5" opacity="0.8"/>
    <circle cx="50" cy="20" r="3" fill="{acc}"/>
    <circle cx="50" cy="{h-20}" r="3" fill="{acc}"/>
  </g>
</svg>"""

    elif st == "minimal":
        px_size = calculate_px_size(title, max_width=540, spacing=2, default_px_size=4, min_px_size=3)
        y_title = 38 if px_size <= 3 else 36
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=px_size,
            front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=540
        )
        y_sub = y_title + t_h + 8

        default_h = 135 if not norm_specs else (140 + len(norm_specs) * 18)
        h = height if height else default_h

        spec_lines = []
        if norm_specs:
            y_specs_start = y_sub + 38
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                col = spec[2] if (len(spec) > 2 and spec[2]) else "#F8F8F2"
                y = y_specs_start + i * 18
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="10" class="font-mono">// {escape_xml(lbl)}: <tspan fill="{col}">{escape_xml(val)}</tspan></text>
""")
        specs_markup = "".join(spec_lines)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
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
  <rect x="4" y="4" width="{width-8}" height="{h-8}" fill="{bg}" stroke="rgba(41, 46, 66, 0.85)" stroke-width="2"/>
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
    <rect x="0" y="0" width="400" height="22" fill="rgba(22, 27, 46, 0.78)" stroke="{acc}" stroke-width="1"/>
    <text x="12" y="15" fill="#F1F5F9" font-size="11" font-weight="bold" class="font-mono">⚡ {sub_clean}</text>
  </g>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- EQUALIZER BARS (RIGHT SIDE) -->
  <g transform="translate({width-120}, 45)">
    <rect x="0" y="28" width="8" height="12" fill="{prim}" class="eq1"/>
    <rect x="14" y="12" width="8" height="28" fill="{acc}" class="eq2"/>
    <rect x="28" y="22" width="8" height="18" fill="#06B6D4" class="eq3"/>
    <rect x="42" y="6" width="8" height="34" fill="#F59E0B" class="eq4"/>
    <rect x="56" y="18" width="8" height="22" fill="#10B981" class="eq5"/>
    <text x="32" y="52" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">LIVE_AUDIO</text>
  </g>
</svg>"""

    else:
        # Cyberpunk Workstation (Default Flagship: 360° Animated Radar, CRT Scanline, 20px Grid, Equalizer)
        h = height if height else 260
        grid_lines = []
        for x in range(0, width + 1, 20):
            grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{prim}" stroke-width="1"/>')
        for y in range(0, h + 1, 20):
            grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{prim}" stroke-width="1"/>')

        px_size = calculate_px_size(title, max_width=520, spacing=2, default_px_size=6, min_px_size=3)
        y_title = 65 if px_size >= 5 else 60
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=px_size,
            front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=520
        )
        y_sub = y_title + t_h + 8

        teletype_block = ""
        if norm_specs:
            teletype_svg = []
            # Lowered slightly for breathing room below subtitle box
            y_teletype_start = max(182, y_sub + 36)
            default_colors = [prim, acc, "#00D26A"]
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                col = spec[2] if (len(spec) > 2 and spec[2]) else default_colors[i % 3]
                y_pos = y_teletype_start + i * 20
                teletype_svg.append(f"""
    <text x="42" y="{y_pos}" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="{y_pos}" fill="#F8F8F2" font-size="11" class="font-mono">{escape_xml(lbl)}:</text>
    <text x="210" y="{y_pos}" fill="{col}" font-size="11" font-weight="bold" class="font-mono">{escape_xml(val)}</text>
""")

            last_y = y_teletype_start + (len(norm_specs) - 1) * 20
            eq_offset = last_y - 210
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
    <rect x="24" y="182" width="5" height="22" fill="#F59E0B" class="w4"/>
  </g>
"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes ledFlicker {{
        0%, 100% {{ fill: #00D26A; }}
        50% {{ fill: #005511; }}
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
  <g opacity="0.08">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{prim}" stroke-width="2" class="scan-line"/>

  <!-- 4. OUTER CHASSIS / BORDER -->
  <rect x="6" y="6" width="{width-12}" height="{h-12}" fill="none" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
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
  <rect x="14" y="14" width="{width-28}" height="22" fill="rgba(15, 23, 38, 0.78)"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="{prim}" stroke-width="1.5" opacity="0.6"/>

  <circle cx="28" cy="25" r="4" fill="#00D26A" class="status-led"/>
  <text x="38" y="29" fill="#00D26A" font-size="11" font-weight="bold" class="font-mono">SYS: ONLINE // 0x00</text>

  <rect x="175" y="19" width="2" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="188" y="29" fill="#94A3B8" font-size="11" class="font-mono">HUD: TRANSLUCENT_GLASS</text>

  <rect x="380" y="19" width="2" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="393" y="29" fill="#94A3B8" font-size="11" class="font-mono">MODE: CYBERPUNK_TERMINAL</text>

  <rect x="585" y="19" width="2" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="598" y="29" fill="#F59E0B" font-size="11" font-weight="bold" class="font-mono">{tag_clean}</text>

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="{width-80}" y="28" fill="#94A3B8" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="{width-59}" y="29" fill="#94A3B8" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="#FF0055"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE: ROLE & SPECIALIZATION -->
  <g transform="translate(42, {y_sub})">
    <rect x="0" y="0" width="440" height="26" fill="rgba(15, 23, 38, 0.78)" stroke="{acc}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="436" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{acc}"/>
    <rect x="436" y="22" width="6" height="6" fill="{acc}"/>
    <text x="12" y="18" fill="#F8F8F2" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ {sub_clean}
    </text>
  </g>

  {teletype_block}

  <!-- RIGHT SIDE: RETRO SCI-FI WORKBENCH / MONITOR HUD (RADAR) -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="rgba(15, 23, 38, 0.78)" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>

    <!-- Concentric Range Rings -->
    <circle cx="85" cy="70" r="50" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{prim}" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{prim}" stroke-width="1" opacity="0.3"/>

    <!-- 360° Rotating Radar Beam (SVG Native animateTransform - 100% Reliable!) -->
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="#00D26A" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="#F59E0B"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>

    <!-- Pulsing Radar Target Blips -->
    <circle cx="110" cy="50" r="3" fill="#FF0055">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="65" cy="85" r="2.5" fill="#00D26A">
      <animate attributeName="opacity" values="0.1;0.9;0.1" dur="3s" repeatCount="indefinite"/>
    </circle>

    <!-- Radar Telemetry Label -->
    <text x="85" y="132" fill="#00D26A" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">RADAR: ACTIVE (360°)</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{h-26}" x2="{width-14}" y2="{h-26}" stroke="rgba(30, 41, 59, 0.85)" stroke-width="1"/>
  <text x="24" y="{h-15}" fill="#94A3B8" font-size="9" class="font-mono">HUD_ARCH: TRANSLUCENT_V2 // GLASS_RATIO: 0.82 // DUAL_THEME: PASS</text>
  <text x="{width-24}" y="{h-15}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">READY // ID: 0xDEADBEEF</text>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 2. FOOTERS (CLOSING PLATES)
# ---------------------------------------------------------------------------

def generate_footer(style="cyberpunk", primary=None, accent=None,
                    status="SESSION_ACTIVE // STANDBY", nav_text="RETURN TO TOP",
                    width=850, height=54):
    prim, acc, bg = resolve_colors(style, primary, accent)
    status_clean = escape_xml(status)
    nav_clean = escape_xml(nav_text)
    st = style.lower()

    if st == "tactical":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Tactical 45° Hull -->
  <polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {height-12}, {width-12} {height-2}, 12 {height-2}, 2 {height-12}, 2 12"
           fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="10 8, 16 8, 8 20, 2 20" fill="{prim}" opacity="0.6"/>
  <polygon points="20 8, 26 8, 18 20, 12 20" fill="{prim}" opacity="0.6"/>
  <!-- Status Readout -->
  <text x="45" y="32" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">▲ {status_clean}</text>
  <!-- Return to Top Button -->
  <polygon points="{width-190} 12, {width-20} 12, {width-12} 20, {width-12} 36, {width-20} 42, {width-190} 42" fill="rgba(245, 158, 11, 0.18)" stroke="{prim}" stroke-width="1.5"/>
  <text x="{width-105}" y="31" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">[ ▲ {nav_clean} ]</text>
</svg>"""

    elif st == "minimal":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Hairline Glass Footer Panel -->
  <rect x="1" y="2" width="{width-2}" height="{height-4}" fill="{bg}" stroke="rgba(41, 46, 66, 0.85)" stroke-width="1.5"/>
  <path d="M 6 12 L 6 6 L 16 6" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-6} 12 L {width-6} 6 L {width-16} 6" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 6 {height-12} L 6 {height-6} L 16 {height-6}" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-6} {height-12} L {width-6} {height-6} L {width-16} {height-6}" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <!-- Status Readout -->
  <text x="35" y="32" fill="#94A3B8" font-size="11" class="font-mono">STATUS: <tspan fill="{prim}" font-weight="bold">{status_clean}</tspan></text>
  <!-- Return to top link button -->
  <rect x="{width-185}" y="12" width="160" height="30" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
  <text x="{width-105}" y="31" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">[ ▲ {nav_clean} ]</text>
</svg>"""

    else:
        # Cyberpunk Terminal Footer
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>
  <!-- Cyberpunk Chassis -->
  <rect x="1" y="2" width="{width-2}" height="{height-4}" fill="{bg}" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
  <rect x="4" y="5" width="{width-8}" height="{height-10}" fill="none" stroke="{prim}" stroke-width="1" opacity="0.75"/>
  <rect x="1" y="2" width="5" height="5" fill="{prim}"/>
  <rect x="{width-6}" y="2" width="5" height="5" fill="{prim}"/>
  <rect x="1" y="{height-7}" width="5" height="5" fill="{prim}"/>
  <rect x="{width-6}" y="{height-7}" width="5" height="5" fill="{prim}"/>
  <!-- LED Indicator & Status -->
  <circle cx="28" cy="27" r="4" fill="{prim}" class="led"/>
  <text x="45" y="31" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">{status_clean}</text>
  <!-- Return to Top Button -->
  <rect x="{width-190}" y="12" width="170" height="30" fill="rgba(0, 200, 215, 0.15)" stroke="{prim}" stroke-width="1.5"/>
  <text x="{width-105}" y="31" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">[ ▲ {nav_clean} ]</text>
</svg>"""

    validate_svg(svg)
    return svg


# ---------------------------------------------------------------------------
# 3. CALLOUTS & QUOTE HEADERS
# ---------------------------------------------------------------------------

def generate_callout(style="cyberpunk", primary=None, accent=None,
                     callout_type="note", title="SYSTEM SPECIFICATION",
                     subtitle="Dual-theme contrast > 7:1 // Monospace typography",
                     is_quote=False, width=850, height=None):
    prim, acc, bg = resolve_colors(style, primary, accent)
    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(callout_type.upper())
    st = style.lower()

    if is_quote:
        # Quote Header Callout (Open Left Edge + Dashed Bottom)
        h = height if height else 42
        if st == "tactical":
            dash_w = "8,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-12}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-12}" y1="2" x2="{width-1}" y2="13" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="13" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/>'
            badge = f'<polygon points="6 6, 12 6, 4 18, 0 18" fill="{prim}" opacity="0.6"/><polygon points="16 6, 22 6, 14 18, 8 18" fill="{prim}" opacity="0.6"/><polygon points="28 8, 165 8, 172 15, 172 27, 165 34, 28 34" fill="rgba(245, 158, 11, 0.18)" stroke="{prim}" stroke-width="1.5"/><text x="96" y="24" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} // HAZARD</text>'
            text_x = 186
            arrow_poly = f'<polygon points="{width-10} {h-5}, {width-2} {h-5}, {width-6} {h-1}" fill="{prim}"/>'
        elif st == "minimal":
            dash_w = "5,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="1.5"/><path d="M {width-1} 2 L {width-1} 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-4}" y="2" width="4" height="4" fill="{acc}"/>'
            badge = f'<rect x="8" y="8" width="115" height="24" fill="rgba(79, 139, 255, 0.15)" stroke="{prim}" stroke-width="1"/><text x="65" y="23" fill="{prim}" font-size="9.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // MINIMAL</text>'
            text_x = 136
            arrow_poly = ""
        else:
            dash_w = "6,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="2" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/><rect x="{width-6}" y="2" width="5" height="5" fill="{prim}"/>'
            badge = f'<rect x="8" y="8" width="120" height="24" fill="rgba(0, 200, 215, 0.18)" stroke="{prim}" stroke-width="1.5"/><circle cx="20" cy="20" r="3.5" fill="{prim}"/><text x="73" y="24" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // 0x01</text>'
            text_x = 142
            arrow_poly = ""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
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
  <text x="{text_x}" y="20" fill="#F8F8F2" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
  <text x="{text_x}" y="33" fill="{acc}" font-size="8.5" class="font-mono">{sub_clean}</text>
  <!-- DASHED BOTTOM LINE: Bridges into live markdown text -->
  <line x1="0" y1="{h-1}" x2="{width-5}" y2="{h-1}" stroke="{prim}" stroke-width="1.5" stroke-dasharray="{dash_w}" opacity="0.75"/>
  {arrow_poly}
</svg>"""

    else:
        # Autonomous Closed Callout (48px)
        h = height if height else 48
        if st == "tactical":
            body = f'<polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>'
            badge = f'<polygon points="34 10, 175 10, 182 17, 182 31, 175 38, 34 38" fill="rgba(245, 158, 11, 0.15)" stroke="{prim}" stroke-width="1.5"/><text x="105" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} // HAZARD</text>'
            accents = f'<polygon points="10 8, 16 8, 8 20, 2 20" fill="{prim}" opacity="0.6"/><polygon points="20 8, 26 8, 18 20, 12 20" fill="{prim}" opacity="0.6"/><circle cx="{width-25}" cy="24" r="8" fill="none" stroke="{prim}" stroke-width="1.5"/><polygon points="{width-28} 24, {width-22} 20, {width-22} 28" fill="{prim}"/>'
            text_x = 196
        elif st == "minimal":
            body = f'<rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="rgba(41, 46, 66, 0.9)" stroke-width="1.5"/>'
            badge = f'<rect x="16" y="11" width="130" height="26" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/><text x="81" y="28" fill="{prim}" font-size="10.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // MINIMAL</text>'
            accents = f'<path d="M 5 12 L 5 5 L 14 5" fill="none" stroke="{prim}" stroke-width="1.5"/><path d="M {width-5} 12 L {width-5} 5 L {width-14} 5" fill="none" stroke="{prim}" stroke-width="1.5"/>'
            text_x = 158
        else:
            body = f'<rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{prim}" stroke-width="1.5"/><rect x="2" y="2" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="2" width="5" height="5" fill="{prim}"/><rect x="2" y="{h-7}" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="{h-7}" width="5" height="5" fill="{prim}"/>'
            badge = f'<rect x="14" y="10" width="140" height="28" fill="rgba(0, 200, 215, 0.15)" stroke="{prim}" stroke-width="1.5"/><circle cx="26" cy="24" r="3.5" fill="{prim}"/><text x="88" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // 0x01</text>'
            accents = f'<rect x="{width-35}" y="14" width="20" height="20" fill="rgba(30, 41, 59, 0.85)"/><text x="{width-25}" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">ℹ</text>'
            text_x = 168

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Body Chassis -->
  {body}
  <!-- Badges & Accents -->
  {badge}
  {accents}
  <!-- Text Content (Properly offset past badge edge) -->
  <text x="{text_x}" y="22" fill="#F8F8F2" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
  <text x="{text_x}" y="36" fill="{acc}" font-size="9" class="font-mono">{sub_clean}</text>
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
                    tag="[OPEN_HUD]", width=850, height=None):
    prim, acc, bg = resolve_colors(style, primary, accent)
    title_clean = escape_xml(title)
    tag_clean = format_tag(tag)
    bot_tag_clean = format_bottom_tag(tag)
    st = style.lower()
    is_top = (frame_type.lower() == "top")

    if is_top:
        h = height if height else 38
        if st == "tactical":
            # Tactical Chamfer Top: Dual Hull, Tech Seam, Flush Downward Prongs x=1..849, LED, Buttons
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>

  <!-- DUAL TACTICAL CHASSIS -->
  <polygon points="12 4, {width-12} 4, {width-1} 15, {width-1} 32, 1 32, 1 15"
           fill="{bg}" stroke="rgba(50, 36, 16, 0.85)" stroke-width="2"/>
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
  <rect x="{width-180}" y="9" width="105" height="18" fill="rgba(30, 22, 10, 0.78)" stroke="{prim}" stroke-width="1"/>
  <text x="{width-127}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-68}" y="11" width="14" height="14" fill="rgba(50, 36, 16, 0.85)"/>
  <text x="{width-64}" y="21" fill="#8892B0" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="rgba(50, 36, 16, 0.85)"/>
  <text x="{width-47}" y="22" fill="#8892B0" font-size="10" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/>
  <text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" font-weight="bold" class="font-mono">×</text>
</svg>"""

        elif st == "minimal":
            # Minimal Glass Table Monolith Top (Hugging Ticks ┌ ┐)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}" opacity="0.45"/>
  <path d="M 4 14 L 4 4 L 14 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 14 L {width-4} 4 L {width-14} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <line x1="8" y1="{h-2}" x2="{width-8}" y2="{h-2}" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <circle cx="24" cy="18" r="4" fill="{prim}"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_clean}</text>
  <rect x="{width-180}" y="9" width="105" height="18" fill="rgba(22, 27, 46, 0.78)" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>
  <rect x="{width-68}" y="11" width="14" height="14" fill="rgba(41, 46, 66, 0.85)"/><text x="{width-64}" y="21" fill="#8892B0" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="rgba(41, 46, 66, 0.85)"/><text x="{width-47}" y="22" fill="#8892B0" font-size="10" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/><text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" class="font-mono">×</text>
</svg>"""

        else:
            # Cyberpunk Brackets Top (Downward prongs on x=1 and x=849)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="4" width="{width-2}" height="28" fill="{bg}" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
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
  <rect x="{width-180}" y="9" width="105" height="18" fill="rgba(15, 23, 38, 0.78)" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>
  <rect x="{width-68}" y="11" width="14" height="14" fill="rgba(30, 41, 59, 0.85)"/><text x="{width-64}" y="21" fill="#8892B0" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="rgba(30, 41, 59, 0.85)"/><text x="{width-47}" y="22" fill="#8892B0" font-size="10" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/><text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" class="font-mono">×</text>
</svg>"""

    else:
        # Bottom Frames
        h = height if height else 24
        if st == "tactical":
            # Tactical Chamfer Bottom: Upward Prongs Flush x=1..849, Chamfer Body, Center Buffer
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- UPWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="0" x2="1" y2="10" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="10" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>

  <polygon points="1 10, {width-1} 10, {width-12} 20, 12 20" fill="{bg}" stroke="rgba(50, 36, 16, 0.85)" stroke-width="1.5"/>
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
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}" opacity="0.35"/>
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
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- UPWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="0" x2="1" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="1" y1="12" x2="{width-1}" y2="12" stroke="rgba(30, 41, 59, 0.85)" stroke-width="3"/>
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
                  chip_type="closed", text="CHIP_LABEL", width=None, height=26):
    prim, acc, bg = resolve_colors(style, primary, accent)
    text_clean = escape_xml(text)
    st = style.lower()
    ct = chip_type.lower()
    text_w = estimate_chip_width(text)

    if st == "tactical":
        if ct == "decay":
            # Tactical Hazard Slash Decay (45° diagonal slashes fading out)
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {box_top_r} 1, {box_bot_r} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {box_top_r} 1, {box_bot_r} 25, 7 25, 1 19, 1 7" fill="rgba(245, 158, 11, 0.12)" stroke="{prim}" stroke-width="1.5"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes targetPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      .laser {{ animation: targetPulse 1.2s infinite ease-in-out; }}
    </style>
  </defs>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="rgba(245, 158, 11, 0.12)" stroke="{prim}" stroke-width="1.5"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="rgba(245, 158, 11, 0.12)" stroke="{prim}" stroke-width="1.5"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes breatheBeacon {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.25; }} }}
      .breathe {{ animation: breatheBeacon 2s infinite ease-in-out; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="rgba(0, 200, 215, 0.12)" stroke="{prim}" stroke-width="1.5"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.4s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="rgba(0, 200, 215, 0.12)" stroke="{prim}" stroke-width="1.5"/>
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
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="rgba(0, 200, 215, 0.12)" stroke="{prim}" stroke-width="1.5"/>
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

def generate_divider(style="cyberpunk", primary=None, accent=None, width=850, height=28):
    prim, acc, bg = resolve_colors(style, primary, accent)
    st = style.lower()

    if st == "tactical":
        # Pulsing Aiming Laser Divider
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
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
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 8px; font-weight: bold; letter-spacing: 1px; }}
      @keyframes barPulse {{ 0%, 100% {{ transform: scaleY(0.4); opacity: 0.5; }} 50% {{ transform: scaleY(1.2); opacity: 1; }} }}
      .s-bar {{ transform-origin: center; animation: barPulse 1.6s infinite ease-in-out; }}
    </style>
  </defs>
  <line x1="20" y1="14" x2="345" y2="14" stroke="rgba(41, 46, 66, 0.85)" stroke-width="1.5"/>
  <line x1="505" y1="14" x2="{width-20}" y2="14" stroke="rgba(41, 46, 66, 0.85)" stroke-width="1.5"/>
  <line x1="60" y1="14" x2="330" y2="14" stroke="{prim}" stroke-width="1" opacity="0.6" stroke-dasharray="12,4"/>
  <line x1="520" y1="14" x2="{width-60}" y2="14" stroke="{prim}" stroke-width="1" opacity="0.6" stroke-dasharray="12,4"/>
  <path d="M 20 8 L 20 14 L 32 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="20" y="12" width="4" height="4" fill="{acc}"/>
  <path d="M {width-20} 8 L {width-20} 14 L {width-32} 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-24}" y="12" width="4" height="4" fill="{acc}"/>
  <text x="240" y="11" fill="{prim}" text-anchor="middle" opacity="0.7" class="font-mono">// 44.1 kHz //</text>
  <text x="610" y="11" fill="{prim}" text-anchor="middle" opacity="0.7" class="font-mono">// SPECTRUM_HUD //</text>
  <rect x="355" y="2" width="140" height="24" fill="{bg}" stroke="rgba(41, 46, 66, 0.85)" stroke-width="1"/>
  {bars_markup}
</svg>"""

    else:
        # Cyberpunk PCB Trace Flow Divider
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; letter-spacing: 1px; }}
      @keyframes pcbTrace {{ 0% {{ stroke-dashoffset: 400; }} 100% {{ stroke-dashoffset: 0; }} }}
      .packet {{ stroke-dasharray: 40, 200; animation: pcbTrace 2.8s infinite linear; }}
    </style>
  </defs>
  <line x1="10" y1="14" x2="{width-10}" y2="14" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
  <line x1="10" y1="14" x2="{width-10}" y2="14" stroke="{prim}" stroke-width="2" class="packet"/>
  <circle cx="20" cy="14" r="4" fill="{prim}"/><circle cx="{width-20}" cy="14" r="4" fill="{prim}"/>
  <rect x="{width//2 - 90}" y="4" width="180" height="20" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <text x="{width//2}" y="17" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">[PCB: DATA_PACKET_FLOW]</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_splitter(style="cyberpunk", primary=None, accent=None,
                      label="[MODULE: SUB_SYSTEM]", width=850, height=22):
    prim, acc, bg = resolve_colors(style, primary, accent)
    lbl_clean = escape_xml(label)
    st = style.lower()

    if st == "tactical":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
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
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="340" y2="11" stroke="rgba(41, 46, 66, 0.9)" stroke-width="1"/>
  <line x1="510" y1="11" x2="{width-1}" y2="11" stroke="rgba(41, 46, 66, 0.9)" stroke-width="1"/>
  <rect x="350" y="2" width="150" height="18" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="425" y="14" fill="{prim}" text-anchor="middle" class="font-mono">{lbl_clean}</text>
</svg>"""

    else:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
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
