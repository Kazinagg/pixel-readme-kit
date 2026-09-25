"""
CLI Generator for Pixel Readme Kit
Builds all SVG assets and assembles README.md based on theme config.
"""

import os
import sys
import argparse

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from palettes import get_theme, THEMES
from font_engine import render_3d_text
from builder import (
    build_header,
    build_frame_top,
    build_frame_bottom,
    build_side_rail,
    build_chip,
    build_pcb_divider
)

def build_kit(output_dir, theme_name="cyberpunk", title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM"):
    os.makedirs(output_dir, exist_ok=True)
    assets_dir = os.path.join(output_dir, "assets")
    chips_dir = os.path.join(assets_dir, "chips")
    os.makedirs(chips_dir, exist_ok=True)

    theme = get_theme(theme_name)
    primary = theme["primary"]
    secondary = theme["secondary"]
    success = theme["success"]
    warning = theme["warning"]

    print(f"Building Pixel Readme Kit with theme: {theme['name']}")

    # 1. Main Header with 3D Pixel Font
    header_svg = build_header(
        title=title,
        subtitle=subtitle,
        specs=[
            ("HUD ARCHITECTURE", "TRANSLUCENT GLASS & CYBER BRACKETS", primary),
            ("TEXT INTEGRATION", "100% COPYABLE MARKDOWN & MATH", secondary),
            ("CHIP VARIATIONS", "CLOSED & DISSOLVING PIXEL DECAY", success)
        ],
        theme=theme
    )
    # Insert 3D pixel letters into header
    text_3d, w_text, h_text = render_3d_text(
        title, x=42, y=65, px_size=6,
        front_color=primary,
        mid_shadow=theme["shadow_mid"],
        dark_shadow=theme["shadow_dark"]
    )
    header_svg = header_svg.replace('</defs>', f'</defs>\n  {text_3d}')
    with open(os.path.join(assets_dir, "header.svg"), "w", encoding="utf-8") as f:
        f.write(header_svg)
    print("  [+] Generated header.svg")

    # 2. PCB Divider
    divider_svg = build_pcb_divider(theme)
    with open(os.path.join(assets_dir, "divider.svg"), "w", encoding="utf-8") as f:
        f.write(divider_svg)
    print("  [+] Generated divider.svg")

    # 3. Window Top Frames (Cyber Brackets with downward accents)
    frames = [
        ("frame-top-architecture.svg", "╔═ SYSTEM.CORE // ARCHITECTURE_SPEC.SYS", "TRANSLUCENT", primary),
        ("frame-top-brackets.svg", "╔═ HUD.BRACKETS // SEAMLESS_OPEN_FRAMING.EXE", "OPEN_HUD", secondary),
        ("frame-top-enclosure.svg", "╔═ HUD.BOX // FULL_ENCLOSURE_SIDE_RAILS.EXE", "FULL_BOX", warning),
        ("frame-top-chips.svg", "╔═ INVENTORY // HOLOGRAPHIC_CHIP_VARIANTS.SYS", "CHIPS_V2", success),
        ("frame-top-guide.svg", "╔═ DEV.GUIDE // QUICK_START_INTEGRATION.PY", "DOCUMENTATION", primary),
    ]
    for fname, ftitle, ftag, fcol in frames:
        svg = build_frame_top(ftitle, ftag, fcol, theme, open_bracket=True)
        with open(os.path.join(assets_dir, fname), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  [+] Generated {fname}")

    # 4. Window Bottom Frame (with upward accents)
    bottom_svg = build_frame_bottom("SYS: OK // BUFFER_END // THREAD_01", primary, theme, open_bracket=True)
    with open(os.path.join(assets_dir, "frame-bottom.svg"), "w", encoding="utf-8") as f:
        f.write(bottom_svg)
    print("  [+] Generated frame-bottom.svg")

    # 5. Side Rails for Full Box Enclosure Mode
    rail_l = build_side_rail(height=180, color=warning, theme=theme, side="left")
    rail_r = build_side_rail(height=180, color=warning, theme=theme, side="right")
    with open(os.path.join(assets_dir, "rail-left.svg"), "w", encoding="utf-8") as f:
        f.write(rail_l)
    with open(os.path.join(assets_dir, "rail-right.svg"), "w", encoding="utf-8") as f:
        f.write(rail_r)
    print("  [+] Generated side rails (rail-left.svg, rail-right.svg)")

    # 6. Chips: Closed, Decay-Right, Decay-Left
    chips_spec = [
        # Closed
        ("chip-closed-core.svg", "📁 generator/", primary, "closed", 125),
        ("chip-closed-cli.svg", "⚡ cli.py", secondary, "closed", 100),
        ("chip-closed-yaml.svg", "📄 config.yaml", warning, "closed", 130),
        ("chip-closed-github.svg", "⚡ GitHub Repo", success, "closed", 130),

        # Decay-Right (Dissolving into subsequent text)
        ("chip-decay-right-src.svg", "📁 src/", primary, "decay_right", 115),
        ("chip-decay-right-tag.svg", "🏷️ v2.0", secondary, "decay_right", 105),
        ("chip-decay-right-done.svg", "✅ READY", success, "decay_right", 110),

        # Decay-Left (Emerging from preceding text)
        ("chip-decay-left-docs.svg", "📄 DOCS", primary, "decay_left", 110),
        ("chip-decay-left-spec.svg", "⚙️ SPEC", warning, "decay_left", 110),

        # Navigation Chips
        ("nav-arch.svg", "🏛️ АРХИТЕКТУРА", primary, "closed", 140),
        ("nav-brackets.svg", "📐 СКОБЫ HUD", secondary, "closed", 135),
        ("nav-enclosure.svg", "📦 ПОЛНЫЙ БОКС", warning, "closed", 140),
        ("nav-chips.svg", "💎 ЧИПЫ", success, "closed", 110),
        ("nav-guide.svg", "🚀 ИНСТРУКЦИЯ", primary, "closed", 140),
    ]

    for cname, ctext, ccol, cstyle, cwidth in chips_spec:
        svg = build_chip(ctext, ccol, theme, style=cstyle, width=cwidth)
        with open(os.path.join(chips_dir, cname), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  [+] Generated chip: {cname} ({cstyle})")

    print("\nAll assets built successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Pixel Readme Kit Assets")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--theme", default="cyberpunk", choices=list(THEMES.keys()), help="Color theme")
    parser.add_argument("--title", default="PIXEL-KIT", help="Main 3D Title")
    parser.add_argument("--subtitle", default="TRANSLUCENT HUD DESIGN SYSTEM", help="Subtitle")
    args = parser.parse_args()

    build_kit(args.output, args.theme, args.title, args.subtitle)
