"""
Core SVG Generation Engine for Pixel Readme Kit
Produces pixel-perfect, 100% valid XML SVG assets for the 3 Global Styles:
- Cyberpunk (Cyan #00C8D7 / Purple #A855F7)
- Tactical Military (Amber #F59E0B / Orange #EA580C)
- Minimal Glass (Tokyo Blue #4F8BFF / Purple #A855F7)

Separates Style (Geometry & Mechanics) from Color (primary & accent).
"""

import html
import xml.etree.ElementTree as ET

STYLE_PALETTES = {
    "cyberpunk": {"primary": "#00C8D7", "accent": "#A855F7", "bg": "rgba(10, 14, 23, 0.85)"},
    "tactical": {"primary": "#F59E0B", "accent": "#EA580C", "bg": "rgba(20, 14, 6, 0.88)"},
    "minimal": {"primary": "#4F8BFF", "accent": "#A855F7", "bg": "rgba(15, 18, 30, 0.82)"}
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

# ---------------------------------------------------------------------------
# 1. HEADERS
# ---------------------------------------------------------------------------

def generate_header(style="cyberpunk", primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                    specs=None, tag="SYSTEM_ACTIVE", width=850, height=None):
    prim, acc, bg = resolve_colors(style, primary, accent)
    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)

    if specs is None:
        specs = [
            ("HUD ARCHITECTURE", "TRANSLUCENT GLASS // ZERO ADAPTERS"),
            ("TEXT INTEGRATION", "100% COPYABLE MARKDOWN & MATH"),
            ("ANIMATION SUITE", "LIVE RADAR // SCANLINE // EQUALIZER")
        ]

    st = style.lower()
    if st == "tactical":
        h = height if height else 220
        # Tactical Military HUD Header (Chamfers, Aiming Laser, Reticle)
        spec_lines = []
        for i, (k, v) in enumerate(specs[:3]):
            y = 150 + i * 20
            spec_lines.append(f"""
            <text x="45" y="{y}" fill="{prim}" font-size="10" font-weight="bold" class="font-mono">▲</text>
            <text x="65" y="{y}" fill="#FFFBEB" font-size="10" font-weight="bold" class="font-mono">{escape_xml(k)}:</text>
            <text x="215" y="{y}" fill="{acc}" font-size="10" class="font-mono">{escape_xml(v)}</text>
            """)
        specs_markup = "".join(spec_lines)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes laserScan {{
        0% {{ transform: translateY(0px); opacity: 0.1; }}
        50% {{ opacity: 0.85; }}
        100% {{ transform: translateY({h}px); opacity: 0.1; }}
      }}
      .laser-beam {{ animation: laserScan 2.4s infinite linear; }}
      @keyframes reticlePulse {{ 0%, 100% {{ opacity: 0.9; }} 50% {{ opacity: 0.3; }} }}
      .reticle {{ animation: reticlePulse 1.8s infinite ease-in-out; }}
    </style>
  </defs>
  <!-- Background Tactical Hull (45° Chamfered Corners) -->
  <polygon points="16 2, {width-16} 2, {width-2} 16, {width-2} {h-16}, {width-16} {h-2}, 16 {h-2}, 2 {h-16}, 2 16"
           fill="{bg}" stroke="{prim}" stroke-width="2"/>
  <!-- Hazard Corner Stripes -->
  <polygon points="14 10, 22 10, 10 22, 2 22" fill="{prim}" opacity="0.6"/>
  <polygon points="26 10, 34 10, 14 30, 6 30" fill="{prim}" opacity="0.6"/>
  <!-- Aiming Laser Line -->
  <line x1="4" y1="0" x2="{width-4}" y2="0" stroke="{acc}" stroke-width="1.5" class="laser-beam"/>
  <!-- Status Badge -->
  <polygon points="45 20, 210 20, 218 28, 218 42, 210 50, 45 50" fill="rgba(245, 158, 11, 0.15)" stroke="{prim}" stroke-width="1.5"/>
  <text x="128" y="38" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} ▲</text>
  <!-- Main Title -->
  <text x="45" y="92" fill="#F8F8F2" font-size="28" font-weight="bold" letter-spacing="2" class="font-mono">{title_clean}</text>
  <text x="45" y="118" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">&gt; {sub_clean}</text>
  <!-- Telemetry Specs -->
  {specs_markup}
  <!-- Right Reticle Target -->
  <circle cx="{width-110}" cy="90" r="45" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="10,6" opacity="0.75" class="reticle"/>
  <circle cx="{width-110}" cy="90" r="18" fill="none" stroke="{acc}" stroke-width="1.5"/>
  <circle cx="{width-110}" cy="90" r="3" fill="{prim}"/>
  <line x1="{width-165}" y1="90" x2="{width-55}" y2="90" stroke="{prim}" stroke-width="1" opacity="0.5"/>
  <line x1="{width-110}" y1="35" x2="{width-110}" y2="145" stroke="{prim}" stroke-width="1" opacity="0.5"/>
  <text x="{width-110}" y="152" fill="{prim}" font-size="9" text-anchor="middle" class="font-mono">[TARGET_LOCK]</text>
</svg>"""

    elif st == "minimal":
        h = height if height else 135
        # Minimal Glass Header (Hairline Glass, Live Frequency Equalizer)
        bars = []
        for i in range(15):
            bx = width - 200 + i * 11
            bh = 6 + (i * 7 % 22)
            by = 75 - bh
            col = prim if i % 2 == 0 else acc
            bars.append(f'<rect x="{bx}" y="{by}" width="5" height="{bh}" fill="{col}" opacity="0.8"/>')
        bars_markup = "".join(bars)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes breathe {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.35; }} }}
      .beacon {{ animation: breathe 2s infinite ease-in-out; }}
    </style>
  </defs>
  <!-- Minimal Hairline Glass Frame -->
  <rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="rgba(41, 46, 66, 0.9)" stroke-width="1.5"/>
  <!-- Corner Hugger Ticks ┌ ┐ └ ┘ -->
  <path d="M 6 16 L 6 6 L 16 6" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-6} 16 L {width-6} 6 L {width-16} 6" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 6 {h-16} L 6 {h-6} L 16 {h-6}" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-6} {h-16} L {width-6} {h-6} L {width-16} {h-6}" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <!-- Status Badge -->
  <rect x="25" y="16" width="130" height="22" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
  <circle cx="36" cy="27" r="3" fill="{prim}" class="beacon"/>
  <text x="88" y="31" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>
  <!-- Main Title -->
  <text x="25" y="74" fill="#F8F8F2" font-size="24" font-weight="bold" letter-spacing="1.5" class="font-mono">{title_clean}</text>
  <text x="25" y="98" fill="{acc}" font-size="11" class="font-mono">{sub_clean}</text>
  <!-- Mini Equalizer on Right -->
  {bars_markup}
  <text x="{width-120}" y="95" fill="{prim}" font-size="9" text-anchor="middle" class="font-mono">// 44.1 kHz SPECTRUM //</text>
</svg>"""

    else:
        # Cyberpunk Workstation (Default: 360° Radar, Scanline, CRT Grid, Corner Pixels)
        h = height if height else 260
        spec_lines = []
        for i, (k, v) in enumerate(specs[:3]):
            y = 175 + i * 22
            spec_lines.append(f"""
            <text x="42" y="{y}" fill="{prim}" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
            <text x="60" y="{y}" fill="#F8F8F2" font-size="11" class="font-mono">{escape_xml(k)}:</text>
            <text x="210" y="{y}" fill="{acc}" font-size="11" font-weight="bold" class="font-mono">{escape_xml(v)}</text>
            """)
        specs_markup = "".join(spec_lines)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes ledFlicker {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #005577; }} }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.35; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY({h}px); opacity: 0; }}
      }}
      .cursor-blink {{ animation: blink 1s infinite steps(1); }}
      .status-led {{ animation: ledFlicker 1.8s infinite steps(1); }}
      .crt-scan {{ animation: crtScanline 3.5s infinite linear; }}
    </style>
  </defs>
  <!-- Cyberpunk Translucent Glass Body -->
  <rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
  <rect x="4" y="5" width="{width-8}" height="{h-10}" fill="none" stroke="{prim}" stroke-width="1" opacity="0.75"/>
  <!-- Corner Pixel Anchors (3x3) -->
  <rect x="1" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="{width-7}" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="1" y="{h-8}" width="6" height="6" fill="{prim}"/>
  <rect x="{width-7}" y="{h-8}" width="6" height="6" fill="{prim}"/>
  <!-- CRT Scanline Simulation -->
  <line x1="4" y1="0" x2="{width-4}" y2="0" stroke="{prim}" stroke-width="1.5" class="crt-scan"/>
  <!-- Title Badge -->
  <rect x="42" y="24" width="165" height="24" fill="rgba(0, 200, 215, 0.15)" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="56" cy="36" r="4" fill="{prim}" class="status-led"/>
  <text x="120" y="40" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>
  <!-- Main Title -->
  <text x="42" y="98" fill="#F8F8F2" font-size="30" font-weight="bold" letter-spacing="2" class="font-mono">{title_clean}</text>
  <text x="42" y="130" fill="{acc}" font-size="12" font-weight="bold" class="font-mono"># {sub_clean}</text>
  <!-- Specs Teletype -->
  {specs_markup}
  <!-- 360° Rotating Radar on Right -->
  <g transform="translate({width-130}, 125)">
    <circle cx="0" cy="0" r="65" fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.65"/>
    <circle cx="0" cy="0" r="45" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.45"/>
    <circle cx="0" cy="0" r="25" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <circle cx="0" cy="0" r="3" fill="{prim}"/>
    <line x1="-65" y1="0" x2="65" y2="0" stroke="{prim}" stroke-width="1" opacity="0.4"/>
    <line x1="0" y1="-65" x2="0" y2="65" stroke="{prim}" stroke-width="1" opacity="0.4"/>
    <line x1="0" y1="0" x2="52" y2="-38" stroke="{acc}" stroke-width="2" opacity="0.9">
      <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="4s" repeatCount="indefinite"/>
    </line>
    <text x="0" y="82" fill="{prim}" font-size="9" text-anchor="middle" class="font-mono">[RADAR 360° ACTIVE]</text>
  </g>
</svg>"""

    validate_svg(svg)
    return svg

# ---------------------------------------------------------------------------
# 2. FOOTERS
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
            badge = f'<polygon points="28 8, 165 8, 172 15, 172 27, 165 34, 28 34" fill="rgba(245, 158, 11, 0.18)" stroke="{prim}" stroke-width="1.5"/><text x="96" y="24" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} // HAZARD</text>'
        elif st == "minimal":
            dash_w = "5,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="1.5"/><path d="M {width-1} 2 L {width-1} 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-4}" y="2" width="4" height="4" fill="{acc}"/>'
            badge = f'<rect x="8" y="8" width="115" height="24" fill="rgba(79, 139, 255, 0.15)" stroke="{prim}" stroke-width="1"/><text x="65" y="23" fill="{prim}" font-size="9.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // MINIMAL</text>'
        else:
            dash_w = "6,4"
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="2" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/><rect x="{width-6}" y="2" width="5" height="5" fill="{prim}"/>'
            badge = f'<rect x="8" y="8" width="120" height="24" fill="rgba(0, 200, 215, 0.18)" stroke="{prim}" stroke-width="1.5"/><circle cx="20" cy="20" r="3.5" fill="{prim}"/><text x="73" y="24" fill="{prim}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // 0x01</text>'

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Background Glass (Flush left to connect with > border-left) -->
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>
  <!-- Top Rail -->
  {top_rail}
  <!-- Badge -->
  {badge}
  <!-- Title & Subtitle -->
  <text x="145" y="20" fill="#F8F8F2" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
  <text x="145" y="33" fill="{acc}" font-size="8.5" class="font-mono">{sub_clean}</text>
  <!-- DASHED BOTTOM LINE: Bridges into live markdown text -->
  <line x1="0" y1="{h-1}" x2="{width-5}" y2="{h-1}" stroke="{prim}" stroke-width="1.5" stroke-dasharray="{dash_w}" opacity="0.75"/>
</svg>"""

    else:
        # Autonomous Closed Callout (48px)
        h = height if height else 48
        if st == "tactical":
            body = f'<polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>'
            badge = f'<polygon points="34 10, 175 10, 182 17, 182 31, 175 38, 34 38" fill="rgba(245, 158, 11, 0.15)" stroke="{prim}" stroke-width="1.5"/><text x="105" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">▲ {tag_clean} // HAZARD</text>'
            accents = f'<polygon points="10 8, 16 8, 8 20, 2 20" fill="{prim}" opacity="0.6"/><polygon points="20 8, 26 8, 18 20, 12 20" fill="{prim}" opacity="0.6"/>'
        elif st == "minimal":
            body = f'<rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="rgba(41, 46, 66, 0.9)" stroke-width="1.5"/>'
            badge = f'<rect x="16" y="11" width="130" height="26" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/><text x="81" y="28" fill="{prim}" font-size="10.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // MINIMAL</text>'
            accents = f'<path d="M 5 12 L 5 5 L 14 5" fill="none" stroke="{prim}" stroke-width="1.5"/><path d="M {width-5} 12 L {width-5} 5 L {width-14} 5" fill="none" stroke="{prim}" stroke-width="1.5"/>'
        else:
            body = f'<rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{prim}" stroke-width="1.5"/><rect x="2" y="2" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="2" width="5" height="5" fill="{prim}"/><rect x="2" y="{h-7}" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="{h-7}" width="5" height="5" fill="{prim}"/>'
            badge = f'<rect x="14" y="10" width="140" height="28" fill="rgba(0, 200, 215, 0.15)" stroke="{prim}" stroke-width="1.5"/><circle cx="26" cy="24" r="3.5" fill="{prim}"/><text x="88" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean} // 0x01</text>'
            accents = f'<rect x="{width-35}" y="14" width="20" height="20" fill="rgba(30, 41, 59, 0.85)"/><text x="{width-25}" y="28" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">ℹ</text>'

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
  <!-- Text Content -->
  <text x="180" y="22" fill="#F8F8F2" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_clean}</text>
  <text x="180" y="36" fill="{acc}" font-size="9" class="font-mono">{sub_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg

# ---------------------------------------------------------------------------
# 4. WINDOW FRAMES (TOP & BOTTOM)
# ---------------------------------------------------------------------------

def generate_frame(style="cyberpunk", primary=None, accent=None,
                   frame_type="top", title="╔═ SYSTEM.CORE // RUNTIME.SYS",
                   tag="[OPEN_HUD]", width=850, height=None):
    prim, acc, bg = resolve_colors(style, primary, accent)
    title_clean = escape_xml(title)
    tag_clean = escape_xml(tag)
    st = style.lower()
    is_top = (frame_type.lower() == "top")

    if is_top:
        h = height if height else 38
        if st == "tactical":
            # Tactical Chamfer Top (flush x=1..849)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <polygon points="12 2, {width-12} 2, {width-1} 13, {width-1} {h}, 1 {h}, 1 13" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="10 6, 16 6, 8 18, 2 18" fill="{prim}" opacity="0.6"/>
  <polygon points="20 6, 26 6, 14 18, 8 18" fill="{prim}" opacity="0.6"/>
  <text x="36" y="23" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_clean}</text>
  <rect x="{width-180}" y="9" width="105" height="20" fill="rgba(20, 14, 6, 0.85)" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="23" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>
  <rect x="{width-68}" y="11" width="14" height="14" fill="rgba(40, 30, 15, 0.85)"/><text x="{width-64}" y="21" fill="#8892B0" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="rgba(40, 30, 15, 0.85)"/><text x="{width-47}" y="22" fill="#8892B0" font-size="10" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/><text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" class="font-mono">×</text>
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
  <line x1="8" y1="36" x2="{width-8}" y2="36" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
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
    </style>
  </defs>
  <rect x="1" y="4" width="{width-2}" height="28" fill="{bg}" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
  <rect x="3" y="6" width="{width-6}" height="24" fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <rect x="1" y="4" width="5" height="5" fill="{prim}"/>
  <rect x="{width-6}" y="4" width="5" height="5" fill="{prim}"/>
  <!-- Downward Embracing Prongs (Flush x=1 and x=849) -->
  <line x1="1" y1="24" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="{h-6}" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="24" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="{h-6}" width="4" height="6" fill="{prim}"/>
  <circle cx="24" cy="18" r="4" fill="{prim}"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_clean}</text>
  <rect x="{width-180}" y="9" width="105" height="18" fill="rgba(15, 23, 38, 0.78)" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>
  <rect x="{width-68}" y="11" width="14" height="14" fill="rgba(30, 41, 59, 0.85)"/><text x="{width-64}" y="21" fill="#8892B0" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="rgba(30, 41, 59, 0.85)"/><text x="{width-47}" y="22" fill="#8892B0" font-size="10" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/><text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" class="font-mono">×</text>
</svg>"""

    else:
        # Bottom Frame
        h = height if height else 24
        if st == "tactical":
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <polygon points="1 0, {width-1} 0, {width-1} 11, {width-12} {h-2}, 12 {h-2}, 1 11" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="10 18, 16 18, 8 6, 2 6" fill="{prim}" opacity="0.6"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" letter-spacing="1.5" text-anchor="middle" class="font-mono">▲ [TACTICAL // DIRECT_CAPPING_PASS] ▲</text>
</svg>"""

        elif st == "minimal":
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}" opacity="0.35"/>
  <path d="M 4 8 L 4 18 L 14 18" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 8 L {width-4} 18 L {width-14} 18" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" letter-spacing="1.5" text-anchor="middle" class="font-mono">╚═ [TOKYO_MONOLITH // BUFFER_PASS_OK] ═╝</text>
</svg>"""

        else:
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <line x1="1" y1="0" x2="1" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="1" y1="12" x2="{width-1}" y2="12" stroke="rgba(30, 41, 59, 0.85)" stroke-width="3"/>
  <line x1="6" y1="12" x2="{width-6}" y2="12" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <rect x="{width//2 - 105}" y="4" width="210" height="16" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">╚═ [SYS: ONLINE // BUFFER_STREAM_ACTIVE] ═╝</text>
</svg>"""

    validate_svg(svg)
    return svg

# ---------------------------------------------------------------------------
# 5. CHIPS & PILLS
# ---------------------------------------------------------------------------

def generate_chip(style="cyberpunk", primary=None, accent=None,
                  chip_type="closed", text="CHIP_LABEL", width=125, height=26):
    prim, acc, bg = resolve_colors(style, primary, accent)
    text_clean = escape_xml(text)
    st = style.lower()
    ct = chip_type.lower()

    if st == "tactical":
        if ct == "decay":
            # Tactical Hazard Slash Decay (45° diagonal slashes fading out)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, 82 1, 68 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, 82 1, 68 25, 7 25, 1 19, 1 7" fill="rgba(245, 158, 11, 0.12)" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="8 13, 13 9, 13 17" fill="{prim}"/>
  <polygon points="87 1, 91 1, 77 25, 73 25" fill="{prim}" opacity="0.9"/>
  <polygon points="96 3, 99.5 3, 87.5 23, 84 23" fill="{prim}" opacity="0.65"/>
  <polygon points="104 6, 107 6, 97.5 20, 94.5 20" fill="{prim}" opacity="0.4"/>
  <polygon points="112 9, 114 9, 107 17, 105 17" fill="{prim}" opacity="0.2"/>
  <text x="44" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Tactical Targeting Reticle Pulse
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes targetPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      .laser {{ animation: targetPulse 1.2s infinite ease-in-out; }}
    </style>
  </defs>
  <polygon points="7 1, {width-8} 1, {width-2} 7, {width-2} 19, {width-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {width-8} 1, {width-2} 7, {width-2} 19, {width-8} 25, 7 25, 1 19, 1 7" fill="rgba(245, 158, 11, 0.12)" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="14" cy="13" r="4.5" fill="none" stroke="{prim}" stroke-width="1"/>
  <circle cx="14" cy="13" r="2.5" fill="{prim}" class="laser"/>
  <text x="68" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Tactical Closed 45° Chamfer
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {width-8} 1, {width-2} 7, {width-2} 19, {width-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {width-8} 1, {width-2} 7, {width-2} 19, {width-8} 25, 7 25, 1 19, 1 7" fill="rgba(245, 158, 11, 0.12)" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="60 1, 64 1, 62 4" fill="{prim}"/>
  <polygon points="60 25, 64 25, 62 22" fill="{prim}"/>
  <polygon points="10 13, 15 9, 15 17" fill="{prim}"/>
  <text x="68" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    elif st == "minimal":
        if ct == "decay":
            # Minimal Glass Micro-Stipple Dissolution
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M 88 1 L 1 1 L 1 25 L 88 25" fill="{bg}"/>
  <path d="M 88 1 L 1 1 L 1 25 L 88 25" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <line x1="88" y1="1" x2="104" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="88" y1="25" x2="104" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <g fill="{prim}">
    <circle cx="95" cy="6" r="1.2" opacity="0.8"/><circle cx="95" cy="11" r="1.2" opacity="0.8"/><circle cx="95" cy="15" r="1.2" opacity="0.8"/><circle cx="95" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="102" cy="8" r="1.1" opacity="0.55"/><circle cx="102" cy="13" r="1.1" opacity="0.55"/><circle cx="102" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="109" cy="10" r="1" opacity="0.35"/><circle cx="109" cy="16" r="1" opacity="0.35"/>
    <circle cx="116" cy="7" r="0.8" opacity="0.2"/><circle cx="116" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="47" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Minimal Glass Breathing Beacon
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes breatheBeacon {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.25; }} }}
      .breathe {{ animation: breatheBeacon 2s infinite ease-in-out; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 8 L {width-4} 4 L {width-8} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 18 L {width-4} 22 L {width-8} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="15" cy="13" r="3" fill="{prim}" class="breathe"/>
  <text x="68" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Minimal Glass Closed Hairline
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="rgba(79, 139, 255, 0.12)" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 8 L {width-4} 4 L {width-8} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 18 L {width-4} 22 L {width-8} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="15" cy="13" r="2" fill="{prim}"/>
  <text x="68" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    else:
        # Cyberpunk Chips
        if ct == "decay":
            # Pixel Matrix Dither Decay
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M 92 1 L 1 1 L 1 25 L 92 25" fill="{bg}"/>
  <path d="M 92 1 L 1 1 L 1 25 L 92 25" fill="rgba(0, 200, 215, 0.12)" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="22" width="3" height="3" fill="{prim}"/>
  <rect x="7" y="8" width="3" height="10" fill="{prim}"/>
  <g fill="{prim}">
    <rect x="94" y="3" width="3" height="3"/><rect x="94" y="9" width="3" height="3"/><rect x="94" y="15" width="3" height="3"/><rect x="94" y="20" width="3" height="3"/>
    <rect x="100" y="5" width="2" height="2"/><rect x="100" y="12" width="2" height="2"/><rect x="100" y="18" width="2" height="2"/>
    <rect x="106" y="7" width="2" height="2" opacity="0.7"/><rect x="106" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="112" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="116" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="48" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Cyberpunk Blinking Square LED Beacon
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.4s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="rgba(0, 200, 215, 0.12)" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <circle cx="14" cy="13" r="3.5" fill="{prim}" class="led"/>
  <text x="68" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Cyberpunk Closed Corner Pixels
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="rgba(0, 200, 215, 0.12)" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="8" y="8" width="4" height="10" fill="{prim}"/>
  <text x="66" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
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
