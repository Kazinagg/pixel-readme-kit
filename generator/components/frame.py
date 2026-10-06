"""Frame window cap components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme
from generator.layout import format_tag, format_bottom_tag, clamp_text_to_width, measure_mono_text_width
from generator.components.base import escape_xml, validate_svg

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


