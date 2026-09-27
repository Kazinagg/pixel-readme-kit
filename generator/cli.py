"""
CLI Generator & Compiler for Pixel Readme Kit v3.0
Usage modes:
1. Generate individual SVG blocks (supports --mode auto|dark|light|transparent|gh|picture):
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

def save_output(svg_content, output_path, default_path):
    target = output_path if output_path else default_path
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    validate_svg(svg_content)
    with open(target, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated SVG successfully: {target}")

def handle_cli_output(args, generator_fn, gen_kwargs, default_name):
    mode = getattr(args, "mode", "auto")
    if mode in ("gh", "github"):
        out = args.output if args.output else f"assets/{default_name}.svg"
        base, ext = os.path.splitext(out)
        out_dark = f"{base}-dark{ext}"
        out_light = f"{base}-light{ext}"
        svg_dark = generator_fn(**dict(gen_kwargs, mode="dark"))
        svg_light = generator_fn(**dict(gen_kwargs, mode="light"))
        save_output(svg_dark, out_dark, out_dark)
        save_output(svg_light, out_light, out_light)
        print("\n[i] GitHub Dark/Light Markdown syntax:")
        print(f"![{default_name}]({out_dark}#gh-dark-mode-only)")
        print(f"![{default_name}]({out_light}#gh-light-mode-only)")
    elif mode == "picture":
        out = args.output if args.output else f"assets/{default_name}.svg"
        base, ext = os.path.splitext(out)
        out_dark = f"{base}-dark{ext}"
        out_light = f"{base}-light{ext}"
        svg_dark = generator_fn(**dict(gen_kwargs, mode="dark"))
        svg_light = generator_fn(**dict(gen_kwargs, mode="light"))
        save_output(svg_dark, out_dark, out_dark)
        save_output(svg_light, out_light, out_light)
        print("\n[i] HTML5 <picture> syntax:")
        print(f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{out_dark}">\n  <source media="(prefers-color-scheme: light)" srcset="{out_light}">\n  <img src="{out_dark}">\n</picture>')
    else:
        svg = generator_fn(**dict(gen_kwargs, mode=mode))
        save_output(svg, args.output, f"assets/{default_name}.svg")

def cmd_header(args):
    handle_cli_output(args, generate_header, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "title": args.title,
        "subtitle": args.subtitle,
        "tag": args.tag,
        "tag_url": getattr(args, "tag_url", None),
        "close_url": getattr(args, "close_url", None),
        "spec1": args.spec1,
        "spec2": args.spec2,
        "spec3": args.spec3,
        "specs": args.specs
    }, f"header-{args.style}")

def cmd_footer(args):
    handle_cli_output(args, generate_footer, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "status": args.status,
        "nav_text": args.nav,
        "sub_text": args.sub
    }, f"footer-{args.style}")

def cmd_callout(args):
    prefix = "callout-quote" if args.quote else "callout"
    handle_cli_output(args, generate_callout, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "callout_type": args.type,
        "title": args.title,
        "subtitle": args.subtitle,
        "is_quote": args.quote
    }, f"{prefix}-{args.style}-{args.type}")

def cmd_frame(args):
    handle_cli_output(args, generate_frame, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "frame_type": args.type,
        "title": args.title,
        "tag": args.tag,
        "tag_url": getattr(args, "tag_url", None),
        "close_url": getattr(args, "close_url", None)
    }, f"frame-{args.type}-{args.style}")

def cmd_chip(args):
    chip_text = args.text
    if getattr(args, "github", None):
        repo = getattr(args, "repo", None) or "Kazinagg/pixel-readme-kit"
        from generator.compiler import fetch_github_stat
        stat_text, _ = fetch_github_stat(repo, args.github)
        chip_text = stat_text

    handle_cli_output(args, generate_chip, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "chip_type": args.type,
        "text": chip_text,
        "width": args.width
    }, f"chip-{args.style}-{args.type}")

def cmd_divider(args):
    handle_cli_output(args, generate_divider, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"divider-{args.style}")

def cmd_splitter(args):
    handle_cli_output(args, generate_splitter, {
        "style": args.style,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "label": args.label
    }, f"splitter-{args.style}")

def cmd_compile(args):
    inp = args.input if args.input else "README.template.md"
    if args.output:
        out = args.output
    else:
        out = "README.md" if inp == "README.template.md" else (inp.replace(".template.md", ".md") if ".template.md" in inp else "README.md")
    print(f"[*] Compiling Markdown template: {inp}")
    print(f"[*] Assets directory: {args.assets_dir}")
    print(f"[*] Output destination: {out}")
    compiler = MarkdownCompiler(assets_dir=args.assets_dir)
    compiler.compile_file(inp, out)
    print(f"[+] Successfully compiled to: {out}")

def main():
    parser = argparse.ArgumentParser(
        prog="pixel-kit",
        description="Pixel Readme Kit v3.0 — Multi-Mode Cyberpunk / Tactical / Minimal HUD Generator & Markdown Compiler"
    )

    subparsers = parser.add_subparsers(dest="command", help="Block type or compiler action")
    mode_choices = ["auto", "dark", "light", "transparent", "gh", "picture"]

    # 1. HEADER
    p_hdr = subparsers.add_parser("header", help="Generate flagship header banner")
    p_hdr.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style (cyberpunk, tactical, minimal)")
    p_hdr.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_hdr.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_hdr.add_argument("--primary", help="Primary brand hex color (e.g. #00C8D7, #F59E0B, #4F8BFF)")
    p_hdr.add_argument("--accent", help="Secondary accent hex color (e.g. #A855F7, #EA580C)")
    p_hdr.add_argument("--title", default="PIXEL-KIT", help="Main title text")
    p_hdr.add_argument("--subtitle", default="TRANSLUCENT HUD DESIGN SYSTEM", help="Subtitle description text")
    p_hdr.add_argument("--tag", default="SYSTEM_ACTIVE", help="Top badge tag text")
    p_hdr.add_argument("--tag-url", help="Optional URL link for the top badge tag")
    p_hdr.add_argument("--close-url", help="Optional URL link for the close button [x]")
    p_hdr.add_argument("--spec1", help="Level 3 spec line 1 (e.g. 'HUD ARCHITECTURE: TRANSLUCENT GLASS')")
    p_hdr.add_argument("--spec2", help="Level 3 spec line 2 (e.g. 'TEXT INTEGRATION: 100%% COPYABLE MARKDOWN')")
    p_hdr.add_argument("--spec3", help="Level 3 spec line 3 (e.g. 'ANIMATION SUITE: RADAR // SCANLINE')")
    p_hdr.add_argument("--specs", help="Combined level 3 specs separated by '|' (max 3 items)")
    p_hdr.add_argument("--output", "-o", help="Target SVG destination path")
    p_hdr.set_defaults(func=cmd_header)

    # 2. FOOTER
    p_ftr = subparsers.add_parser("footer", help="Generate full-width closing footer plate")
    p_ftr.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_ftr.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_ftr.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_ftr.add_argument("--primary", help="Primary brand hex color")
    p_ftr.add_argument("--accent", help="Secondary accent hex color")
    p_ftr.add_argument("--status", default="SESSION_ACTIVE // STANDBY", help="Status telemetry readout text")
    p_ftr.add_argument("--sub", help="Secondary diagnostic or telemetry readout line")
    p_ftr.add_argument("--nav", default="RETURN TO TOP", help="Navigation button text")
    p_ftr.add_argument("--output", "-o", help="Target SVG destination path")
    p_ftr.set_defaults(func=cmd_footer)

    # 3. CALLOUT
    p_clt = subparsers.add_parser("callout", help="Generate inline alert plate or quote header")
    p_clt.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_clt.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_clt.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
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
    p_frm.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_frm.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_frm.add_argument("--type", choices=["top", "bottom"], default="top", help="Frame position: top or bottom")
    p_frm.add_argument("--primary", help="Primary brand hex color")
    p_frm.add_argument("--accent", help="Secondary accent hex color")
    p_frm.add_argument("--title", default="╔═ SYSTEM.CORE // RUNTIME.SYS", help="Window title text (for top frame)")
    p_frm.add_argument("--tag", default="[OPEN_HUD]", help="Window tag text (for top frame)")
    p_frm.add_argument("--tag-url", help="Optional URL link for the top frame tag")
    p_frm.add_argument("--close-url", help="Optional URL link for the close button [x]")
    p_frm.add_argument("--output", "-o", help="Target SVG destination path")
    p_frm.set_defaults(func=cmd_frame)

    # 5. CHIP
    p_chp = subparsers.add_parser("chip", help="Generate holographic pill / chip badge")
    p_chp.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_chp.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_chp.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_chp.add_argument("--type", choices=["closed", "decay", "pulse"], default="closed", help="Form & decay mechanics: closed, decay, pulse")
    p_chp.add_argument("--primary", help="Primary brand hex color")
    p_chp.add_argument("--accent", help="Secondary accent hex color")
    p_chp.add_argument("--text", default="CHIP_TAG", help="Text label inside the chip")
    p_chp.add_argument("--github", choices=["stars", "forks", "issues", "license", "watchers", "version", "release"], help="Fetch live GitHub stat for label")
    p_chp.add_argument("--repo", default="Kazinagg/pixel-readme-kit", help="GitHub repo for live stats (e.g. Kazinagg/pixel-readme-kit)")
    p_chp.add_argument("--width", type=int, help="Optional manual width override in px (default: auto-calculated from text)")
    p_chp.add_argument("--output", "-o", help="Target SVG destination path")
    p_chp.set_defaults(func=cmd_chip)

    # 6. DIVIDER
    p_div = subparsers.add_parser("divider", help="Generate chapter divider (PCB, Laser, or Spectrum)")
    p_div.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Style: cyberpunk=PCB, tactical=Laser, minimal=Spectrum")
    p_div.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_div.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_div.add_argument("--primary", help="Primary brand hex color")
    p_div.add_argument("--accent", help="Secondary accent hex color")
    p_div.add_argument("--output", "-o", help="Target SVG destination path")
    p_div.set_defaults(func=cmd_divider)

    # 7. SPLITTER
    p_spl = subparsers.add_parser("splitter", help="Generate sub-module splitter (flush x=1..849)")
    p_spl.add_argument("--style", choices=["cyberpunk", "tactical", "minimal"], default="cyberpunk", help="Geometry style")
    p_spl.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_spl.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_spl.add_argument("--primary", help="Primary brand hex color")
    p_spl.add_argument("--accent", help="Secondary accent hex color")
    p_spl.add_argument("--label", default="[MODULE: SUB_SYSTEM]", help="Splitter center label text")
    p_spl.add_argument("--output", "-o", help="Target SVG destination path")
    p_spl.set_defaults(func=cmd_splitter)

    # 8. COMPILE
    p_cmp = subparsers.add_parser("compile", help="Compile README template markdown containing pixel-kit directives")
    p_cmp.add_argument("--input", "-i", default="README.template.md", help="Input Markdown template filepath (default: README.template.md)")
    p_cmp.add_argument("--output", "-o", default=None, help="Output compiled Markdown filepath (default: README.md or matching *.md)")
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
