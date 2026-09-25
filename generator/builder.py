"""
Upgraded Builder Engine v2.1 with:
- Flawless XML escaping (0 Camo parser errors)
- Ultra-detailed Flagship Cyberpunk Header with 360° Animated Radar, Scanline, and Spectrum Visualizer
- 3D Pixel text rendered in front of translucent glass
- Checkered & Scattered Pixel Gutters (for table border compensation)
- Fixed corner hooks (pointing downward, no false closing shelf)
- Full suite of styles for headers, frames, rails, dividers, and chips
"""

import math
import html
import random

def escape_xml(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=True)

def build_header_terminal(title, subtitle, specs, theme, width=850, height=260):
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    bg_panel = theme.get("bg_panel", "rgba(15, 23, 38, 0.78)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")
    primary = theme.get("primary", "#00C8D7")
    secondary = theme.get("secondary", "#A855F7")
    success = theme.get("success", "#00D26A")
    warning = theme.get("warning", "#F59E0B")
    accent = theme.get("accent", "#FF0055")
    text_main = theme.get("text_main", "#F8F8F2")
    text_dim = theme.get("text_dim", "#94A3B8")

    grid_lines = []
    for x in range(0, width + 1, 20):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{primary}" stroke-width="1"/>')
    for y in range(0, height + 1, 20):
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{primary}" stroke-width="1"/>')

    teletype_svg = []
    for i, (label, val, col) in enumerate(specs):
        y_pos = 175 + i * 22
        val_clean = escape_xml(val)
        label_clean = escape_xml(label)
        teletype_svg.append(f"""
    <text x="42" y="{y_pos}" fill="{success}" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="{y_pos}" fill="{text_main}" font-size="11" class="font-mono">{label_clean}:</text>
    <text x="210" y="{y_pos}" fill="{col}" font-size="11" font-weight="bold" class="font-mono">{val_clean}</text>
        """)

    sub_clean = escape_xml(subtitle)
    theme_name_clean = escape_xml(theme.get("name", "CYBERPUNK").upper())

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes ledFlicker {{
        0%, 100% {{ fill: {success}; }}
        50% {{ fill: #005511; }}
      }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.35; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY({height}px); opacity: 0; }}
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

  <!-- 1. TRANSLUCENT GLASS BACKGROUND (True Alpha Blending) -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="{bg_glass}"/>

  <!-- 2. MATRIX RETRO GRID PATTERN -->
  <g opacity="0.08">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{primary}" stroke-width="2" class="scan-line"/>

  <!-- 4. OUTER CHASSIS / BORDER -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" fill="none" stroke="{border_slate}" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{height-24}" fill="none" stroke="{primary}" stroke-width="2" opacity="0.85"/>

  <!-- CORNER ACCENT BRACKETS -->
  <rect x="6" y="6" width="24" height="6" fill="{primary}"/>
  <rect x="6" y="6" width="6" height="24" fill="{primary}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{primary}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{primary}"/>
  <rect x="6" y="{height-12}" width="24" height="6" fill="{primary}"/>
  <rect x="6" y="{height-30}" width="6" height="24" fill="{primary}"/>
  <rect x="{width-30}" y="{height-12}" width="24" height="6" fill="{primary}"/>
  <rect x="{width-12}" y="{height-30}" width="6" height="24" fill="{primary}"/>

  <!-- TOP CONSOLE STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="{bg_panel}"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="{primary}" stroke-width="1.5" opacity="0.6"/>

  <circle cx="28" cy="25" r="4" fill="{success}" class="status-led"/>
  <text x="38" y="29" fill="{success}" font-size="11" font-weight="bold" class="font-mono">SYS: ONLINE // 0x00</text>

  <rect x="175" y="19" width="2" height="12" fill="{border_slate}"/>
  <text x="188" y="29" fill="{text_dim}" font-size="11" class="font-mono">HUD: TRANSLUCENT_GLASS</text>

  <rect x="380" y="19" width="2" height="12" fill="{border_slate}"/>
  <text x="393" y="29" fill="{text_dim}" font-size="11" class="font-mono">MODE: CYBERPUNK_TERMINAL</text>

  <rect x="600" y="19" width="2" height="12" fill="{border_slate}"/>
  <text x="613" y="29" fill="{warning}" font-size="11" font-weight="bold" class="font-mono">{theme_name_clean}</text>

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="{border_slate}"/>
  <text x="{width-80}" y="28" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="{border_slate}"/>
  <text x="{width-59}" y="29" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="{accent}"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- PLACEHOLDER FOR 3D PIXEL TITLE (Rendered in front of background!) -->
  <!-- INSERT_PIXEL_TEXT -->

  <!-- SUB-BADGE: ROLE & SPECIALIZATION -->
  <g transform="translate(42, 126)">
    <rect x="0" y="0" width="440" height="26" fill="{bg_panel}" stroke="{secondary}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{secondary}"/>
    <rect x="436" y="-2" width="6" height="6" fill="{secondary}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{secondary}"/>
    <rect x="436" y="22" width="6" height="6" fill="{secondary}"/>
    <text x="12" y="18" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ {sub_clean}
    </text>
  </g>

  <!-- TELETYPE TELEMETRY LINES -->
  <g>
    {''.join(teletype_svg)}
    <rect x="500" y="210" width="8" height="12" fill="{primary}" class="cursor-blink"/>
  </g>

  <!-- MINI SPECTRUM EQUALIZER -->
  <g transform="translate(525, 0)">
    <rect x="0" y="198" width="5" height="6" fill="{primary}" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="{secondary}" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="{accent}" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="{warning}" class="w4"/>
  </g>

  <!-- RIGHT SIDE: RETRO SCI-FI WORKBENCH / MONITOR HUD -->
  <g transform="translate(630, 60)">
    <rect x="0" y="0" width="170" height="140" fill="{bg_panel}" stroke="{border_slate}" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{primary}" stroke-width="1" opacity="0.6"/>

    <!-- Concentric Range Rings -->
    <circle cx="85" cy="70" r="50" fill="none" stroke="{primary}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{primary}" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{primary}" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{primary}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{primary}" stroke-width="1" opacity="0.3"/>

    <!-- 360° Rotating Radar Beam (SVG Native animateTransform - 100% Reliable!) -->
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="{success}" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="{warning}"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>

    <!-- Pulsing Radar Target Blips -->
    <circle cx="110" cy="50" r="3" fill="{accent}">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="65" cy="85" r="2.5" fill="{success}">
      <animate attributeName="opacity" values="0.1;0.9;0.1" dur="3s" repeatCount="indefinite"/>
    </circle>

    <!-- Radar Telemetry Label -->
    <text x="85" y="132" fill="{success}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">RADAR: ACTIVE (360°)</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{height-20}" x2="{width-14}" y2="{height-20}" stroke="{border_slate}" stroke-width="1"/>
  <text x="24" y="{height-8}" fill="{text_dim}" font-size="9" class="font-mono">HUD_ARCH: TRANSLUCENT_V2 // GLASS_RATIO: 0.82 // DUAL_THEME: PASS</text>
  <text x="{width-24}" y="{height-8}" fill="{primary}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">READY // ID: 0xDEADBEEF</text>
</svg>"""
    return svg

def build_header_tactical(title, subtitle, specs, theme, width=850, height=220):
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    bg_panel = theme.get("bg_panel", "rgba(15, 23, 38, 0.78)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")
    primary = theme.get("primary", "#00C8D7")
    secondary = theme.get("secondary", "#A855F7")
    warning = theme.get("warning", "#F59E0B")
    accent = theme.get("accent", "#FF0055")
    text_main = theme.get("text_main", "#F8F8F2")

    sub_clean = escape_xml(subtitle)
    s0 = escape_xml(specs[0][1]) if len(specs) > 0 else "ALPHA // HAZARD VERIFIED"
    s1 = escape_xml(specs[1][1]) if len(specs) > 1 else "LASER SCAN ACTIVE"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
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
  <polygon points="20 4, {width-20} 4, {width-4} 20, {width-4} {height-20}, {width-20} {height-4}, 20 {height-4}, 4 {height-20}, 4 20"
           fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  
  <polygon points="24 10, {width-24} 10, {width-10} 24, {width-10} {height-24}, {width-24} {height-10}, 24 {height-10}, 10 {height-24}, 10 24"
           fill="none" stroke="{warning}" stroke-width="1.5" opacity="0.75"/>

  <!-- HAZARD STRIPES TOP-LEFT -->
  <g fill="{warning}" opacity="0.6">
    <polygon points="30 14, 38 14, 26 26, 18 26"/>
    <polygon points="44 14, 52 14, 40 26, 32 26"/>
    <polygon points="58 14, 66 14, 54 26, 46 26"/>
  </g>

  <!-- TACTICAL TITLE BAR -->
  <text x="80" y="24" fill="{warning}" font-size="11" font-weight="bold" letter-spacing="1.5" class="font-mono">
    // TACTICAL.HUD // SEC_CLASS_ALPHA // SYSTEM_READY
  </text>

  <!-- PLACEHOLDER FOR 3D PIXEL TITLE -->
  <!-- INSERT_PIXEL_TEXT -->

  <!-- SUBTITLE -->
  <rect x="42" y="112" width="380" height="24" fill="{bg_panel}" stroke="{secondary}" stroke-width="1"/>
  <text x="54" y="128" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">
    [TARGET] {sub_clean}
  </text>

  <!-- SPECS TELEMETRY -->
  <text x="42" y="162" fill="{primary}" font-size="11" class="font-mono">&gt; ARCH: {s0}</text>
  <text x="42" y="184" fill="{primary}" font-size="11" class="font-mono">&gt; PROTOCOL: {s1}</text>
  <text x="42" y="204" fill="{warning}" font-size="11" font-weight="bold" class="font-mono">&gt; STATUS: [ONLINE // LOCKED]</text>

  <!-- RIGHT SIDE: TARGET LOCK-ON CROSSHAIR RETICLE -->
  <g class="reticle-pulse">
    <circle cx="750" cy="105" r="45" fill="none" stroke="{warning}" stroke-width="1.5" stroke-dasharray="8,4"/>
    <circle cx="750" cy="105" r="24" fill="none" stroke="{accent}" stroke-width="1.5"/>
    <circle cx="750" cy="105" r="4" fill="{accent}"/>
    <line x1="750" y1="50" x2="750" y2="75" stroke="{warning}" stroke-width="2"/>
    <line x1="750" y1="135" x2="750" y2="160" stroke="{warning}" stroke-width="2"/>
    <line x1="695" y1="105" x2="720" y2="105" stroke="{warning}" stroke-width="2"/>
    <line x1="780" y1="105" x2="805" y2="105" stroke="{warning}" stroke-width="2"/>
    <path d="M 725 80 L 720 80 L 720 85" fill="none" stroke="{warning}" stroke-width="2"/>
    <path d="M 775 80 L 780 80 L 780 85" fill="none" stroke="{warning}" stroke-width="2"/>
    <path d="M 725 130 L 720 130 L 720 125" fill="none" stroke="{warning}" stroke-width="2"/>
    <path d="M 775 130 L 780 130 L 780 125" fill="none" stroke="{warning}" stroke-width="2"/>
    <text x="750" y="168" fill="{warning}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">TARGET LOCK</text>
  </g>

  <!-- SWEEPING TARGET LASER -->
  <g class="laser-scan">
    <line x1="50" y1="10" x2="50" y2="{height-10}" stroke="{accent}" stroke-width="1.5" opacity="0.8"/>
    <circle cx="50" cy="20" r="3" fill="{accent}"/>
    <circle cx="50" cy="{height-20}" r="3" fill="{accent}"/>
  </g>
</svg>"""
    return svg

def build_header_minimal(title, subtitle, specs, theme, width=850, height=135):
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    bg_panel = theme.get("bg_panel", "rgba(15, 23, 38, 0.78)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")
    primary = theme.get("primary", "#00C8D7")
    secondary = theme.get("secondary", "#A855F7")
    success = theme.get("success", "#00D26A")
    warning = theme.get("warning", "#F59E0B")
    accent = theme.get("accent", "#FF0055")
    text_main = theme.get("text_main", "#F8F8F2")

    sub_clean = escape_xml(subtitle)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
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
  <rect x="4" y="4" width="{width-8}" height="{height-8}" fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  <rect x="8" y="8" width="{width-16}" height="{height-16}" fill="none" stroke="{primary}" stroke-width="1.5" class="breath"/>

  <!-- CORNER PIXEL ACCENTS -->
  <rect x="4" y="4" width="8" height="3" fill="{primary}"/>
  <rect x="4" y="4" width="3" height="8" fill="{primary}"/>
  <rect x="{width-12}" y="4" width="8" height="3" fill="{primary}"/>
  <rect x="{width-7}" y="4" width="3" height="8" fill="{primary}"/>
  <rect x="4" y="{height-7}" width="8" height="3" fill="{primary}"/>
  <rect x="4" y="{height-12}" width="3" height="8" fill="{primary}"/>
  <rect x="{width-12}" y="{height-7}" width="8" height="3" fill="{primary}"/>
  <rect x="{width-7}" y="{height-12}" width="3" height="8" fill="{primary}"/>

  <!-- PLACEHOLDER FOR 3D PIXEL TITLE -->
  <!-- INSERT_PIXEL_TEXT -->

  <!-- SUBTITLE CHIP -->
  <g transform="translate(42, 85)">
    <rect x="0" y="0" width="380" height="22" fill="{bg_panel}" stroke="{secondary}" stroke-width="1"/>
    <text x="12" y="15" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">⚡ {sub_clean}</text>
  </g>

  <!-- EQUALIZER BARS (RIGHT SIDE) -->
  <g transform="translate({width-120}, 45)">
    <rect x="0" y="28" width="8" height="12" fill="{primary}" class="eq1"/>
    <rect x="14" y="12" width="8" height="28" fill="{secondary}" class="eq2"/>
    <rect x="28" y="22" width="8" height="18" fill="{accent}" class="eq3"/>
    <rect x="42" y="6" width="8" height="34" fill="{warning}" class="eq4"/>
    <rect x="56" y="18" width="8" height="22" fill="{success}" class="eq5"/>
    <text x="32" y="52" fill="{primary}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">LIVE_AUDIO</text>
  </g>
</svg>"""
    return svg

def build_header(title, subtitle, specs, theme, width=850, height=None, style="terminal"):
    if style == "tactical":
        h = height if height else 220
        return build_header_tactical(title, subtitle, specs, theme, width, h)
    elif style == "minimal":
        h = height if height else 135
        return build_header_minimal(title, subtitle, specs, theme, width, h)
    else:
        h = height if height else 260
        return build_header_terminal(title, subtitle, specs, theme, width, h)

# ----------------------------------------------------
# CHECKERED & SCATTERED PIXEL GUTTERS
# ----------------------------------------------------

def build_gutter_rail(height=200, color="#00C8D7", theme=None, side="left", width=32):
    bg_glass = "rgba(10, 14, 23, 0.82)" if theme is None else theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    border_slate = "rgba(30, 41, 59, 0.85)" if theme is None else theme.get("border_slate", "rgba(30, 41, 59, 0.85)")
    accent = "#FF0055" if theme is None else theme.get("accent", "#FF0055")
    warning = "#F59E0B" if theme is None else theme.get("warning", "#F59E0B")

    rng = random.Random(42 if side == "left" else 137)
    elements = []

    # 1. Broken vertical bus line
    curr_y = 6
    while curr_y < height - 10:
        seg_len = rng.choice([8, 14, 22, 6])
        gap = rng.choice([6, 10, 14, 4])
        line_x = 6 if side == "left" else width - 6
        elements.append(f'<line x1="{line_x}" y1="{curr_y}" x2="{line_x}" y2="{curr_y + seg_len}" stroke="{color}" stroke-width="1.5" opacity="0.75"/>')
        curr_y += seg_len + gap

    # 2. Checkered blocks ("шахматка")
    num_blocks = max(height // 60, 2)
    for b in range(num_blocks):
        block_y = 15 + b * (height // num_blocks) + rng.randint(-5, 5)
        if block_y + 20 >= height:
            continue
        start_x = 10 if side == "left" else 8
        for row in range(4):
            for col in range(4):
                if (row + col) % 2 == 0:
                    px = start_x + col * 3
                    py = block_y + row * 3
                    elements.append(f'<rect x="{px}" y="{py}" width="2.5" height="2.5" fill="{color}" opacity="0.6"/>')

    # 3. Scattered pixel dust ("раскиданные пиксели")
    for _ in range(height // 8):
        px = rng.randint(4, width - 6)
        py = rng.randint(6, height - 6)
        sz = rng.choice([1.5, 2, 2.5])
        op = rng.choice([0.3, 0.5, 0.8, 1.0])
        col = rng.choice([color, color, color, accent if rng.random() > 0.85 else warning])
        elements.append(f'<rect x="{px}" y="{py}" width="{sz}" height="{sz}" fill="{col}" opacity="{op:.2f}"/>')

    # 4. Telemetry tick marks
    ticks_y = [20, height // 3, (2 * height) // 3, height - 25]
    for ty in ticks_y:
        tx = 12 if side == "left" else 8
        elements.append(f'<rect x="{tx}" y="{ty}" width="6" height="2" fill="{warning}" opacity="0.85"/>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes ditherPulse {{
        0%, 100% {{ opacity: 0.35; }}
        50% {{ opacity: 0.95; }}
      }}
      .pulse-px {{ animation: ditherPulse 2s infinite ease-in-out; }}
    </style>
  </defs>

  <rect width="{width}" height="{height}" fill="{bg_glass}"/>
  {''.join(elements)}
</svg>"""
    return svg

# ----------------------------------------------------
# FRAME TOP & BOTTOM
# ----------------------------------------------------

def build_frame_top(title, tag, color, theme, width=850, height=38, style="brackets"):
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    bg_panel = theme.get("bg_panel", "rgba(15, 23, 38, 0.78)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    title_clean = escape_xml(title)
    tag_clean = escape_xml(tag)

    if style == "brackets":
        teeth_markup = f"""
  <!-- DOWNWARD EMBRACING PRONGS (OPENING INTO CONTENT) -->
  <line x1="6" y1="24" x2="6" y2="38" stroke="{color}" stroke-width="2.5"/>
  <rect x="4" y="32" width="5" height="6" fill="{color}"/>
  <line x1="{width-6}" y1="24" x2="{width-6}" y2="38" stroke="{color}" stroke-width="2.5"/>
  <rect x="{width-9}" y="32" width="5" height="6" fill="{color}"/>
        """
        chassis = f"""
  <rect x="6" y="4" width="{width-12}" height="28" fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  <rect x="8" y="6" width="{width-16}" height="24" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.85"/>
  <rect x="6" y="4" width="5" height="5" fill="{color}"/>
  <rect x="{width-11}" y="4" width="5" height="5" fill="{color}"/>
        """
    elif style == "chamfer":
        teeth_markup = f"""
  <path d="M 4 28 L 4 38 L 10 38" fill="none" stroke="{color}" stroke-width="2"/>
  <path d="M {width-4} 28 L {width-4} 38 L {width-10} 38" fill="none" stroke="{color}" stroke-width="2"/>
        """
        chassis = f"""
  <polygon points="14 4, {width-14} 4, {width-4} 14, {width-4} 32, 4 32, 4 14"
           fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  <polygon points="16 7, {width-16} 7, {width-7} 16, {width-7} 29, 7 29, 7 16"
           fill="none" stroke="{color}" stroke-width="1.5" opacity="0.85"/>
  <line x1="30" y1="32" x2="{width-30}" y2="32" stroke="{color}" stroke-width="1" stroke-dasharray="6,4" opacity="0.6"/>
        """
    else:  # enclosure
        teeth_markup = f"""
  <line x1="6" y1="26" x2="6" y2="38" stroke="{color}" stroke-width="3"/>
  <line x1="{width-6}" y1="26" x2="{width-6}" y2="38" stroke="{color}" stroke-width="3"/>
        """
        chassis = f"""
  <rect x="6" y="4" width="{width-12}" height="28" fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  <rect x="8" y="6" width="{width-16}" height="24" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.85"/>
  <rect x="6" y="4" width="6" height="6" fill="{color}"/>
  <rect x="{width-12}" y="4" width="6" height="6" fill="{color}"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {color}; }} 50% {{ fill: #1E293B; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>

  {chassis}
  {teeth_markup}

  <!-- Status LED -->
  <circle cx="24" cy="18" r="4" fill="{color}" class="led"/>

  <!-- Title Text -->
  <text x="36" y="22" fill="{color}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">
    {title_clean}
  </text>

  <!-- Right Status Tag -->
  <rect x="{width-180}" y="9" width="105" height="18" fill="{bg_panel}" stroke="{color}" stroke-width="1"/>
  <text x="{width-127}" y="22" fill="{color}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">[{tag_clean}]</text>

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-68}" y="11" width="14" height="14" fill="{border_slate}"/>
  <text x="{width-64}" y="21" fill="#8892B0" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{border_slate}"/>
  <text x="{width-47}" y="22" fill="#8892B0" font-size="10" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/>
  <text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" font-weight="bold" class="font-mono">×</text>
</svg>"""
    return svg

def build_frame_bottom(tag, color, theme, width=850, height=24, style="brackets"):
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")
    tag_clean = escape_xml(tag)

    if style == "brackets":
        teeth_markup = f"""
  <line x1="6" y1="0" x2="6" y2="12" stroke="{color}" stroke-width="2.5"/>
  <rect x="4" y="0" width="5" height="5" fill="{color}"/>
  <line x1="{width-6}" y1="0" x2="{width-6}" y2="12" stroke="{color}" stroke-width="2.5"/>
  <rect x="{width-9}" y="0" width="5" height="5" fill="{color}"/>
        """
        boundary = f"""
  <line x1="6" y1="12" x2="{width-6}" y2="12" stroke="{border_slate}" stroke-width="3"/>
  <line x1="12" y1="12" x2="{width-12}" y2="12" stroke="{color}" stroke-width="1.5" opacity="0.85"/>
  <path d="M 6 12 L 6 20 L 20 20" fill="none" stroke="{color}" stroke-width="1.5"/>
  <rect x="6" y="17" width="4" height="4" fill="{color}"/>
  <path d="M {width-6} 12 L {width-6} 20 L {width-20} 20" fill="none" stroke="{color}" stroke-width="1.5"/>
  <rect x="{width-10}" y="17" width="4" height="4" fill="{color}"/>
        """
    elif style == "chamfer":
        teeth_markup = f"""
  <path d="M 4 0 L 4 10 L 10 10" fill="none" stroke="{color}" stroke-width="2"/>
  <path d="M {width-4} 0 L {width-4} 10 L {width-10} 10" fill="none" stroke="{color}" stroke-width="2"/>
        """
        boundary = f"""
  <polygon points="4 10, {width-4} 10, {width-14} 20, 14 20" fill="{bg_glass}" stroke="{border_slate}" stroke-width="1.5"/>
  <line x1="14" y1="20" x2="{width-14}" y2="20" stroke="{color}" stroke-width="2"/>
        """
    else:  # enclosure
        teeth_markup = f"""
  <line x1="6" y1="0" x2="6" y2="10" stroke="{color}" stroke-width="3"/>
  <line x1="{width-6}" y1="0" x2="{width-6}" y2="10" stroke="{color}" stroke-width="3"/>
        """
        boundary = f"""
  <rect x="6" y="8" width="{width-12}" height="14" fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  <line x1="8" y1="10" x2="{width-8}" y2="10" stroke="{color}" stroke-width="1.5" opacity="0.85"/>
  <rect x="6" y="16" width="6" height="6" fill="{color}"/>
  <rect x="{width-12}" y="16" width="6" height="6" fill="{color}"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>

  {teeth_markup}
  {boundary}

  <!-- Center Status Buffer Readout -->
  <rect x="{width//2 - 105}" y="4" width="210" height="16" fill="{bg_glass}" stroke="{color}" stroke-width="1"/>
  <text x="{width//2}" y="15" fill="{color}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">
    ╚═ [{tag_clean}] ═╝
  </text>
</svg>"""
    return svg

# ----------------------------------------------------
# SIDE RAILS (Ladder, Laser, Matrix)
# ----------------------------------------------------

def build_side_rail(height, color, theme, side="left", width=14, style="ladder"):
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.82)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    line_x = 6 if side == "left" else width - 6
    inner_x = width - 2 if side == "left" else 2

    elements = []
    style_def = ""

    if style == "ladder":
        style_def = f"""
      @keyframes rungGlow {{
        0%, 100% {{ opacity: 0.35; }}
        50% {{ opacity: 1; fill: #FFFFFF; }}
      }}
      .rung {{ animation: rungGlow 2.4s infinite ease-in-out; }}
        """
        for i, y in enumerate(range(8, height - 8, 14)):
            delay = (i % 6) * 0.3
            elements.append(f'<rect x="{line_x - 2}" y="{y}" width="5" height="5" fill="{color}" class="rung" style="animation-delay: {delay:.1f}s;"/>')

    elif style == "laser":
        for y in range(10, height - 10, 20):
            elements.append(f'<line x1="{line_x - 3}" y1="{y}" x2="{line_x + 3}" y2="{y}" stroke="{color}" stroke-width="1"/>')

    else:  # matrix
        for i, y in enumerate(range(6, height - 6, 10)):
            op = 0.3 + (i % 4) * 0.2
            elements.append(f'<rect x="{line_x - 1}" y="{y}" width="3" height="3" fill="{color}" opacity="{op:.2f}"/>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {style_def}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="{bg_glass}"/>
  <line x1="{line_x}" y1="0" x2="{line_x}" y2="{height}" stroke="{color}" stroke-width="2"/>
  <line x1="{inner_x}" y1="0" x2="{inner_x}" y2="{height}" stroke="{border_slate}" stroke-width="1"/>
  {''.join(elements)}
</svg>"""
    return svg

# ----------------------------------------------------
# DIVIDERS
# ----------------------------------------------------

def build_pcb_divider(theme, width=850, height=30):
    primary = theme.get("primary", "#00C8D7")
    secondary = theme.get("secondary", "#A855F7")
    success = theme.get("success", "#00D26A")
    warning = theme.get("warning", "#F59E0B")
    accent = theme.get("accent", "#FF0055")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes traceFlow {{
        0% {{ transform: translateX(-80px); }}
        100% {{ transform: translateX({width + 80}px); }}
      }}
      .flow-packet {{ animation: traceFlow 3.5s linear infinite; }}
    </style>
  </defs>

  <line x1="20" y1="15" x2="{width-20}" y2="15" stroke="{border_slate}" stroke-width="4"/>
  <line x1="20" y1="15" x2="{width-20}" y2="15" stroke="{primary}" stroke-width="2" opacity="0.7"/>

  <path d="M 50 7 L 150 7 L 160 15 L 300 15 L 310 7 L 500 7 L 510 15 L 720 15 L 730 7 L 800 7" fill="none" stroke="{secondary}" stroke-width="1.5" opacity="0.6"/>
  <path d="M 40 23 L 110 23 L 120 15 L 240 15 L 250 23 L 440 23 L 450 15 L 650 15 L 660 23 L 810 23" fill="none" stroke="{success}" stroke-width="1.5" opacity="0.5"/>

  <rect x="20" y="12" width="6" height="6" fill="{warning}"/>
  <rect x="50" y="4" width="6" height="6" fill="{primary}"/>
  <rect x="150" y="4" width="6" height="6" fill="{secondary}"/>
  <rect x="{width-20}" y="12" width="6" height="6" fill="{warning}"/>

  <g transform="translate({width//2}, 15)">
    <rect x="-14" y="-10" width="28" height="20" fill="rgba(10, 14, 23, 0.9)" stroke="{primary}" stroke-width="1.5"/>
    <circle cx="0" cy="0" r="3" fill="{warning}"/>
  </g>

  <g class="flow-packet">
    <rect x="0" y="13" width="14" height="4" fill="{warning}"/>
    <rect x="14" y="14" width="8" height="2" fill="#FFFFFF"/>
    <rect x="-8" y="14" width="8" height="2" fill="{accent}"/>
  </g>
</svg>"""
    return svg

def build_laser_divider(theme, width=850, height=20, color=None):
    if color is None:
        color = theme.get("primary", "#00C8D7")
    accent = theme.get("accent", "#FF0055")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes laserPulse {{ 0%, 100% {{ opacity: 0.9; }} 50% {{ opacity: 0.4; }} }}
      .pulse-laser {{ animation: laserPulse 2s infinite ease-in-out; }}
    </style>
  </defs>

  <line x1="20" y1="10" x2="{width-20}" y2="10" stroke="{color}" stroke-width="1" opacity="0.4"/>
  <line x1="60" y1="10" x2="{width-60}" y2="10" stroke="{color}" stroke-width="2" class="pulse-laser"/>
  <line x1="{width//2 - 100}" y1="10" x2="{width//2 + 100}" y2="10" stroke="#FFFFFF" stroke-width="2.5" class="pulse-laser"/>
  <polygon points="{width//2} 4, {width//2 + 6} 10, {width//2} 16, {width//2 - 6} 10" fill="{accent}"/>
</svg>"""
    return svg

# ----------------------------------------------------
# CHIPS
# ----------------------------------------------------

def build_chip(text, color, theme, style="closed", width=None, height=26):
    bg_chip = theme.get("bg_chip", "rgba(0, 200, 215, 0.12)")
    bg_glass_base = "rgba(10, 14, 23, 0.85)"
    stroke_w = 1.5

    text_clean = escape_xml(text)

    if width is None:
        width = max(len(text) * 9 + 36, 95)

    style_tag = ""

    if style == "closed":
        body_markup = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_glass_base}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="1" y="1" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{color}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{color}"/>
        """
        text_x = width // 2

    elif style == "chamfer":
        body_markup = f"""
  <polygon points="6 1, {width-6} 1, {width-1} 6, {width-1} {height-6}, {width-6} {height-1}, 6 {height-1}, 1 {height-6}, 1 6" fill="{bg_glass_base}"/>
  <polygon points="6 1, {width-6} 1, {width-1} 6, {width-1} {height-6}, {width-6} {height-1}, 6 {height-1}, 1 {height-6}, 1 6" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
        """
        text_x = width // 2

    elif style == "decay_right":
        width_body = width - 20
        body_markup = f"""
  <path d="M {width_body} 1 L 1 1 L 1 {height-1} L {width_body} {height-1}" fill="{bg_glass_base}"/>
  <path d="M {width_body} 1 L 1 1 L 1 {height-1} L {width_body} {height-1}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="1" y="1" width="3" height="3" fill="{color}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{color}"/>

  <g fill="{color}">
    <rect x="{width_body + 2}" y="3" width="3" height="3"/>
    <rect x="{width_body + 2}" y="9" width="3" height="3"/>
    <rect x="{width_body + 2}" y="15" width="3" height="3"/>
    <rect x="{width_body + 2}" y="20" width="3" height="3"/>
    <rect x="{width_body + 7}" y="5" width="2" height="2"/>
    <rect x="{width_body + 7}" y="12" width="2" height="2"/>
    <rect x="{width_body + 7}" y="18" width="2" height="2"/>
    <rect x="{width_body + 12}" y="7" width="2" height="2" opacity="0.6"/>
    <rect x="{width_body + 15}" y="14" width="2" height="2" opacity="0.4"/>
    <rect x="{width_body + 18}" y="10" width="1" height="1" opacity="0.3"/>
  </g>
        """
        text_x = (width_body + 4) // 2

    elif style == "decay_left":
        left_offset = 20
        body_markup = f"""
  <path d="M {left_offset} 1 L {width-1} 1 L {width-1} {height-1} L {left_offset} {height-1}" fill="{bg_glass_base}"/>
  <path d="M {left_offset} 1 L {width-1} 1 L {width-1} {height-1} L {left_offset} {height-1}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{color}"/>

  <g fill="{color}">
    <rect x="{left_offset - 5}" y="3" width="3" height="3"/>
    <rect x="{left_offset - 5}" y="9" width="3" height="3"/>
    <rect x="{left_offset - 5}" y="15" width="3" height="3"/>
    <rect x="{left_offset - 5}" y="20" width="3" height="3"/>
    <rect x="{left_offset - 10}" y="5" width="2" height="2"/>
    <rect x="{left_offset - 10}" y="12" width="2" height="2"/>
    <rect x="{left_offset - 10}" y="18" width="2" height="2"/>
    <rect x="{left_offset - 14}" y="7" width="2" height="2" opacity="0.6"/>
    <rect x="{left_offset - 17}" y="14" width="2" height="2" opacity="0.4"/>
    <rect x="{left_offset - 19}" y="10" width="1" height="1" opacity="0.3"/>
  </g>
        """
        text_x = left_offset + (width - left_offset) // 2

    elif style == "pulse":
        style_tag = f"""
      @keyframes pulseDot {{ 0%, 100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.3; transform: scale(0.8); }} }}
      .beacon {{ animation: pulseDot 1.4s infinite ease-in-out; transform-origin: 12px 13px; }}
        """
        body_markup = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_glass_base}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="1" y="1" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{color}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{color}"/>
  <circle cx="12" cy="13" r="3.5" fill="{color}" class="beacon"/>
        """
        text_x = width // 2 + 6

    else:
        body_markup = f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_glass_base}" stroke="{color}"/>'
        text_x = width // 2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      {style_tag}
    </style>
  </defs>
  {body_markup}
  <text x="{text_x}" y="17" fill="{color}" text-anchor="middle" class="chip-text">
    {text_clean}
  </text>
</svg>"""
    return svg
