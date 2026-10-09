"""
Unit tests for Style 3: Hand-Drawn Sketch / Excalidraw (Pixel Readme Kit v6.1).
Validates XML conformance, pencil hatching patterns, multi-mode theming, compiler monolith integration, and templates.
"""

import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from generator.components import (
    generate_header,
    generate_compact_header,
    generate_frame,
    generate_footer,
    generate_callout,
    generate_divider,
    generate_splitter,
    generate_chip,
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
    generate_social,
    generate_starchart,
    generate_profile_card,
)
from generator.compiler import MarkdownCompiler
from generator.scaffolder import scaffold_readme, get_available_templates


class TestSketchComponentsXML(unittest.TestCase):
    """Verifies that all sketch style components generate valid SVG XML with hand-drawn aesthetic elements."""

    def test_sketch_headers(self):
        svg = generate_header(
            style="sketch", theme="excali-dark",
            title="EXCALI ARCHITECTURE", subtitle="HAND DRAWN SPECIFICATION",
            spec1="DETERMINISTIC PHYSICS", spec2="HATCH PATTERN /////", spec3="VIRGIL TYPOGRAPHY"
        )
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("viewBox", root.attrib)
        self.assertIn("font-sketch", svg)

        svg_compact = generate_compact_header(
            style="sketch", theme="whiteboard",
            title="QUICK DRAFT", subtitle="NOTES & SKETCHES"
        )
        root_c = ET.fromstring(svg_compact)
        self.assertEqual(root_c.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("font-sketch", svg_compact)

    def test_sketch_frames_and_footer(self):
        svg_top = generate_frame(frame_type="top", style="sketch", theme="notebook-graph", title="DRAFT WINDOW")
        root_top = ET.fromstring(svg_top)
        self.assertEqual(root_top.tag, "{http://www.w3.org/2000/svg}svg")

        svg_bot = generate_frame(frame_type="bottom", style="sketch", theme="notebook-graph", tag="[ END DRAFT ]")
        root_bot = ET.fromstring(svg_bot)
        self.assertEqual(root_bot.tag, "{http://www.w3.org/2000/svg}svg")

        svg_foot = generate_footer(style="sketch", theme="blueprint-sketch", status="SKETCH SESSION ARCHIVED", nav_text="BACK TO TOP")
        root_foot = ET.fromstring(svg_foot)
        self.assertEqual(root_foot.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("font-sketch", svg_foot)

    def test_sketch_callouts(self):
        for ctype in ["NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"]:
            with self.subTest(ctype=ctype):
                svg = generate_callout(
                    style="sketch", theme="excali-dark",
                    callout_type=ctype, title=f"POST-IT {ctype}",
                    subtitle="Sticky note with washi tape and pencil contour."
                )
                root = ET.fromstring(svg)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertIn("calloutSketch-tape", svg)

    def test_sketch_divider_and_splitter(self):
        svg_div = generate_divider(style="sketch", theme="excali-dark")
        root_d = ET.fromstring(svg_div)
        self.assertEqual(root_d.tag, "{http://www.w3.org/2000/svg}svg")

        svg_spl = generate_splitter(style="sketch", theme="whiteboard", label="PHASE 2: DETAILED SKETCH")
        root_s = ET.fromstring(svg_spl)
        self.assertEqual(root_s.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("font-sketch", svg_spl)

    def test_sketch_chips(self):
        svg_chip = generate_chip(style="sketch", theme="excali-dark", text="★ DRAFT v6.1")
        root_c = ET.fromstring(svg_chip)
        self.assertEqual(root_c.tag, "{http://www.w3.org/2000/svg}svg")

        svg_chip_val = generate_chip(style="sketch", theme="notebook-graph", text="STARS: 4.2k")
        root_cv = ET.fromstring(svg_chip_val)
        self.assertEqual(root_cv.tag, "{http://www.w3.org/2000/svg}svg")

    def test_sketch_metrics_and_progress(self):
        items = [
            {"label": "STAR TRACTION", "value": "4.2K+", "delta": "+84% wow!", "trend": "up"},
            {"label": "COMPLIANCE", "value": "100%", "status": "VERIFIED"}
        ]
        svg_m = generate_metrics(style="sketch", theme="excali-dark", metrics=items)
        root_m = ET.fromstring(svg_m)
        self.assertEqual(root_m.tag, "{http://www.w3.org/2000/svg}svg")

        svg_p = generate_progress(style="sketch", theme="excali-dark", value=75, label="PROJECT ROADMAP")
        root_p = ET.fromstring(svg_p)
        self.assertEqual(root_p.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("progSketch-hatch", svg_p)

    def test_sketch_techstack(self):
        svg_t = generate_techstack(style="sketch", theme="excali-dark", items=["python", "rust", "docker"], columns=3)
        root_t = ET.fromstring(svg_t)
        self.assertEqual(root_t.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("font-sketch", svg_t)

    def test_sketch_timeline(self):
        milestones = [
            {"title": "DRAFT SPEC", "date": "2026-Q1", "status": "COMPLETED", "desc": "Excalidraw physics exploration"},
            {"title": "VECTOR ENGINE", "date": "2026-Q2", "status": "IN_PROGRESS", "desc": "Pencil hatching and sketch components"},
            {"title": "HUD STUDIO ROLLOUT", "date": "2026-Q3", "status": "PLANNED", "desc": "Interactive canvas preview"},
        ]
        svg_tl = generate_timeline(style="sketch", theme="excali-dark", milestones=milestones)
        root_tl = ET.fromstring(svg_tl)
        self.assertEqual(root_tl.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("timelineSketch-tape", svg_tl)

    def test_sketch_starchart(self):
        svg_sc = generate_starchart(
            style="sketch", theme="excali-dark",
            repo="Kazinagg/pixel-readme-kit", points=[100, 300, 750, 1800, 3200],
            current="3,200", delta="+84%"
        )
        root_sc = ET.fromstring(svg_sc)
        self.assertEqual(root_sc.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("starSketch-hatch", svg_sc)
        self.assertIn("font-sketch", svg_sc)

    def test_sketch_social_and_profile_card(self):
        svg_soc = generate_social(
            style="sketch", theme="excali-dark",
            title="EXCALI SPEC", subtitle="HAND DRAWN VECTOR SUITE",
            repo="org/sketch-kit", tags="PYTHON,SVG,EXCALIDRAW"
        )
        root_soc = ET.fromstring(svg_soc)
        self.assertEqual(root_soc.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("socialSketch-tape", svg_soc)

        svg_prof = generate_profile_card(
            style="sketch", theme="excali-dark",
            name="LEO ARCHITECT", role="SYSTEMS & COMPILER DESIGNER",
            bio="Drafting high performance developer runtimes.",
            status="AVAILABLE FOR HIRE", location="BERLIN // UTC+1"
        )
        root_prof = ET.fromstring(svg_prof)
        self.assertEqual(root_prof.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("profileSketch-tape", svg_prof)


class TestSketchThemesAndModes(unittest.TestCase):
    """Verifies that all 4 sketch themes and display modes work seamlessly together."""

    def test_all_sketch_themes_and_modes(self):
        themes = ["excali-dark", "whiteboard", "notebook-graph", "blueprint-sketch"]
        modes = ["auto", "dark", "light", "transparent"]

        for theme in themes:
            for mode in modes:
                with self.subTest(theme=theme, mode=mode):
                    svg = generate_header(style="sketch", theme=theme, mode=mode, title="THEME TEST")
                    root = ET.fromstring(svg)
                    self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


class TestSketchCompilerIntegration(unittest.TestCase):
    """Verifies compilation of Markdown documents with style='sketch'."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.compiler = MarkdownCompiler(assets_dir=self.tmp_dir, use_cache=False)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_compile_sketch_markdown(self):
        md_input = """# Sketch Readme

<!-- pixel-kit:header style="sketch" theme="excali-dark" title="SKETCH ENGINE" subtitle="EXCALIDRAW ARCHITECTURE" -->

<!-- pixel-kit:metrics style="sketch" theme="excali-dark" -->
- label="SPEED" value="10X" trend="up"
- label="TESTS" value="100%" status="PASSED"
<!-- /pixel-kit:metrics -->

<!-- pixel-kit:window style="sketch" theme="excali-dark" title="DRAFT WINDOW" -->
Rough notes and handwritten architectural specs.
<!-- /pixel-kit:window -->

<!-- pixel-kit:footer style="sketch" theme="excali-dark" title="SKETCH DRAFT COMPLETE" -->
"""
        compiled = self.compiler.compile_text(md_input)
        self.assertIn("<table", compiled)
        self.assertIn("header-excali-dark-1.svg", compiled)

        files = os.listdir(self.tmp_dir)
        self.assertGreaterEqual(len(files), 4)
        for f in files:
            if f.endswith(".svg"):
                path = os.path.join(self.tmp_dir, f)
                with open(path, "r", encoding="utf-8") as fp:
                    content = fp.read()
                root = ET.fromstring(content)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


class TestSketchTemplates(unittest.TestCase):
    """Verifies that sketch templates exist and can be scaffolded."""

    def test_templates_registered(self):
        avail = get_available_templates()
        self.assertIn("repo/sketch", avail)
        self.assertIn("profile/sketch", avail)
        self.assertIn("sketch", avail)

    def test_scaffold_sketch_templates(self):
        tmp_repo = tempfile.mktemp(suffix=".md")
        res_repo = scaffold_readme(project_type="repo/sketch", title="SKETCH LIB", output_path=tmp_repo)
        with open(res_repo, "r", encoding="utf-8") as f:
            repo_md = f.read()
        self.assertIn('style="sketch"', repo_md)
        self.assertIn("SKETCH LIB", repo_md)

        tmp_prof = tempfile.mktemp(suffix=".md")
        res_prof = scaffold_readme(project_type="profile/sketch", title="JANE SKETCHER", output_path=tmp_prof)
        with open(res_prof, "r", encoding="utf-8") as f:
            prof_md = f.read()
        self.assertIn('style="sketch"', prof_md)
        self.assertIn("JANE SKETCHER", prof_md)

        for p in (tmp_repo, tmp_prof):
            if os.path.exists(p):
                os.remove(p)


if __name__ == "__main__":
    unittest.main()
