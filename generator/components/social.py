"""Social, starchart and profile card components for Pixel Readme Kit."""
from typing import Optional, Any, List
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import measure_mono_text_width, clamp_text_to_width
from generator.components.base import escape_xml, validate_svg
from generator.font_engine import render_3d_text, calculate_smart_layout, calculate_px_size

def generate_social(style=None, primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT RETRO HUD READMES",
                    repo="Kazinagg/pixel-readme-kit", tags="PYTHON,SVG,HUD,RETRO",
                    width=1280, height=640, mode="auto", preset=None, tertiary=None, theme=None):
    """
    Renders an OpenGraph Social Preview Card (1280x640) for GitHub repositories.
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

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

def generate_starchart(style=None, primary=None, accent=None,
                       repo="Kazinagg/pixel-readme-kit", points=None,
                       current=None, delta="+78% past 6m", title="STAR GROWTH TRAJECTORY",
                       period="6M", width=850, height=230, mode="auto", preset=None, tertiary=None, theme=None):
    """
    Renders an authentic, vector SVG star trend chart / activity chart (850x230).
    Features:
    - Glowing polyline curve and area gradient fill
    - Dynamic coordinate grid with Y-value levels and X-period labels
    - Peak milestone marker with star count callout tag
    - Authentic HUD header plate with live/custom repository stats
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

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

def generate_profile_card(style=None, primary=None, accent=None,
                          name="ALEX DEVELOPER", role="FULLSTACK & SYSTEMS ARCHITECT",
                          bio="Building high-performance runtimes and resilient developer tooling.",
                          status="AVAILABLE FOR HIRE", location="REMOTE // UTC+3",
                          badge="LEVEL_99", width=850, height=190, mode="auto", preset=None,
                          tertiary=None, theme=None):
    """
    Renders a flagship developer dossier / identity header card (850x190) for GitHub Profiles.
    Features:
    - Stylized cyber avatar frame with status LED ring
    - 3D Typography name header and role descriptor
    - Clean manifesto / bio summary section
    - Multi-mode theming and responsive vector geometry
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    if theme_name in ("tactical", "amber", "amber_crt") or style_name == "tactical":
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper",
                       "corporate-blue", "corporate_blue", "swiss-mono", "swiss_mono",
                       "executive-slate", "executive_slate", "slate-dark", "slate_dark",
                       "nordic-frost", "nordic_frost", "linear-violet", "linear_violet",
                       "emerald-clean", "emerald_clean", "enterprise-navy", "enterprise_navy") or style_name in ("modern", "corporate"):
        st = "modern_corporate"
    else:
        st = "cyberpunk"

    name_clean = escape_xml(name.upper())
    role_clean = escape_xml(role.upper())
    bio_clean = escape_xml(bio)
    status_clean = escape_xml(status.upper())
    loc_clean = escape_xml(location.upper())
    badge_clean = escape_xml(badge.upper())

    # Available width for name and header items
    av_x, av_y, av_size = 28, 28, 134
    max_name_w = width - 180 - 40

    # Dynamic badges and status pills (top right)
    badge_disp = clamp_text_to_width(badge_clean, 120, 10.5)
    badge_w = max(70, int(measure_mono_text_width(badge_disp, 10.5) + 20))
    status_disp = clamp_text_to_width(status_clean, 160, 10)
    status_w = max(90, int(measure_mono_text_width(status_disp, 10) + 32))
    pills_gap = 8
    pills_total_w = badge_w + pills_gap + status_w
    pills_x = width - pills_total_w - 20

    # Top breadcrumb dossier
    avail_dossier_w = max(60, pills_x - 180 - 15)
    if st == "tactical":
        dossier_prefix = "■ TAC_ID // "
    elif st == "modern_corporate":
        dossier_prefix = "DOSSIER // "
    else:
        dossier_prefix = "■ CYBER_ID // "
    dossier_full = f"{dossier_prefix}{loc_clean}"
    dossier_disp = clamp_text_to_width(dossier_full, avail_dossier_w - 24, 11)
    dossier_w = max(120, min(avail_dossier_w, int(measure_mono_text_width(dossier_disp, 11) + 24)))

    # Role and Bio sizing
    max_role_w = width - 180 - 30
    role_disp = clamp_text_to_width(f"▶ {role_clean}", max_role_w - 28, 12)
    role_w = max(160, min(max_role_w, int(measure_mono_text_width(role_disp, 12) + 28)))
    bio_disp = clamp_text_to_width(bio_clean, width - 180 - 30, 12)

    # -------------------------------------------------------------
    # 1. TACTICAL HUD PARADIGM (MIL-SPEC armored casing & crosshairs)
    # -------------------------------------------------------------
    if st == "tactical":
        chassis = f"""
  <!-- TACTICAL ARMORED CHASSIS -->
  <polygon points="16 1, {width-16} 1, {width-1} 16, {width-1} {height-16}, {width-16} {height-1}, 16 {height-1}, 1 {height-16}, 1 16"
           fill="{bg}" stroke="{border}" stroke-width="1.8"/>
  <rect x="1" y="16" width="4" height="24" fill="{prim}"/>
  <rect x="{width-5}" y="{height-40}" width="4" height="24" fill="{acc}"/>
  <!-- Reticle Crosshair Marks -->
  <line x1="20" y1="10" x2="28" y2="10" stroke="{prim}" stroke-width="1.5"/>
  <line x1="24" y1="6" x2="24" y2="14" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{width-28}" y1="10" x2="{width-20}" y2="10" stroke="{acc}" stroke-width="1.5"/>
  <line x1="{width-24}" y1="6" x2="{width-24}" y2="14" stroke="{acc}" stroke-width="1.5"/>
  <!-- Telemetry Grate (Bottom Right) -->
  <rect x="{width-80}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <rect x="{width-73}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <rect x="{width-66}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <rect x="{width-59}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <text x="24" y="{height-8}" fill="{text_dim}" font-size="8.5" class="font-mono">MIL-STD-810 // HUD_TELEMETRY // SYS_ID:0x884F</text>
"""
        avatar_markup = f"""
  <!-- TACTICAL AVATAR & RANGEFINDER RETICLE -->
  <g transform="translate({av_x}, {av_y})">
    <polygon points="10 0, {av_size-10} 0, {av_size} 10, {av_size} {av_size-10}, {av_size-10} {av_size}, 10 {av_size}, 0 {av_size-10}, 0 10"
             fill="{panel}" stroke="{border}" stroke-width="1.8"/>
    <!-- Azimuth Rangefinder Ring -->
    <circle cx="{av_size//2}" cy="54" r="38" fill="none" stroke="{prim}" stroke-width="1.2" stroke-dasharray="3 4"/>
    <circle cx="{av_size//2}" cy="54" r="46" fill="none" stroke="{border}" stroke-width="0.8"/>
    <!-- Reticle Crosshair Ticks -->
    <line x1="{av_size//2}" y1="10" x2="{av_size//2}" y2="22" stroke="{acc}" stroke-width="1.5"/>
    <line x1="{av_size//2}" y1="86" x2="{av_size//2}" y2="98" stroke="{acc}" stroke-width="1.5"/>
    <line x1="14" y1="54" x2="26" y2="54" stroke="{acc}" stroke-width="1.5"/>
    <line x1="{av_size-26}" y1="54" x2="{av_size-14}" y2="54" stroke="{acc}" stroke-width="1.5"/>
    <!-- Operator Silhouette -->
    <circle cx="{av_size//2}" cy="50" r="16" fill="{bg}" stroke="{prim}" stroke-width="2"/>
    <path d="M 32 94 L 46 78 L {av_size-46} 78 L {av_size-32} 94 Z" fill="{bg}" stroke="{prim}" stroke-width="2"/>
    <circle cx="{av_size//2}" cy="50" r="6" fill="{acc}"/>
    <!-- Tactical Readiness Status Bar -->
    <rect x="8" y="110" width="{av_size-16}" height="16" fill="{bg}" stroke="{acc}" stroke-width="1"/>
    <text x="{av_size//2}" y="122" fill="{acc}" font-size="8.5" font-weight="bold" text-anchor="middle" class="font-mono">HUD // ACTIVE</text>
  </g>
"""
        lines, calc_px = calculate_smart_layout(name, max_width=max_name_w, default_px_size=5, min_px_size=3, spacing=2, allow_wrap=False)
        single_name = lines[0] if lines else name
        name_markup, _, _ = render_3d_text(
            single_name, x=180, y=58, px_size=calc_px,
            front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
            spacing=2, max_width=max_name_w, allow_wrap=False
        )
        role_markup = f"""
  <g transform="translate(180, 116)">
    <polygon points="0 0, {role_w-8} 0, {role_w} 8, {role_w} 26, 0 26" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
    <rect x="0" y="0" width="5" height="26" fill="{prim}"/>
    <text x="14" y="17" fill="{acc}" font-size="11.5" font-weight="bold" class="font-mono">{role_disp}</text>
  </g>
"""

    # -------------------------------------------------------------
    # 2. MODERN & CORPORATE & ACADEMIC PARADIGM (Pure Vector Cleanliness)
    # -------------------------------------------------------------
    elif st == "modern_corporate":
        is_academic_corp = theme_name in ("academic-paper", "academic_paper", "corporate-blue", "corporate_blue",
                                          "enterprise-navy", "enterprise_navy", "swiss-mono", "swiss_mono", "clean-mono", "clean_mono") or style_name == "corporate"
        if is_academic_corp:
            chassis = f"""
  <!-- CORPORATE / ACADEMIC FORMAL SPECIFICATION DOSSIER -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="5" y="5" width="{width-10}" height="{height-10}" fill="none" stroke="{border}" stroke-width="0.8" opacity="0.6"/>
  <line x1="5" y1="5" x2="{width-5}" y2="5" stroke="{prim}" stroke-width="2.5"/>
  <line x1="5" y1="{height-5}" x2="{width-5}" y2="{height-5}" stroke="{border}" stroke-width="1"/>
  <text x="{width-18}" y="{height-10}" fill="{text_dim}" font-size="8.5" text-anchor="end" class="font-mono">IDENTIFICATION PROTOCOL // VERIFIED</text>
"""
        else:
            chassis = f"""
  <!-- MODERN CLEAN VECTOR CARD -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <path d="M 12 1 L {width-12} 1" stroke="{prim}" stroke-width="2.5" stroke-linecap="round"/>
"""

        avatar_markup = f"""
  <!-- CLEAN MINIMALIST AVATAR -->
  <g transform="translate({av_x}, {av_y})">
    <rect x="0" y="0" width="{av_size}" height="{av_size}" rx="12" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <!-- Smooth User Silhouette (Pure Vector) -->
    <circle cx="{av_size//2}" cy="48" r="22" fill="{bg}" stroke="{prim}" stroke-width="1.8"/>
    <path d="M 28 98 C 28 76, {av_size-28} 76, {av_size-28} 98 Z" fill="{bg}" stroke="{prim}" stroke-width="1.8"/>
    <circle cx="{av_size//2}" cy="48" r="8" fill="{acc}"/>
    <!-- Minimalist Status Indicator -->
    <rect x="16" y="108" width="{av_size-32}" height="18" rx="9" fill="{bg}" stroke="{success}" stroke-width="1"/>
    <circle cx="28" cy="117" r="3" fill="{success}"/>
    <text x="36" y="120" fill="{success}" font-size="8.5" font-weight="600" class="font-mono">ACTIVE</text>
  </g>
"""
        # PURE VECTOR NAME TYPOGRAPHY (No pixelated pseudo-3D block shadows)
        calc_font_size = 26
        while calc_font_size > 14 and measure_mono_text_width(name_clean, calc_font_size) > max_name_w:
            calc_font_size -= 2
        name_markup = f"""  <text x="180" y="78" fill="{c['title_front']}" font-size="{calc_font_size}" font-weight="700" letter-spacing="0.04em" class="font-mono">{name_clean}</text>"""

        role_markup = f"""
  <g transform="translate(180, 116)">
    <rect x="0" y="0" width="{role_w}" height="26" rx="4" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <rect x="0" y="0" width="3" height="26" rx="1.5" fill="{prim}"/>
    <text x="12" y="17" fill="{acc}" font-size="11.5" font-weight="600" class="font-mono">{role_disp}</text>
  </g>
"""

    # -------------------------------------------------------------
    # 3. CYBERPUNK / RETRO-TECH PARADIGM (Asymmetrical cuts & neon beacons)
    # -------------------------------------------------------------
    else:
        chassis = f"""
  <!-- CYBERPUNK ASYMMETRICAL DECK -->
  <polygon points="20 1, {width-1} 1, {width-1} {height-20}, {width-20} {height-1}, 1 {height-1}, 1 20"
           fill="{bg}" stroke="{border}" stroke-width="1.8"/>
  <rect x="1" y="20" width="3" height="40" fill="{prim}"/>
  <rect x="{width-4}" y="{height-60}" width="3" height="40" fill="{acc}"/>
  <line x1="24" y1="{height-8}" x2="160" y2="{height-8}" stroke="{acc}" stroke-width="2" stroke-dasharray="8 4 2 4"/>
  <!-- Corner Beacons -->
  <rect x="20" y="1" width="12" height="3" fill="{prim}"/>
  <rect x="{width-32}" y="{height-4}" width="12" height="3" fill="{prim}"/>
"""
        avatar_markup = f"""
  <!-- CYBERPUNK HEXAGONAL AVATAR & SCANNER -->
  <g transform="translate({av_x}, {av_y})">
    <polygon points="16 0, {av_size-16} 0, {av_size} 16, {av_size} {av_size-16}, {av_size-16} {av_size}, 16 {av_size}, 0 {av_size-16}, 0 16"
             fill="{panel}" stroke="{prim}" stroke-width="1.8"/>
    <!-- Cyber Scanner Lines -->
    <line x1="10" y1="40" x2="{av_size-10}" y2="40" stroke="{border}" stroke-width="0.8"/>
    <line x1="10" y1="70" x2="{av_size-10}" y2="70" stroke="{border}" stroke-width="0.8"/>
    <!-- Netrunner Silhouette -->
    <circle cx="{av_size//2}" cy="50" r="22" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <polygon points="28 102, 42 78, {av_size-42} 78, {av_size-28} 102" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <circle cx="{av_size//2}" cy="50" r="8" fill="{prim}"/>
    <!-- Neon Status LED Pill -->
    <polygon points="10 110, {av_size-10} 110, {av_size-14} 126, 6 126" fill="{bg}" stroke="{success}" stroke-width="1.2"/>
    <text x="{av_size//2}" y="122" fill="{success}" font-size="8.5" font-weight="bold" text-anchor="middle" class="font-mono">NET // ONLINE</text>
  </g>
"""
        lines, calc_px = calculate_smart_layout(name, max_width=max_name_w, default_px_size=5, min_px_size=3, spacing=2, allow_wrap=False)
        single_name = lines[0] if lines else name
        name_markup, _, _ = render_3d_text(
            single_name, x=180, y=58, px_size=calc_px,
            front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
            spacing=2, max_width=max_name_w, allow_wrap=False
        )
        role_markup = f"""
  <g transform="translate(180, 116)">
    <rect x="0" y="0" width="{role_w}" height="26" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
    <rect x="0" y="0" width="4" height="26" fill="{prim}"/>
    <text x="14" y="17" fill="{acc}" font-size="12" font-weight="bold" class="font-mono">{role_disp}</text>
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

  {avatar_markup}

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

  <!-- NAME TYPOGRAPHY -->
  {name_markup}

  <!-- ROLE PILL -->
  {role_markup}

  <!-- BIO SUMMARY -->
  <text x="182" y="166" fill="{text_main}" font-size="12" font-weight="normal" class="font-mono">{bio_disp}</text>
</svg>"""

    validate_svg(svg)
    return svg


