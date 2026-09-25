"""
SVG Builder module for Pixel Readme Kit
Generates:
- Translucent Glass Headers with 3D typography
- Open HUD Cyber Brackets (Top & Bottom)
- Side Rails for Full Box Enclosures
- Chips with 3 styles: Closed, Decay-Right, Decay-Left
"""

import math

def build_header(title, subtitle, specs, theme, width=850, height=260):
    """
    Builds a translucent glass HUD banner with 3D pixel typography and animated oscilloscopes.
    """
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.75)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")
    primary = theme.get("primary", "#00F0FF")
    secondary = theme.get("secondary", "#BD93F9")
    success = theme.get("success", "#39FF14")
    warning = theme.get("warning", "#FFE600")
    accent = theme.get("accent", "#FF0055")
    text_main = theme.get("text_main", "#F8F8F2")
    text_dim = theme.get("text_dim", "#8892B0")

    # Generate grid lines with opacity
    grid_lines = []
    for x in range(0, width + 1, 20):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{primary}" stroke-width="1"/>')
    for y in range(0, height + 1, 20):
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{primary}" stroke-width="1"/>')

    teletype_svg = []
    for i, (label, val, col) in enumerate(specs):
        y_pos = 175 + i * 22
        teletype_svg.append(f'''
    <text x="42" y="{y_pos}" fill="{success}" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="{y_pos}" fill="{text_main}" font-size="11" class="font-mono">{label}:</text>
    <text x="210" y="{y_pos}" fill="{col}" font-size="11" font-weight="bold" class="font-mono">{val}</text>
        ''')

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
      @keyframes osciWave {{
        0% {{ d: path("M 660 102 Q 670 95 680 102 T 700 102 T 720 102"); }}
        50% {{ d: path("M 660 102 Q 670 108 680 102 T 700 96 T 720 102"); }}
        100% {{ d: path("M 660 102 Q 670 95 680 102 T 700 102 T 720 102"); }}
      }}
      .font-mono {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      }}
      .cursor-blink {{
        animation: blink 1s infinite steps(1);
      }}
      .status-led {{
        animation: ledFlicker 1.8s infinite steps(1);
      }}
    </style>
  </defs>

  <!-- TRANSLUCENT GLASS BACKGROUND -->
  <rect width="{width}" height="{height}" fill="{bg_glass}"/>

  <!-- SUBTLE COGNITIVE GRID -->
  <g opacity="0.08">
    {' '.join(grid_lines)}
  </g>

  <!-- OUTER PIXEL BORDER -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" fill="none" stroke="{border_slate}" stroke-width="4"/>
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
  <rect x="14" y="14" width="{width-28}" height="22" fill="{theme['bg_panel']}"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="{primary}" stroke-width="1.5" opacity="0.6"/>

  <circle cx="28" cy="25" r="4" fill="{success}" class="status-led"/>
  <text x="38" y="29" fill="{success}" font-size="11" font-weight="bold" class="font-mono">SYS: ONLINE // 0x00</text>

  <rect x="175" y="19" width="2" height="12" fill="{border_slate}"/>
  <text x="188" y="29" fill="{text_dim}" font-size="11" class="font-mono">HUD: TRANSLUCENT_GLASS</text>

  <rect x="380" y="19" width="2" height="12" fill="{border_slate}"/>
  <text x="393" y="29" fill="{text_dim}" font-size="11" class="font-mono">MODE: OPEN_BRACKETS</text>

  <rect x="600" y="19" width="2" height="12" fill="{border_slate}"/>
  <text x="613" y="29" fill="{warning}" font-size="11" font-weight="bold" class="font-mono">{theme['name'].upper()}</text>

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="{border_slate}"/>
  <text x="{width-80}" y="28" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="{border_slate}"/>
  <text x="{width-59}" y="29" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="{accent}"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- SUB-BADGE: ROLE & SPECIALIZATION -->
  <g transform="translate(42, 126)">
    <rect x="0" y="0" width="440" height="26" fill="{theme['bg_panel']}" stroke="{secondary}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{secondary}"/>
    <rect x="436" y="-2" width="6" height="6" fill="{secondary}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{secondary}"/>
    <rect x="436" y="22" width="6" height="6" fill="{secondary}"/>
    <text x="12" y="18" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ {subtitle}
    </text>
  </g>

  <!-- TELETYPE TELEMETRY LINES -->
  <g>
    {''.join(teletype_svg)}
    <rect x="490" y="210" width="8" height="12" fill="{primary}" class="cursor-blink"/>
  </g>

  <!-- RIGHT SIDE: RETRO SCI-FI WORKBENCH / MONITOR HUD -->
  <g transform="translate(630, 60)">
    <rect x="0" y="0" width="170" height="140" fill="{theme['bg_panel']}" stroke="{border_slate}" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{primary}" stroke-width="1" opacity="0.6"/>

    <!-- Mini Radar / Scope Circle -->
    <circle cx="85" cy="70" r="50" fill="none" stroke="{primary}" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>
    <circle cx="85" cy="70" r="30" fill="none" stroke="{primary}" stroke-width="1" opacity="0.7"/>
    <circle cx="85" cy="70" r="4" fill="{warning}"/>

    <line x1="85" y1="15" x2="85" y2="125" stroke="{primary}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{primary}" stroke-width="1" opacity="0.3"/>

    <!-- Oscilloscope sine wave -->
    <path d="M 40 70 Q 55 50 70 70 T 100 70 T 130 70" fill="none" stroke="{success}" stroke-width="2">
      <animate attributeName="d" 
        values="M 40 70 Q 55 50 70 70 T 100 70 T 130 70;
                M 40 70 Q 55 90 70 70 T 100 50 T 130 70;
                M 40 70 Q 55 50 70 70 T 100 70 T 130 70" 
        dur="1.5s" repeatCount="indefinite"/>
    </path>

    <!-- Corner rivets -->
    <rect x="4" y="4" width="4" height="4" fill="{primary}"/>
    <rect x="162" y="4" width="4" height="4" fill="{primary}"/>
    <rect x="4" y="132" width="4" height="4" fill="{primary}"/>
    <rect x="162" y="132" width="4" height="4" fill="{primary}"/>

    <text x="85" y="128" fill="{primary}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">
      TELEMETRY // ACTIVE
    </text>
  </g>

  <!-- BOTTOM ACCENT LINE -->
  <rect x="14" y="{height-14}" width="{width-28}" height="4" fill="{primary}" opacity="0.4"/>
</svg>"""
    return svg

def build_frame_top(title, tag, color, theme, width=850, height=38, open_bracket=True):
    """
    Builds a top window frame.
    If open_bracket=True, downward vertical guide teeth extend to embrace the markdown text.
    """
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.75)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    teeth_markup = ""
    if open_bracket:
        # Downward vertical teeth (8px width, 12px depth) on left and right borders
        teeth_markup = f"""
  <!-- DOWNWARD EMBRACING BRACKET ACCENTS -->
  <path d="M 6 30 L 6 38 L 12 38" fill="none" stroke="{color}" stroke-width="2"/>
  <rect x="6" y="34" width="3" height="4" fill="{color}"/>
  <path d="M {width-6} 30 L {width-6} 38 L {width-12} 38" fill="none" stroke="{color}" stroke-width="2"/>
  <rect x="{width-9}" y="34" width="3" height="4" fill="{color}"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      }}
      @keyframes blinkLed {{
        0%, 100% {{ fill: {color}; }}
        50% {{ fill: #1E293B; }}
      }}
      .led {{
        animation: blinkLed 2s infinite steps(1);
      }}
    </style>
  </defs>

  <!-- TRANSLUCENT BACKGROUND -->
  <rect x="6" y="4" width="{width-12}" height="28" fill="{bg_glass}" stroke="{border_slate}" stroke-width="2"/>
  <rect x="8" y="6" width="{width-16}" height="24" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.8"/>

  <!-- Corner notches (Top bracket ┌ ┐) -->
  <rect x="6" y="4" width="5" height="5" fill="{color}"/>
  <rect x="{width-11}" y="4" width="5" height="5" fill="{color}"/>
  <rect x="6" y="27" width="5" height="5" fill="{color}"/>
  <rect x="{width-11}" y="27" width="5" height="5" fill="{color}"/>

  {teeth_markup}

  <!-- Status LED -->
  <circle cx="24" cy="18" r="4" fill="{color}" class="led"/>

  <!-- Title Text -->
  <text x="36" y="22" fill="{color}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">
    {title}
  </text>

  <!-- Right Status Tag -->
  <rect x="{width-180}" y="9" width="105" height="18" fill="{theme['bg_panel']}" stroke="{color}" stroke-width="1"/>
  <text x="{width-127}" y="22" fill="{color}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">[{tag}]</text>

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-68}" y="11" width="14" height="14" fill="{border_slate}"/>
  <text x="{width-64}" y="21" fill="#8892B0" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{border_slate}"/>
  <text x="{width-47}" y="22" fill="#8892B0" font-size="10" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-32}" y="11" width="14" height="14" fill="#FF0055"/>
  <text x="{width-28}" y="22" fill="#FFFFFF" font-size="10" font-weight="bold" class="font-mono">×</text>
</svg>"""
    return svg

def build_frame_bottom(tag, color, theme, width=850, height=22, open_bracket=True):
    """
    Builds a bottom window frame with upward embracing teeth and status buffer readout.
    """
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.75)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    teeth_markup = ""
    if open_bracket:
        teeth_markup = f"""
  <!-- UPWARD EMBRACING BRACKET ACCENTS -->
  <path d="M 6 0 L 6 8 L 12 8" fill="none" stroke="{color}" stroke-width="2"/>
  <rect x="6" y="0" width="3" height="4" fill="{color}"/>
  <path d="M {width-6} 0 L {width-6} 8 L {width-12} 8" fill="none" stroke="{color}" stroke-width="2"/>
  <rect x="{width-9}" y="0" width="3" height="4" fill="{color}"/>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      .font-mono {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      }}
    </style>
  </defs>

  {teeth_markup}

  <!-- Main bottom boundary line -->
  <line x1="6" y1="8" x2="{width-6}" y2="8" stroke="{border_slate}" stroke-width="3"/>
  <line x1="12" y1="8" x2="{width-12}" y2="8" stroke="{color}" stroke-width="1.5" opacity="0.8"/>

  <!-- Left / Right Corner hooks (Bottom bracket └ ┘) -->
  <path d="M 6 8 L 6 18 L 24 18" fill="none" stroke="{color}" stroke-width="1.5"/>
  <rect x="6" y="15" width="4" height="4" fill="{color}"/>

  <path d="M {width-6} 8 L {width-6} 18 L {width-24} 18" fill="none" stroke="{color}" stroke-width="1.5"/>
  <rect x="{width-10}" y="15" width="4" height="4" fill="{color}"/>

  <!-- Center Status Buffer Readout -->
  <rect x="{width//2 - 95}" y="2" width="190" height="16" fill="{bg_glass}" stroke="{color}" stroke-width="1"/>
  <text x="{width//2}" y="13" fill="{color}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">
    ╚═ [{tag}] ═╝
  </text>
</svg>"""
    return svg

def build_side_rail(height, color, theme, side="left", width=14):
    """
    Builds a vertical side rail SVG for full box enclosure mode.
    """
    bg_glass = theme.get("bg_glass", "rgba(10, 14, 23, 0.75)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    dash_lines = []
    for y in range(8, height - 8, 12):
        dash_lines.append(f'<rect x="4" y="{y}" width="4" height="6" fill="{color}" opacity="0.6"/>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <rect width="{width}" height="{height}" fill="{bg_glass}"/>
  <line x1="2" y1="0" x2="2" y2="{height}" stroke="{color}" stroke-width="2"/>
  <line x1="{width-2}" y1="0" x2="{width-2}" y2="{height}" stroke="{border_slate}" stroke-width="1"/>
  {''.join(dash_lines)}
</svg>"""
    return svg

def build_chip(text, color, theme, style="closed", width=None, height=26):
    """
    Builds a holographic clickable chip:
    - 'closed': Classic 4-sided semi-transparent pill.
    - 'decay_right': Right border breaks into pixel dithering fade.
    - 'decay_left': Left border breaks into pixel dithering fade.
    """
    bg_chip = theme.get("bg_chip", "rgba(0, 240, 255, 0.08)")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    # Estimate width if not given (approx 8px per char + padding)
    if width is None:
        width = max(len(text) * 9 + 32, 85)

    dither_markup = ""
    stroke_w = 1.5

    if style == "closed":
        # Full enclosing border with 4 corner notches
        body_markup = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="1" y="1" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{color}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{color}"/>
        """
        text_x = width // 2
    elif style == "decay_right":
        # Solid on left, dithered decay on right
        width_body = width - 20
        body_markup = f"""
  <!-- Left solid box -->
  <path d="M {width_body} 1 L 1 1 L 1 {height-1} L {width_body} {height-1}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="1" y="1" width="3" height="3" fill="{color}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{color}"/>

  <!-- Right Pixel Decay (Scattered Dithering) -->
  <g fill="{color}">
    <!-- Column 1 (dense) -->
    <rect x="{width_body + 2}" y="3" width="3" height="3"/>
    <rect x="{width_body + 2}" y="9" width="3" height="3"/>
    <rect x="{width_body + 2}" y="15" width="3" height="3"/>
    <rect x="{width_body + 2}" y="20" width="3" height="3"/>

    <!-- Column 2 (medium) -->
    <rect x="{width_body + 7}" y="5" width="2" height="2"/>
    <rect x="{width_body + 7}" y="12" width="2" height="2"/>
    <rect x="{width_body + 7}" y="18" width="2" height="2"/>

    <!-- Column 3 (sparse/scatter) -->
    <rect x="{width_body + 12}" y="7" width="2" height="2" opacity="0.6"/>
    <rect x="{width_body + 15}" y="14" width="2" height="2" opacity="0.4"/>
    <rect x="{width_body + 18}" y="10" width="1" height="1" opacity="0.3"/>
  </g>
        """
        text_x = (width_body + 4) // 2
    elif style == "decay_left":
        # Dithered decay on left, solid on right
        left_offset = 20
        body_markup = f"""
  <!-- Right solid box -->
  <path d="M {left_offset} 1 L {width-1} 1 L {width-1} {height-1} L {left_offset} {height-1}" fill="{bg_chip}" stroke="{color}" stroke-width="{stroke_w}"/>
  <rect x="{width-4}" y="1" width="3" height="3" fill="{color}"/>
  <rect x="{width-4}" y="{height-4}" width="3" height="3" fill="{color}"/>

  <!-- Left Pixel Decay (Scattered Dithering) -->
  <g fill="{color}">
    <!-- Column 1 (dense) -->
    <rect x="{left_offset - 5}" y="3" width="3" height="3"/>
    <rect x="{left_offset - 5}" y="9" width="3" height="3"/>
    <rect x="{left_offset - 5}" y="15" width="3" height="3"/>
    <rect x="{left_offset - 5}" y="20" width="3" height="3"/>

    <!-- Column 2 (medium) -->
    <rect x="{left_offset - 10}" y="5" width="2" height="2"/>
    <rect x="{left_offset - 10}" y="12" width="2" height="2"/>
    <rect x="{left_offset - 10}" y="18" width="2" height="2"/>

    <!-- Column 3 (sparse/scatter) -->
    <rect x="{left_offset - 14}" y="7" width="2" height="2" opacity="0.6"/>
    <rect x="{left_offset - 17}" y="14" width="2" height="2" opacity="0.4"/>
    <rect x="{left_offset - 19}" y="10" width="1" height="1" opacity="0.3"/>
  </g>
        """
        text_x = left_offset + (width - left_offset) // 2
    else:
        body_markup = f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg_chip}" stroke="{color}"/>'
        text_x = width // 2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      .chip-text {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 0.5px;
      }}
    </style>
  </defs>

  {body_markup}

  <!-- Label Text -->
  <text x="{text_x}" y="17" fill="{color}" text-anchor="middle" class="chip-text">
    {text}
  </text>
</svg>"""
    return svg

def build_pcb_divider(theme, width=850, height=26):
    """
    Builds a translucent PCB circuit trace with animated flowing data packet.
    """
    primary = theme.get("primary", "#00F0FF")
    secondary = theme.get("secondary", "#BD93F9")
    success = theme.get("success", "#39FF14")
    warning = theme.get("warning", "#FFE600")
    accent = theme.get("accent", "#FF0055")
    border_slate = theme.get("border_slate", "rgba(30, 41, 59, 0.85)")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes traceFlow {{
        0% {{ transform: translateX(-100px); }}
        100% {{ transform: translateX({width + 100}px); }}
      }}
      .flow-packet {{
        animation: traceFlow 3.5s linear infinite;
      }}
    </style>
  </defs>

  <!-- Bus line -->
  <line x1="20" y1="13" x2="{width-20}" y2="13" stroke="{border_slate}" stroke-width="4"/>
  <line x1="20" y1="13" x2="{width-20}" y2="13" stroke="{primary}" stroke-width="2" opacity="0.6"/>

  <!-- Auxiliary trace top -->
  <path d="M 50 6 L 150 6 L 160 13 L 300 13 L 310 6 L 500 6 L 510 13 L 720 13 L 730 6 L 800 6" fill="none" stroke="{secondary}" stroke-width="1.5" opacity="0.5"/>
  <!-- Auxiliary trace bottom -->
  <path d="M 40 20 L 110 20 L 120 13 L 240 13 L 250 20 L 440 20 L 450 13 L 650 13 L 660 20 L 810 20" fill="none" stroke="{success}" stroke-width="1.5" opacity="0.4"/>

  <!-- Soldering pads / Vias -->
  <rect x="20" y="10" width="6" height="6" fill="{warning}"/>
  <rect x="21" y="11" width="4" height="4" fill="rgba(10, 14, 23, 0.9)"/>

  <rect x="50" y="3" width="6" height="6" fill="{primary}"/>
  <rect x="51" y="4" width="4" height="4" fill="rgba(10, 14, 23, 0.9)"/>

  <rect x="150" y="3" width="6" height="6" fill="{secondary}"/>
  <rect x="240" y="10" width="6" height="6" fill="{success}"/>

  <g transform="translate({width//2}, 13)">
    <rect x="-10" y="-8" width="20" height="16" fill="{theme['bg_panel']}" stroke="{primary}" stroke-width="1.5"/>
    <circle cx="0" cy="0" r="2" fill="{warning}"/>
  </g>

  <rect x="600" y="10" width="6" height="6" fill="{success}"/>
  <rect x="730" y="3" width="6" height="6" fill="{primary}"/>
  <rect x="{width-20}" y="10" width="6" height="6" fill="{warning}"/>
  <rect x="{width-19}" y="11" width="4" height="4" fill="rgba(10, 14, 23, 0.9)"/>

  <!-- Moving Data Packet -->
  <g class="flow-packet">
    <rect x="0" y="11" width="12" height="4" fill="{warning}"/>
    <rect x="12" y="12" width="8" height="2" fill="#FFFFFF"/>
    <rect x="-8" y="12" width="8" height="2" fill="{accent}"/>
  </g>
</svg>"""
    return svg
