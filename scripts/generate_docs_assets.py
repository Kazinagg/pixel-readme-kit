import os
import shutil
from generator.components import (
    generate_header,
    generate_metrics,
    generate_starchart,
    generate_profile_card
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "assets")
os.makedirs(OUT_DIR, exist_ok=True)

metrics_cards = [
    {"label": "ARCHITECTURE", "val": "MULTI-STYLE"},
    {"label": "THEMES", "val": "5 THEMES"},
    {"label": "ENGINE", "val": "v6.5 CORE"}
]

# Modern Clean (dark & light)
for mode, suffix in [("dark", ""), ("light", "-light")]:
    hdr = generate_header(
        style="modern", theme="modern-clean", mode=mode,
        title="MODERN CLEAN RUNTIME",
        subtitle="Ultra-Minimalist Vector Engineering for GitHub",
        spec1="CORE: V6.5", spec2="LATENCY: <35ms", spec3="IMMUNITY: 100%"
    )
    with open(os.path.join(OUT_DIR, f"header-modern{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(hdr)

    met = generate_metrics(
        cards=metrics_cards, style="modern", theme="modern-clean", mode=mode
    )
    with open(os.path.join(OUT_DIR, f"metrics-modern{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(met)

    sc = generate_starchart(
        style="modern", theme="modern-clean", mode=mode,
        repo="Kazinagg/pixel-readme-kit",
        title="STAR GROWTH TRAJECTORY",
        points="12,45,120,380,820,1450",
        current="1,450", delta="+120% 6m"
    )
    with open(os.path.join(OUT_DIR, f"starchart-modern{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(sc)

    prof = generate_profile_card(
        style="modern", theme="modern-clean", mode=mode,
        name="MODERN DEVELOPER",
        role="SYSTEMS & CLOUD ARCHITECT",
        bio="Engineering deterministic SVG instruments and resilient developer runtimes.",
        status="ACTIVE // VERIFIED",
        badge="TIER_1"
    )
    with open(os.path.join(OUT_DIR, f"profile-modern{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(prof)

# Sketch Rough Doodle (dark & light)
for mode, suffix in [("dark", ""), ("light", "-light")]:
    hdr = generate_header(
        style="sketch", theme="rough-doodle", mode=mode,
        title="HAND-DRAWN ARCHITECTURE",
        subtitle="Excalidraw & Rough Vector Instrumentation",
        spec1="DRAFT: V6.5", spec2="PHYSICS: WOBBLE", spec3="STATUS: OK"
    )
    with open(os.path.join(OUT_DIR, f"header-sketch{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(hdr)

    met = generate_metrics(
        cards=metrics_cards, style="sketch", theme="rough-doodle", mode=mode
    )
    with open(os.path.join(OUT_DIR, f"metrics-sketch{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(met)

    sc = generate_starchart(
        style="sketch", theme="rough-doodle", mode=mode,
        repo="Kazinagg/pixel-readme-kit",
        title="STAR GROWTH TRAJECTORY",
        points="12,45,120,380,820,1450",
        current="1,450", delta="+120% 6m"
    )
    with open(os.path.join(OUT_DIR, f"starchart-sketch{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(sc)

    prof = generate_profile_card(
        style="sketch", theme="rough-doodle", mode=mode,
        name="SKETCH ARCHITECT",
        role="CREATIVE TECH DESIGNER",
        bio="Drafting blueprints, handmade diagrams, and zero-dependency SVG kits.",
        status="SKETCHING DRAFTS",
        badge="DRAFT_01"
    )
    with open(os.path.join(OUT_DIR, f"profile-sketch{suffix}.svg"), "w", encoding="utf-8") as f:
        f.write(prof)

# Also copy extra generated demo assets from assets/generated/
gen_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "generated")
extra_files = [
    "callout-modern-tip-demo.svg", "callout-sketch-tip-demo.svg",
    "footer-modern-demo.svg", "footer-sketch-demo.svg",
    "progress-modern-demo.svg", "progress-sketch-demo.svg"
]
for ef in extra_files:
    src = os.path.join(gen_dir, ef)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(OUT_DIR, ef))

print(f"Generated and synced all assets into {OUT_DIR}")
