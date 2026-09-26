"""
CLI Generator & Compiler for Pixel Readme Kit v2.2
Usage modes:
1. Generate individual SVG blocks:
   python -m generator.cli header --help
   python -m generator.cli footer --help
   python -m generator.cli callout --help
   python -m generator.cli frame --help
   python -m generator.cli chip --help
   python -m generator.cli divider --help
   python -m generator.cli splitter --help

2. Compile README markdown template with pixel-kit directives:
   python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
"""

import os
import sys
import argparse

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.engine import (
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    validate_svg
)
from generator.compiler import MarkdownCompiler

def cmd_header(args):
    svg = generate_header(
        style=args.style,
        primary=args.primary,
        accent=args.accent,
        title=args.title,
        subtitle=args.subtitle,
        tag=args.tag
    )
    save_output(svg, args.output, f"assets/header-{args.style}.svg")

def cmd_footer(args):
    svg = generate_footer(
        style=args.style,
        primary=args.primary,
        accent=args.accent,
        status=args.status,
        nav_text=args.nav
    )
    save_output(svg, args.output, f"assets/footer-{args.style}.svg")

def cmd_callout(args):
    svg = generate_callout(
        style=args.style,
        primary=args.primary,
        accent=args.accent,
        callout_type=args.type,
        title=args.title,
        subtitle=args.subtitle,
        is_quote=args.quote
    )
    prefix = "callout-quote" if args.quote else "callout"
    save_output(svg, args.output, f"assets/{prefix}-{args.style}-{args.type}.svg")

def cmd_frame(args):
    svg = generate_frame(
        style=args.style,
        primary=args.primary,
        accent=args.accent,
        frame_type=args.type,
        title=args.title,
        tag=args.tag
    )
    save_output(svg, args.output, f"assets/frame-{args.type}-{args.style}.svg")

def cmd_chip(args):
    svg = generate_chip(
        style=args.style,
        primary=args.primary,
        accent=args.accent,
        chip_type=args.type,
        text=args.text
    )
    save_output(svg, args.output, f"assets/chip-{args.style}-{args.type}.svg")

def cmd_divider(args):
    svg = generate_divider(
        style=args.style,
        primary=args.primary,
        accent=args.accent
    )
    save_output(svg, args.output, f"assets/divider-{args.style}.svg")

def cmd_splitter(args):
    svg = generate_splitter(
        style=args.style,
        primary=args.primary,
        accent=args.accent,
        label=args.label
    )
    save_output(svg, args.output, f"assets/splitter-{args.style}.svg")

def cmd_compile(args):
    print(f"[*] Compiling Markdown template: {args.input}")
    print(f"[*] Assets directory: {args.assets_dir}")
    compiler = MarkdownCompiler(assets_dir=args.assets_dir)
    compiler.compile_file(args.input, args.output)
    print(f"[+] Successfully compiled to: {args.output}")

def save_output(svg_content, output_path, default_path):
    target = output_path if output_path else default_path
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    validate_svg(svg_content)
    with open(target, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated SVG successfully: {target}")

def main():
    parser = argparse.ArgumentParser(
        prog="pixel-kit",
        description="Pixel Readme Kit v2.2 — Cyberpunk / Tactical / Minimal HUD Generator & Markdown Compiler"
    )

    subparsers = parser.add_subparsers(dest="command", help="Block type or compiler action")

    # 1. HEADER
    p_hdr = subparsers.add_parser("header", help="Generate flagship header banner")
    p_hdr.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style (cyberpunk, tactical, minimal)")
    p_hdr.add_argument("--primary", help="Primary brand hex color (e.g. #00C8D7, #F59E0B, #4F8BFF)")
    p_hdr.add_argument("--accent", help="Secondary accent hex color (e.g. #A855F7, #EA580C)")
    p_hdr.add_argument("--title", default="PIXEL-KIT", help="Main title text")
    p_hdr.add_argument("--subtitle", default="TRANSLUCENT HUD DESIGN SYSTEM", help="Subtitle description text")
    p_hdr.add_argument("--tag", default="SYSTEM_ACTIVE", help="Top badge tag text")
    p_hdr.add_argument("--output", "-o", help="Target SVG destination path")
    p_hdr.set_defaults(func=cmd_header)

    # 2. FOOTER
    p_ftr = subparsers.add_parser("footer", help="Generate full-width closing footer plate")
    p_ftr.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_ftr.add_argument("--primary", help="Primary brand hex color")
    p_ftr.add_argument("--accent", help="Secondary accent hex color")
    p_ftr.add_argument("--status", default="SESSION_ACTIVE // STANDBY", help="Status telemetry readout text")
    p_ftr.add_argument("--nav", default="RETURN TO TOP", help="Navigation button text")
    p_ftr.add_argument("--output", "-o", help="Target SVG destination path")
    p_ftr.set_defaults(func=cmd_footer)

    # 3. CALLOUT
    p_clt = subparsers.add_parser("callout", help="Generate inline alert plate or quote header")
    p_clt.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_clt.add_argument("--type", choices=["note", "warning", "critical", "success", "info"], default="note", help="Callout type / badge")
    p_clt.add_argument("--primary", help="Primary brand hex color")
    p_clt.add_argument("--accent", help="Secondary accent hex color")
    p_clt.add_argument("--title", default="SYSTEM ARCHITECTURE NOTICE", help="Callout header title text")
    p_clt.add_argument("--subtitle", default="Dual-theme contrast > 7:1 // Monospace typography", help="Callout subtext message")
    p_clt.add_argument("--quote", action="store_true", help="Generate quote header sub-variant (open left edge + dashed bottom line)")
    p_clt.add_argument("--output", "-o", help="Target SVG destination path")
    p_clt.set_defaults(func=cmd_callout)

    # 4. FRAME
    p_frm = subparsers.add_parser("frame", help="Generate window top cap or bottom plate")
    p_frm.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_frm.add_argument("--type", choices=["top", "bottom"], default="top", help="Frame position: top or bottom")
    p_frm.add_argument("--primary", help="Primary brand hex color")
    p_frm.add_argument("--accent", help="Secondary accent hex color")
    p_frm.add_argument("--title", default="╔═ SYSTEM.CORE // RUNTIME.SYS", help="Window title text (for top frame)")
    p_frm.add_argument("--tag", default="[OPEN_HUD]", help="Window tag text (for top frame)")
    p_frm.add_argument("--output", "-o", help="Target SVG destination path")
    p_frm.set_defaults(func=cmd_frame)

    # 5. CHIP
    p_chp = subparsers.add_parser("chip", help="Generate holographic pill / chip badge")
    p_chp.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_chp.add_argument("--type", choices=["closed", "decay", "pulse"], default="closed", help="Form & decay mechanics: closed, decay, pulse")
    p_chp.add_argument("--primary", help="Primary brand hex color")
    p_chp.add_argument("--accent", help="Secondary accent hex color")
    p_chp.add_argument("--text", default="CHIP_TAG", help="Text label inside the chip")
    p_chp.add_argument("--output", "-o", help="Target SVG destination path")
    p_chp.set_defaults(func=cmd_chip)

    # 6. DIVIDER
    p_div = subparsers.add_parser("divider", help="Generate chapter divider (PCB, Laser, or Spectrum)")
    p_div.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Style: cyberpunk=PCB, tactical=Laser, minimal=Spectrum")
    p_div.add_argument("--primary", help="Primary brand hex color")
    p_div.add_argument("--accent", help="Secondary accent hex color")
    p_div.add_argument("--output", "-o", help="Target SVG destination path")
    p_div.set_defaults(func=cmd_divider)

    # 7. SPLITTER
    p_spl = subparsers.add_parser("splitter", help="Generate sub-module splitter (flush x=1..849)")
    p_spl.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_spl.add_argument("--primary", help="Primary brand hex color")
    p_spl.add_argument("--accent", help="Secondary accent hex color")
    p_spl.add_argument("--label", default="[MODULE: SUB_SYSTEM]", help="Splitter center label text")
    p_spl.add_argument("--output", "-o", help="Target SVG destination path")
    p_spl.set_defaults(func=cmd_splitter)

    # 8. COMPILE
    p_cmp = subparsers.add_parser("compile", help="Compile README template markdown containing pixel-kit directives")
    p_cmp.add_argument("--input", "-i", required=True, help="Input Markdown template filepath (e.g. README.template.md)")
    p_cmp.add_argument("--output", "-o", required=True, help="Output compiled Markdown filepath (e.g. README.md)")
    p_cmp.add_argument("--assets-dir", default="assets/generated", help="Folder where generated SVGs will be stored")
    p_cmp.set_defaults(func=cmd_compile)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
