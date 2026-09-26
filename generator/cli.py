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
    build_laser_divider,
    build_bullet_icon,
    build_footer,
    build_callout
)

def build_kit(output_dir, theme_name="cyberpunk", title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM", header_style="terminal"):
    os.makedirs(output_dir, exist_ok=True)
    assets_dir = os.path.join(output_dir, "assets")
    chips_dir = os.path.join(assets_dir, "chips")
    rails_dir = os.path.join(assets_dir, "rails")
    frames_dir = os.path.join(assets_dir, "frames")
    headers_dir = os.path.join(assets_dir, "headers")
    footers_dir = os.path.join(assets_dir, "footers")
    bullets_dir = os.path.join(assets_dir, "bullets")
    callouts_dir = os.path.join(assets_dir, "callouts")

    for d in [assets_dir, chips_dir, rails_dir, frames_dir, headers_dir, footers_dir, bullets_dir, callouts_dir]:
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

    # 3. Window Frames: Brackets, Chamfer, Enclosure, Minimal, Table Minimal
    # Root assets
    fb_top = build_frame_top("╔═ SYSTEM.CORE // RUNTIME_KERNEL.SYS", "OPEN_HUD", primary, theme, style="brackets")
    fb_bot = build_frame_bottom("SYS: OK // BUFFER_STREAM_ACTIVE", primary, theme, style="brackets")
    fe_top = build_frame_top("╔═ HUD.BOX // FULL_ENCLOSURE_SIDE_RAILS.EXE", "FULL_BOX", warning, theme, style="enclosure")
    fa_top = build_frame_top("╔═ SYSTEM.CORE // ARCHITECTURE_SPEC.SYS", "TRANSLUCENT", "#00F0FF", get_theme("cyberpunk"), style="brackets")
    fc_top = build_frame_top("╔═ INVENTORY // HOLOGRAPHIC_CHIP_VARIANTS.SYS", "CHIPS_V2", "#39FF14", get_theme("matrix"), style="brackets")
    fg_top = build_frame_top("╔═ DEPLOYMENT // SYSTEM_INTEGRATION_GUIDE.SYS", "GUIDE_V2", "#FF0055", get_theme("cyberpunk"), style="brackets")

    with open(os.path.join(assets_dir, "frame-top-brackets.svg"), "w", encoding="utf-8") as f:
        f.write(fb_top)
    with open(os.path.join(assets_dir, "frame-bottom.svg"), "w", encoding="utf-8") as f:
        f.write(fb_bot)
    with open(os.path.join(assets_dir, "frame-top-enclosure.svg"), "w", encoding="utf-8") as f:
        f.write(fe_top)
    with open(os.path.join(assets_dir, "frame-top-architecture.svg"), "w", encoding="utf-8") as f:
        f.write(fa_top)
    with open(os.path.join(assets_dir, "frame-top-chips.svg"), "w", encoding="utf-8") as f:
        f.write(fc_top)
    with open(os.path.join(assets_dir, "frame-top-guide.svg"), "w", encoding="utf-8") as f:
        f.write(fg_top)

    # Suite of themed frames in assets/frames/
    frames_catalog = [
        ("frame-top-brackets-green.svg", "╔═ SYSTEM.CORE // MATRIX_STREAM.SYS", "MATRIX_HUD", "#00D26A", get_theme("matrix"), "brackets", True),
        ("frame-bottom-brackets-green.svg", "", "SYS: ONLINE // BUFFER_STREAM_ACTIVE", "#00D26A", get_theme("matrix"), "brackets", False),
        ("frame-top-chamfer-amber.svg", "╔═ HUD.CHAMFER // TACTICAL_ENCLOSURE.EXE", "TACTICAL", "#F59E0B", get_theme("amber"), "chamfer", True),
        ("frame-bottom-chamfer-amber.svg", "", "ENCLOSURE_BUFFER // ACTIVE", "#F59E0B", get_theme("amber"), "chamfer", False),
        ("frame-top-enclosure-cyan.svg", "╔═ HUD.BOX // FULL_ENCLOSURE_SIDE_RAILS.EXE", "FULL_BOX", "#00C8D7", get_theme("cyberpunk"), "enclosure", True),
        ("frame-bottom-enclosure-cyan.svg", "", "SYS: OK // BUFFER_END // THREAD_01", "#00C8D7", get_theme("cyberpunk"), "enclosure", False),
        ("frame-top-minimal-tokyo.svg", "╔═ SYNTH.RAIL // TOKYO_NIGHT_SESSION.SYS", "SESSION", "#4F8BFF", get_theme("tokyo"), "minimal", True),
        ("frame-bottom-minimal-tokyo.svg", "", "TOKYO_HUD // BUFFER_SYNC_OK", "#4F8BFF", get_theme("tokyo"), "minimal", False),
        # Trial Table-Minimal style for Variant 2B (Integrated Table HUD Plate)
        ("frame-top-table-minimal.svg", "╔═ HUD.TABLE // INTEGRATED_MONOLITH.SYS", "TABLE_HUD", "#00D26A", get_theme("matrix"), "table_minimal", True),
        ("frame-bottom-table-minimal.svg", "", "INTEGRATED_TABLE // BUFFER_PASS", "#00D26A", get_theme("matrix"), "table_minimal", False),
        ("frame-top-table-minimal-cyan.svg", "╔═ HUD.TABLE // INTEGRATED_MONOLITH.SYS", "CYBER_TABLE", "#00C8D7", get_theme("cyberpunk"), "table_minimal", True),
        ("frame-bottom-table-minimal-cyan.svg", "", "INTEGRATED_TABLE // BUFFER_PASS", "#00C8D7", get_theme("cyberpunk"), "table_minimal", False),
        # Interactive Collapsible Drawer Style for <details><summary> (Architecture IV)
        ("frame-top-collapsible-cyan.svg", "╔═ INTERACTIVE.TERMINAL // CLICK_TO_TOGGLE.SYS", "▶ TOGGLE", "#00C8D7", get_theme("cyberpunk"), "collapsible", True),
        ("frame-top-collapsible-amber.svg", "╔═ TACTICAL.DRAWER // CLICK_TO_TOGGLE.SYS", "▶ TOGGLE", "#F59E0B", get_theme("amber"), "collapsible", True),
        ("frame-top-collapsible-green.svg", "╔═ MATRIX.DRAWER // CLICK_TO_TOGGLE.SYS", "▶ TOGGLE", "#00D26A", get_theme("matrix"), "collapsible", True),
    ]

    for fname, ftitle, ftag, fcol, ftheme, fstyle, is_top in frames_catalog:
        if is_top:
            fsvg = build_frame_top(ftitle, ftag, fcol, ftheme, style=fstyle)
        else:
            fsvg = build_frame_bottom(ftag, fcol, ftheme, style=fstyle)
        with open(os.path.join(frames_dir, fname), "w", encoding="utf-8") as f:
            f.write(fsvg)
        print(f"  [+] Generated frame: {fname} ({fstyle})")

    print("  [+] Generated all root & themed frame assets")

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
        ("nav-catalog.svg", "📚 КАТАЛОГ", primary, "closed", 130),
        ("nav-guide.svg", "🚀 ИНСТРУКЦИЯ", primary, "closed", 140),
    ]

    for cname, ctext, ccol, cstyle, cwidth in chips_spec:
        svg = build_chip(ctext, ccol, theme, style=cstyle, width=cwidth)
        with open(os.path.join(chips_dir, cname), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  [+] Generated chip: {cname} ({cstyle})")

    # 6. Master Footers (Closing Plates across themes)
    footer_curr = build_footer(style=header_style, theme=theme)
    with open(os.path.join(assets_dir, "footer.svg"), "w", encoding="utf-8") as f:
        f.write(footer_curr)

    footers_spec = [
        ("footer-terminal-cyberpunk.svg", "terminal", "SYSTEM_STANDBY // 0xDEADBEEF", get_theme("cyberpunk")),
        ("footer-tactical-amber.svg", "tactical", "CLASSIFIED // SECTOR_CLEAR", get_theme("amber")),
        ("footer-minimal-tokyo.svg", "minimal", "TOKYO_VAPORWAVE // HUD v2.2", get_theme("tokyo")),
        ("footer-matrix-green.svg", "matrix", "CONNECTION TERMINATED // BUFFER_FLUSHED", get_theme("matrix")),
    ]
    for fname, fstyle, fstatus, ftheme in footers_spec:
        fsvg = build_footer(style=fstyle, status=fstatus, theme=ftheme)
        with open(os.path.join(footers_dir, fname), "w", encoding="utf-8") as f:
            f.write(fsvg)
        print(f"  [+] Generated footer: {fname}")

    # 7. Pixel Bullet Icons (14x14)
    bullets_spec = [
        # Cyberpunk
        ("bullet-diamond-cyan.svg", "diamond", "#00C8D7", get_theme("cyberpunk")),
        ("bullet-arrow-pink.svg", "arrow", "#FF0055", get_theme("cyberpunk")),
        ("bullet-marker-cyan.svg", "marker", "#00C8D7", get_theme("cyberpunk")),
        ("bullet-check-cyan.svg", "check", "#00C8D7", get_theme("cyberpunk")),
        # Tactical
        ("bullet-chevron-amber.svg", "chevron", "#F59E0B", get_theme("amber")),
        ("bullet-plus-amber.svg", "plus", "#F59E0B", get_theme("amber")),
        ("bullet-minus-amber.svg", "minus", "#F59E0B", get_theme("amber")),
        ("bullet-alert-amber.svg", "alert", "#F59E0B", get_theme("amber")),
        ("bullet-stripe-amber.svg", "stripe", "#EA580C", get_theme("amber")),
        # Matrix
        ("bullet-square-green.svg", "square", "#00D26A", get_theme("matrix")),
        ("bullet-dither-light-green.svg", "dither_light", "#00D26A", get_theme("matrix")),
        ("bullet-dither-med-green.svg", "dither_med", "#00D26A", get_theme("matrix")),
        ("bullet-dither-dark-green.svg", "dither_dark", "#00D26A", get_theme("matrix")),
        ("bullet-prompt-green.svg", "prompt", "#00D26A", get_theme("matrix")),
        # Tokyo
        ("bullet-star-blue.svg", "star", "#4F8BFF", get_theme("tokyo")),
        ("bullet-diamond-purple.svg", "diamond_nested", "#A855F7", get_theme("tokyo")),
    ]
    for bname, bsymbol, bcolor, btheme in bullets_spec:
        bsvg = build_bullet_icon(symbol=bsymbol, color=bcolor, theme=btheme, size=14)
        with open(os.path.join(bullets_dir, bname), "w", encoding="utf-8") as f:
            f.write(bsvg)
        print(f"  [+] Generated bullet: {bname}")

    # 8. Inline Callouts, Quotes & Alerts
    callouts_spec = [
        ("callout-note-cyan.svg", "note", "SYSTEM ARCHITECTURE NOTICE // SPECIFICATION", "Dual-theme contrast > 7:1 // Markdown & LaTeX copyable", get_theme("cyberpunk")),
        ("callout-warning-amber.svg", "warning", "CAUTION: CAMO PROXY & TABLE PADDING RESTRICTIONS", "Enforce 54px rails to prevent image compression", get_theme("amber")),
        ("callout-critical-magenta.svg", "critical", "FATAL EXCEPTION // EMERGENCY OVERRIDE ENGAGED", "XML unescaped ampersands will break Camo proxy", get_theme("cyberpunk")),
        ("callout-success-green.svg", "success", "ALL SYSTEMS NOMINAL // 100% XML VALIDATED", "Zero Camo proxy errors // Ready for deployment", get_theme("matrix")),
    ]
    for cname, ctype, ctitle, cmsg, ctheme in callouts_spec:
        csvg = build_callout(callout_type=ctype, title=ctitle, message=cmsg, theme=ctheme)
        with open(os.path.join(callouts_dir, cname), "w", encoding="utf-8") as f:
            f.write(csvg)
        print(f"  [+] Generated callout: {cname}")

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
