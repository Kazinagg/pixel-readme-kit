#!/usr/bin/env python3
"""
Render Stand & Catalog Generator for ReadmeKit.
Generates all 16 block types across all 5 canonical themes into assets/gallery/
and builds an interactive HTML showcase for visual quality inspection.
"""

import os
import sys
from generator import engine
from generator.components.base import validate_svg

CANONICAL_THEMES = [
    {
        "style": "pixel",
        "theme": "cyberpunk",
        "name": "CYBERPUNK",
        "desc": "Classic Sci-Fi HUD with 3D extruded typography, 360 radar, audio equalizer, and neon cyan/magenta styling."
    },
    {
        "style": "pixel",
        "theme": "tactical",
        "name": "TACTICAL",
        "desc": "Mil-Spec HUD with 45-degree chamfers, hazard chevron patterns, crosshair targeting reticle, and amber palette."
    },
    {
        "style": "pixel",
        "theme": "minimal",
        "name": "MINIMAL",
        "desc": "Tokyo Minimalist Dot-Matrix with Swiss hairline grid, clean pixel borders, and quiet high-contrast mono typography."
    },
    {
        "style": "modern",
        "theme": "modern-clean",
        "name": "MODERN CLEAN",
        "desc": "Silicon Valley clean vector styling with rounded cards, smooth gradients, subtle drop shadows, and Inter typography."
    },
    {
        "style": "sketch",
        "theme": "rough-doodle",
        "name": "ROUGH DOODLE",
        "desc": "Excalidraw hand-drawn vector styling with organic rough pencil contours, sketchy crosshatch shading, and marker tape."
    }
]

BLOCK_DEFINITIONS = [
    {
        "id": "header",
        "name": "Header Banner",
        "category": "Hero & Banners",
        "directive": '<!-- readme-kit:header title="READMEKIT // STUDIO" subtitle="Universal Customization System for GitHub" tag="[V5.1]" spec1="PYTHON 3.10+" spec2="100% SVG" spec3="NOMINAL" -->',
        "generate": lambda s, t: engine.generate_header(
            style=s, theme=t,
            title="READMEKIT // STUDIO",
            subtitle="Universal Customization System for GitHub",
            tag="[V5.1]",
            spec1="PYTHON 3.10+", spec2="100% SVG", spec3="NOMINAL"
        )
    },
    {
        "id": "window-top",
        "name": "Window Frame (Top)",
        "category": "Containers",
        "directive": '<!-- readme-kit:window title="CORE // ARCHITECTURE" tag="[SYS_LOG]" -->',
        "generate": lambda s, t: engine.generate_frame(
            style=s, theme=t, frame_type="top",
            title="CORE // ARCHITECTURE", tag="[SYS_LOG]"
        )
    },
    {
        "id": "window-bottom",
        "name": "Window Frame (Bottom)",
        "category": "Containers",
        "directive": '<!-- /readme-kit:window -->',
        "generate": lambda s, t: engine.generate_frame(
            style=s, theme=t, frame_type="bottom",
            title="CORE // ARCHITECTURE", tag="[SYS_LOG]"
        )
    },
    {
        "id": "terminal-top",
        "name": "Terminal Shell (Top)",
        "category": "Containers",
        "directive": '<!-- readme-kit:terminal title="BASH // PRODUCTION_DEPLOY" tag="[ONLINE]" -->',
        "generate": lambda s, t: engine.generate_frame(
            style=s, theme=t, frame_type="term_top",
            title="BASH // PRODUCTION_DEPLOY", tag="[ONLINE]"
        )
    },
    {
        "id": "terminal-bottom",
        "name": "Terminal Shell (Bottom)",
        "category": "Containers",
        "directive": '<!-- /readme-kit:terminal -->',
        "generate": lambda s, t: engine.generate_frame(
            style=s, theme=t, frame_type="term_bottom",
            title="BASH // PRODUCTION_DEPLOY", tag="[ONLINE]"
        )
    },
    {
        "id": "quote",
        "name": "Architectural Quote",
        "category": "Callouts & Content",
        "directive": '<!-- readme-kit:quote title="ARCHITECTURAL NOTICE" subtitle="Component standard" badge="NOTE" -->',
        "generate": lambda s, t: engine.generate_callout(
            style=s, theme=t, is_quote=True,
            title="ARCHITECTURAL NOTICE",
            subtitle="Component standard guarantees deterministic SVG rendering across dark and light modes.",
            callout_type="note"
        )
    },
    {
        "id": "callout",
        "name": "Alert Callout",
        "category": "Callouts & Content",
        "directive": '<!-- readme-kit:callout title="SECURITY ADVISORY" subtitle="Update dependency versions to latest patch" callout_type="warning" -->',
        "generate": lambda s, t: engine.generate_callout(
            style=s, theme=t, is_quote=False,
            title="SECURITY ADVISORY",
            subtitle="Update dependency versions to latest patch to ensure binary integrity.",
            callout_type="warning"
        )
    },
    {
        "id": "footer",
        "name": "Footer Bar",
        "category": "Navigation",
        "directive": '<!-- readme-kit:footer status="SYSTEM NOMINAL // ALL TESTS GREEN" nav_text="BACK TO TOP [^]" sub_text="BUILD 2026.10" -->',
        "generate": lambda s, t: engine.generate_footer(
            style=s, theme=t,
            status="SYSTEM NOMINAL // ALL TESTS GREEN",
            nav_text="BACK TO TOP [^]",
            sub_text="BUILD 2026.10"
        )
    },
    {
        "id": "divider",
        "name": "Divider Line",
        "category": "Navigation",
        "directive": '<!-- readme-kit:divider -->',
        "generate": lambda s, t: engine.generate_divider(
            style=s, theme=t, width=850
        )
    },
    {
        "id": "splitter",
        "name": "Section Splitter",
        "category": "Navigation",
        "directive": '<!-- readme-kit:splitter label="SECTION // TELEMETRY METRICS" -->',
        "generate": lambda s, t: engine.generate_splitter(
            style=s, theme=t, label="SECTION // TELEMETRY METRICS", width=850
        )
    },
    {
        "id": "chip",
        "name": "Status Chip",
        "category": "Badges",
        "directive": '<!-- readme-kit:chip text="STATUS: 200 OK" type="decay" decay_dir="right" -->',
        "generate": lambda s, t: engine.generate_chip(
            style=s, theme=t, text="STATUS: 200 OK", chip_type="decay", decay_dir="right"
        )
    },
    {
        "id": "metrics",
        "name": "Metrics KPI Row",
        "category": "Metrics & Status",
        "directive": '<!-- readme-kit:metrics items="CORE UPTIME: 99.98% | LATENCY: 12ms | BUFFER: 256MB" -->',
        "generate": lambda s, t: engine.generate_metrics(
            style=s, theme=t,
            metrics=[
                {"label": "CORE UPTIME", "value": "99.98%", "status": "NOMINAL", "delta": "+0.02%"},
                {"label": "LATENCY", "value": "12ms", "status": "OPTIMAL", "delta": "-3ms"},
                {"label": "BUFFER", "value": "256MB", "status": "STABLE", "delta": "+14MB"}
            ],
            width=850
        )
    },
    {
        "id": "progress",
        "name": "Progress Gauge",
        "category": "Metrics & Status",
        "directive": '<!-- readme-kit:progress value="85" label="SPRINT COMPLETION" sub="34 OF 40 TASKS COMPLETED" -->',
        "generate": lambda s, t: engine.generate_progress(
            style=s, theme=t, value=85,
            label="SPRINT COMPLETION",
            sub="34 OF 40 TASKS COMPLETED (85%)",
            width=850
        )
    },
    {
        "id": "techstack",
        "name": "Tech Stack Grid",
        "category": "Metrics & Status",
        "directive": '<!-- readme-kit:techstack items="python,rust,docker,git,typescript" columns="5" -->',
        "generate": lambda s, t: engine.generate_techstack(
            style=s, theme=t,
            items=[
                {"name": "PYTHON", "icon": "python", "label": "CORE"},
                {"name": "RUST", "icon": "rust", "label": "NATIVE"},
                {"name": "DOCKER", "icon": "docker", "label": "OPS"},
                {"name": "GIT", "icon": "git", "label": "VCS"},
                {"name": "TYPESCRIPT", "icon": "typescript", "label": "STUDIO"}
            ],
            columns=5, width=850
        )
    },
    {
        "id": "timeline",
        "name": "Roadmap Timeline",
        "category": "Metrics & Status",
        "directive": '<!-- readme-kit:timeline -->\nmilestone title="v1.0" date="2024-Q1" status="COMPLETED" desc="Core pixel engine"\nmilestone title="v2.0" date="2025-Q2" status="ACTIVE" desc="Modern clean vector"\nmilestone title="v3.0" date="2026-Q4" status="PLANNED" desc="Universal 3-tier kit"\n<!-- /readme-kit:timeline -->',
        "generate": lambda s, t: engine.generate_timeline(
            style=s, theme=t,
            milestones=[
                {"title": "v1.0 GENESIS", "date": "2024-Q1", "status": "COMPLETED", "desc": "Initial pixel engine and 8-bit typography"},
                {"title": "v2.0 VECTOR", "date": "2025-Q2", "status": "ACTIVE", "desc": "Modern clean vector paradigms and glass UI"},
                {"title": "v3.0 HORIZON", "date": "2026-Q4", "status": "PLANNED", "desc": "Universal 3-tier design system and studio stand"}
            ],
            width=850
        )
    },
    {
        "id": "starchart",
        "name": "Star Growth Chart",
        "category": "GitHub Social",
        "directive": '<!-- readme-kit:starchart repo="Kazinagg/pixel-readme-kit" title="TELEMETRY // STAR GROWTH" -->',
        "generate": lambda s, t: engine.generate_starchart(
            style=s, theme=t,
            title="TELEMETRY // STAR GROWTH",
            repo="Kazinagg/pixel-readme-kit",
            current=1280,
            delta="+340 this month",
            width=850
        )
    },
    {
        "id": "profile",
        "name": "Profile HUD Card",
        "category": "GitHub Social",
        "directive": '<!-- readme-kit:profile name="CYBER_ARCHITECT" role="SYSTEM SPECIALIST" bio="Building modular pixel and vector HUD experiences" status="ONLINE" location="TOKYO / NET" badge="CORE_DEV" -->',
        "generate": lambda s, t: engine.generate_profile_card(
            style=s, theme=t,
            name="CYBER_ARCHITECT",
            role="SYSTEM SPECIALIST",
            bio="Building modular pixel and vector HUD experiences for GitHub readmes",
            status="ONLINE",
            location="TOKYO / NET",
            badge="CORE_DEV",
            width=850
        )
    },
    {
        "id": "social",
        "name": "Social Preview Banner",
        "category": "GitHub Social",
        "directive": '<!-- readme-kit:social title="READMEKIT" subtitle="Universal Customization System for GitHub" repo="Kazinagg/pixel-readme-kit" tags="PYTHON,SVG,STUDIO,GITHUB" -->',
        "generate": lambda s, t: engine.generate_social(
            style=s, theme=t,
            title="READMEKIT",
            subtitle="Universal Customization System for GitHub",
            repo="Kazinagg/pixel-readme-kit",
            tags="PYTHON,SVG,STUDIO,GITHUB",
            width=850
        )
    }
]


def render_all_gallery():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gallery_dir = os.path.join(base_dir, "assets", "gallery")
    os.makedirs(gallery_dir, exist_ok=True)

    print(f"[*] Rendering all 16 blocks across {len(CANONICAL_THEMES)} canonical themes...")
    rendered_items = []

    for theme_info in CANONICAL_THEMES:
        style = theme_info["style"]
        theme = theme_info["theme"]
        theme_name = theme_info["name"]
        theme_subfolder = os.path.join(gallery_dir, theme)
        os.makedirs(theme_subfolder, exist_ok=True)

        print(f" -> Theme: {theme_name} ({style} / {theme})")

        for block in BLOCK_DEFINITIONS:
            block_id = block["id"]
            block_name = block["name"]
            filename = f"{block_id}.svg"
            filepath = os.path.join(theme_subfolder, filename)

            try:
                svg_content = block["generate"](style, theme)
                validate_svg(svg_content)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(svg_content)
                print(f"    [OK] {block_name} ({filename})")
                rendered_items.append({
                    "theme": theme,
                    "theme_name": theme_name,
                    "style": style,
                    "block_id": block_id,
                    "block_name": block_name,
                    "category": block["category"],
                    "directive": block["directive"],
                    "rel_path": f"{theme}/{filename}"
                })
            except Exception as e:
                print(f"    [ERR] {block_name} failed: {e}")
                sys.exit(1)

    print(f"[+] All {len(rendered_items)} SVGs generated successfully!")

    # Build Standalone Interactive HTML Gallery
    generate_html_gallery(gallery_dir, rendered_items)


def generate_html_gallery(gallery_dir, items):
    html_path = os.path.join(gallery_dir, "index.html")

    categories = sorted(list(set(i["category"] for i in items)))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pixel Readme Kit — Block & Theme Gallery Stand</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --surface: #0f172a;
      --surface-border: #1e293b;
      --text-main: #f8fafc;
      --text-dim: #94a3b8;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.2);
      --card-bg: #111827;
      --preview-bg: #0d1117;
    }}
    body[data-canvas-mode="light"] {{
      --preview-bg: #ffffff;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg);
      color: var(--text-main);
      padding: 32px 24px;
      line-height: 1.5;
    }}
    .gallery-container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    header.header {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 32px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--surface-border);
    }}
    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .title-group h1 {{
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #fff;
    }}
    .title-group p {{
      font-size: 14px;
      color: var(--text-dim);
      margin-top: 4px;
    }}
    .global-controls {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .btn {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #f1f5f9;
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: #334155;
      border-color: #475569;
    }}
    .btn.active {{
      background: var(--accent);
      color: #090d16;
      border-color: var(--accent);
    }}
    .filter-bar {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      padding: 16px;
      border-radius: 10px;
      margin-bottom: 32px;
    }}
    .filter-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .filter-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      text-transform: uppercase;
      color: var(--text-dim);
      min-width: 90px;
      font-weight: 600;
    }}
    .theme-pills, .category-pills {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .pill {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .pill:hover {{
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }}
    .pill.active {{
      background: #38bdf8;
      color: #090d16;
      border-color: #38bdf8;
    }}
    .stats-bar {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: var(--text-dim);
      margin-bottom: 20px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 32px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 20px;
      background: rgba(15, 23, 42, 0.7);
      border-bottom: 1px solid var(--surface-border);
    }}
    .card-title-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .card-title {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }}
    .badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .badge-theme {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .badge-cat {{
      background: rgba(148, 163, 184, 0.15);
      color: #94a3b8;
    }}
    .card-actions {{
      display: flex;
      gap: 8px;
    }}
    .card-body {{
      padding: 24px;
      background: var(--preview-bg);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 120px;
      transition: background 0.2s ease;
      overflow-x: auto;
    }}
    .card-body img {{
      max-width: 100%;
      height: auto;
      display: block;
    }}
    .card-footer {{
      padding: 12px 20px;
      background: #090d16;
      border-top: 1px solid var(--surface-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .directive-snippet {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #94a3b8;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      flex: 1;
    }}
    .copy-btn {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      background: #1e293b;
      border: 1px solid #334155;
      color: #f1f5f9;
      padding: 5px 10px;
      border-radius: 4px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
    }}
    .copy-btn:hover {{
      background: #38bdf8;
      color: #090d16;
      border-color: #38bdf8;
    }}
  </style>
</head>
<body>
  <div class="gallery-container">
    <header class="header">
      <div class="header-top">
        <div class="title-group">
          <h1>Pixel Readme Kit — Multi-Theme Visual Stand</h1>
          <p>Full inspection of all 16 component blocks across 5 canonical geometric themes.</p>
        </div>
        <div class="global-controls">
          <button class="btn active" id="btn-mode-dark" onclick="setCanvasMode('dark')">GitHub Dark</button>
          <button class="btn" id="btn-mode-light" onclick="setCanvasMode('light')">GitHub Light</button>
        </div>
      </div>
    </header>

    <div class="filter-bar">
      <div class="filter-row">
        <div class="filter-label">Theme:</div>
        <div class="theme-pills">
          <button class="pill active" onclick="filterByTheme('all', this)">ALL THEMES (5)</button>
          <button class="pill" onclick="filterByTheme('cyberpunk', this)">CYBERPUNK</button>
          <button class="pill" onclick="filterByTheme('tactical', this)">TACTICAL</button>
          <button class="pill" onclick="filterByTheme('minimal', this)">MINIMAL</button>
          <button class="pill" onclick="filterByTheme('modern-clean', this)">MODERN CLEAN</button>
          <button class="pill" onclick="filterByTheme('rough-doodle', this)">ROUGH DOODLE</button>
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-label">Block Type:</div>
        <div class="category-pills">
          <button class="pill active" onclick="filterByBlock('all', this)">ALL BLOCKS (16)</button>
"""

    for b in BLOCK_DEFINITIONS:
        html_content += f"""          <button class="pill" onclick="filterByBlock('{b['id']}', this)">{b['name']}</button>\n"""

    html_content += f"""        </div>
      </div>
    </div>

    <div class="stats-bar" id="stats-counter">Showing {len(items)} of {len(items)} rendered components</div>

    <div class="grid" id="gallery-grid">
"""

    for item in items:
        directive_escaped = item['directive'].replace('"', '&quot;').replace('\n', '&#10;')
        html_content += f"""      <div class="card" data-theme="{item['theme']}" data-block="{item['block_id']}" data-category="{item['category']}">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-title">{item['block_name']}</span>
            <span class="badge badge-theme">{item['theme_name']}</span>
            <span class="badge badge-cat">{item['category']}</span>
          </div>
          <div class="card-actions">
            <a href="{item['rel_path']}" target="_blank" class="copy-btn">Open SVG</a>
          </div>
        </div>
        <div class="card-body">
          <img src="{item['rel_path']}" alt="{item['block_name']} ({item['theme_name']})" loading="lazy" />
        </div>
        <div class="card-footer">
          <div class="directive-snippet">{item['directive'].splitlines()[0]}</div>
          <button class="copy-btn" onclick="copySnippet(this, `{directive_escaped}`)">Copy Directive</button>
        </div>
      </div>\n"""

    html_content += """    </div>
  </div>

  <script>
    let currentThemeFilter = "all";
    let currentBlockFilter = "all";

    function setCanvasMode(mode) {
      document.body.setAttribute("data-canvas-mode", mode);
      document.getElementById("btn-mode-dark").classList.toggle("active", mode === "dark");
      document.getElementById("btn-mode-light").classList.toggle("active", mode === "light");
    }

    function filterByTheme(theme, btn) {
      currentThemeFilter = theme;
      document.querySelectorAll(".theme-pills .pill").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      applyFilters();
    }

    function filterByBlock(blockId, btn) {
      currentBlockFilter = blockId;
      document.querySelectorAll(".category-pills .pill").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      applyFilters();
    }

    function applyFilters() {
      const cards = document.querySelectorAll("#gallery-grid .card");
      let visibleCount = 0;
      cards.forEach(card => {
        const cTheme = card.getAttribute("data-theme");
        const cBlock = card.getAttribute("data-block");
        const matchTheme = (currentThemeFilter === "all" || currentThemeFilter === cTheme);
        const matchBlock = (currentBlockFilter === "all" || currentBlockFilter === cBlock);
        if (matchTheme && matchBlock) {
          card.style.display = "block";
          visibleCount++;
        } else {
          card.style.display = "none";
        }
      });
      document.getElementById("stats-counter").innerText = `Showing ${visibleCount} of ${cards.length} rendered components`;
    }

    function copySnippet(btn, code) {
      navigator.clipboard.writeText(code).then(() => {
        const orig = btn.innerText;
        btn.innerText = "COPIED!";
        btn.style.background = "#10b981";
        btn.style.color = "#090d16";
        setTimeout(() => {
          btn.innerText = orig;
          btn.style.background = "";
          btn.style.color = "";
        }, 1500);
      });
    }
  </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] HTML Showcase written to: {html_path}")


if __name__ == "__main__":
    render_all_gallery()
