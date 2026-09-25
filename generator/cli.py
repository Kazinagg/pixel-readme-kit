"""
CLI Generator for Pixel Readme Kit v2.0
Builds SVG assets across multiple styles, themes, and animations.
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
    build_header_terminal,
    build_header_tactical,
    build_header_minimal,
    build_frame_top,
    build_frame_bottom,
    build_side_rail,
    build_chip,
    build_pcb_divider,
    build_laser_divider
)

def build_kit(output_dir, theme_name="cyberpunk", title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM", header_style="terminal"):
    os.makedirs(output_dir, exist_ok=True)
    assets_dir = os.path.join(output_dir, "assets")
    chips_dir = os.path.join(assets_dir, "chips")
    rails_dir = os.path.join(assets_dir, "rails")
    frames_dir = os.path.join(assets_dir, "frames")
    headers_dir = os.path.join(assets_dir, "headers")

    for d in [assets_dir, chips_dir, rails_dir, frames_dir, headers_dir]:
        os.makedirs(d, exist_ok=True)

    theme = get_theme(theme_name)
    primary = theme["primary"]
    secondary = theme["secondary"]
    success = theme["success"]
    warning = theme["warning"]

    print(f"Building Pixel Readme Kit with theme: {theme['name']} (style: {header_style})")

    # 1. Main Header with 3D Pixel Font
    specs = [
        ("HUD ARCHITECTURE", "TRANSLUCENT GLASS & CYBER BRACKETS", primary),
        ("TEXT INTEGRATION", "100% COPYABLE MARKDOWN & MATH", secondary),
        ("ANIMATION SUITE", "RADAR // SCANLINE // LADDER CASCADE", success)
    ]
    header_svg = build_header(
        title=title,
        subtitle=subtitle,
        specs=specs,
        theme=theme,
        style=header_style
    )

    # Insert 3D pixel letters into header
    y_text = 65 if header_style == "terminal" else (55 if header_style == "tactical" else 42)
    px_sz = 6 if header_style == "terminal" else (5 if header_style == "tactical" else 4)
    text_3d, _, _ = render_3d_text(
        title, x=42, y=y_text, px_size=px_sz,
        front_color=primary,
        mid_shadow=theme["shadow_mid"],
        dark_shadow=theme["shadow_dark"]
    )
    header_svg = header_svg.replace("</defs>", f"</defs>\n  {text_3d}")
    with open(os.path.join(assets_dir, "header.svg"), "w", encoding="utf-8") as f:
        f.write(header_svg)
    print("  [+] Generated assets/header.svg")

    # 2. Dividers
    div_pcb = build_pcb_divider(theme)
    div_laser = build_laser_divider(theme)
    with open(os.path.join(assets_dir, "divider.svg"), "w", encoding="utf-8") as f:
        f.write(div_pcb)
    with open(os.path.join(assets_dir, "divider-laser.svg"), "w", encoding="utf-8") as f:
        f.write(div_laser)
    print("  [+] Generated divider.svg & divider-laser.svg")

    # 3. Window Frames: Brackets, Chamfer, Enclosure
    # Mode A: Cyber Brackets (Fixed downward vertical prongs)
    fb_top = build_frame_top("╔═ SYSTEM.CORE // RUNTIME_KERNEL.SYS", "OPEN_HUD", primary, theme, style="brackets")
    fb_bot = build_frame_bottom("SYS: OK // BUFFER_STREAM_ACTIVE", primary, theme, style="brackets")
    with open(os.path.join(assets_dir, "frame-top-brackets.svg"), "w", encoding="utf-8") as f:
        f.write(fb_top)
    with open(os.path.join(assets_dir, "frame-bottom.svg"), "w", encoding="utf-8") as f:
        f.write(fb_bot)

    # Mode B: Full Box Enclosure (Flush sockets)
    fe_top = build_frame_top("╔═ HUD.BOX // FULL_ENCLOSURE_SIDE_RAILS.EXE", "FULL_BOX", warning, theme, style="enclosure")
    fe_bot = build_frame_bottom("TELEMETRY: NOMINAL // ALL_SYSTEMS_GO", warning, theme, style="enclosure")
    with open(os.path.join(assets_dir, "frame-top-enclosure.svg"), "w", encoding="utf-8") as f:
        f.write(fe_top)

    print("  [+] Generated frame-top-brackets.svg, frame-top-enclosure.svg, frame-bottom.svg")

    # 4. Side Rails: Ladder & Laser
    rail_l = build_side_rail(180, color=warning, theme=theme, side="left", style="ladder")
    rail_r = build_side_rail(180, color=warning, theme=theme, side="right", style="ladder")
    with open(os.path.join(assets_dir, "rail-left.svg"), "w", encoding="utf-8") as f:
        f.write(rail_l)
    with open(os.path.join(assets_dir, "rail-right.svg"), "w", encoding="utf-8") as f:
        f.write(rail_r)
    print("  [+] Generated rail-left.svg, rail-right.svg")

    # 5. Chips: Closed, Chamfer, Decay-Right, Decay-Left, Pulse
    chips_spec = [
        ("chip-closed-core.svg", "📁 generator/", primary, "closed", 125),
        ("chip-closed-cli.svg", "⚡ cli.py", secondary, "closed", 100),
        ("chip-closed-github.svg", "⚡ GitHub Repo", success, "closed", 130),
        ("chip-chamfer-spec.svg", "⚙️ ARCH_v2", warning, "chamfer", 115),
        ("chip-decay-right-src.svg", "📁 src/", primary, "decay_right", 115),
        ("chip-decay-right-tag.svg", "🏷️ v2.0", secondary, "decay_right", 105),
        ("chip-decay-right-done.svg", "✅ READY", success, "decay_right", 110),
        ("chip-decay-left-docs.svg", "📄 DOCS", primary, "decay_left", 110),
        ("chip-decay-left-spec.svg", "⚙️ SPEC", warning, "decay_left", 110),
        ("chip-pulse-live.svg", "🔴 LIVE STREAM", theme["accent"], "pulse", 145),
        ("chip-pulse-online.svg", "🟢 SYS: ONLINE", success, "pulse", 135),
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

    print("\n[+] Kit assets built successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Pixel Readme Kit Assets")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--theme", default="cyberpunk", choices=list(THEMES.keys()), help="Color theme")
    parser.add_argument("--style", default="terminal", choices=["terminal", "tactical", "minimal"], help="Header style")
    parser.add_argument("--title", default="PIXEL-KIT", help="Main 3D Title")
    parser.add_argument("--subtitle", default="TRANSLUCENT HUD DESIGN SYSTEM", help="Subtitle")
    args = parser.parse_args()

    build_kit(args.output, args.theme, args.title, args.subtitle, args.style)
