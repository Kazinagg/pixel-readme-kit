"""Footer closing plate components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import measure_mono_text_width, clamp_text_to_width
from generator.components.base import escape_xml, validate_svg

def generate_footer(style=None, primary=None, accent=None,
                    status="SESSION_ACTIVE // STANDBY", nav_text="RETURN TO TOP",
                    sub_text=None, width=850, height=76, mode="auto", preset=None, tertiary=None,
                    theme=None):
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
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
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

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


