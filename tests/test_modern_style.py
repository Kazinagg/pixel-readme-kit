"""
Unit tests for Style 2: Modern / Clean Vector (Pixel Readme Kit v6.0).
Validates XML conformance, multi-mode theming, compiler integration, and templates.
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
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.compiler import MarkdownCompiler
from generator.scaffolder import scaffold_readme, get_available_templates


class TestModernComponentsXML(unittest.TestCase):
    """Verifies that all modern style components generate valid SVG XML."""

    def test_modern_headers(self):
        svg = generate_header(
            style="modern", theme="slate-dark",
            title="CLEAN RUNTIME", subtitle="SYSTEM STATUS READY",
            spec1="CORE: V6.0", spec2="MEMORY: 16GB", spec3="NET: 10GBPS"
        )
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("viewBox", root.attrib)

        svg_compact = generate_compact_header(
            style="modern", theme="nordic-frost",
            title="COMPACT HEADER", subtitle="SUBTITLE TEXT"
        )
        root_c = ET.fromstring(svg_compact)
        self.assertEqual(root_c.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_frames_and_footer(self):
        svg_top = generate_frame(style="modern", theme="linear-violet", frame_type="top", title="WINDOW TITLE")
        root_top = ET.fromstring(svg_top)
        self.assertEqual(root_top.tag, "{http://www.w3.org/2000/svg}svg")

        svg_bot = generate_frame(style="modern", theme="linear-violet", frame_type="bottom", title="WINDOW TITLE")
        root_bot = ET.fromstring(svg_bot)
        self.assertEqual(root_bot.tag, "{http://www.w3.org/2000/svg}svg")

        svg_foot = generate_footer(style="modern", theme="emerald-clean", status="FOOTER STATUS", nav_text="BACK TO TOP")
        root_foot = ET.fromstring(svg_foot)
        self.assertEqual(root_foot.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_callouts(self):
        for ctype in ["NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"]:
            with self.subTest(ctype=ctype):
                svg = generate_callout(
                    style="modern", theme="slate-dark",
                    callout_type=ctype, title=f"{ctype} TITLE",
                    subtitle="This is a modern clean vector callout."
                )
                root = ET.fromstring(svg)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_divider_and_splitter(self):
        svg_div = generate_divider(style="modern", theme="slate-dark")
        root_d = ET.fromstring(svg_div)
        self.assertEqual(root_d.tag, "{http://www.w3.org/2000/svg}svg")

        svg_spl = generate_splitter(style="modern", theme="nordic-frost", label="SUBSECTION")
        root_s = ET.fromstring(svg_spl)
        self.assertEqual(root_s.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_chips(self):
        svg_chip = generate_chip(style="modern", theme="slate-dark", text="STABLE RELEASE", chip_type="pulse")
        root_c = ET.fromstring(svg_chip)
        self.assertEqual(root_c.tag, "{http://www.w3.org/2000/svg}svg")

        svg_chip_val = generate_chip(style="modern", theme="slate-dark", text="STARS: 1.2k", chip_type="closed")
        root_cv = ET.fromstring(svg_chip_val)
        self.assertEqual(root_cv.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_metrics_and_progress(self):
        items = [
            {"label": "LATENCY", "value": "1.2ms", "delta": "-20%", "trend": "up"},
            {"label": "UPTIME", "value": "99.99%", "status": "OPTIMAL"}
        ]
        svg_m = generate_metrics(style="modern", theme="linear-violet", metrics=items)
        root_m = ET.fromstring(svg_m)
        self.assertEqual(root_m.tag, "{http://www.w3.org/2000/svg}svg")

        svg_p = generate_progress(style="modern", theme="emerald-clean", value=78, label="BUILD PROGRESS")
        root_p = ET.fromstring(svg_p)
        self.assertEqual(root_p.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_techstack(self):
        svg_t = generate_techstack(style="modern", theme="slate-dark", items=["python", "rust", "docker"], columns=3)
        root_t = ET.fromstring(svg_t)
        self.assertEqual(root_t.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_timeline(self):
        milestones = [
            {"title": "INIT", "date": "2026-Q1", "status": "COMPLETED", "desc": "Phase 1"},
            {"title": "BETA", "date": "2026-Q2", "status": "IN_PROGRESS", "desc": "Phase 2"},
            {"title": "PROD", "date": "2026-Q3", "status": "PLANNED", "desc": "Phase 3"},
        ]
        svg_tl = generate_timeline(style="modern", theme="slate-dark", milestones=milestones)
        root_tl = ET.fromstring(svg_tl)
        self.assertEqual(root_tl.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_starchart(self):
        svg_sc = generate_starchart(
            style="modern", theme="slate-dark",
            repo="test/repo", points=[10, 50, 200, 600, 1500],
            current="1,500", delta="+120%"
        )
        root_sc = ET.fromstring(svg_sc)
        self.assertEqual(root_sc.tag, "{http://www.w3.org/2000/svg}svg")

    def test_modern_social_and_profile_card(self):
        svg_soc = generate_social(
            style="modern", theme="linear-violet",
            title="PROJECT TITAN", subtitle="ENTERPRISE RUNTIME",
            repo="org/titan", tags="RUST,K8S,GRPC"
        )
        root_soc = ET.fromstring(svg_soc)
        self.assertEqual(root_soc.tag, "{http://www.w3.org/2000/svg}svg")

        svg_prof = generate_profile_card(
            style="modern", theme="slate-dark",
            name="JORDAN ARCHITECT", role="PRINCIPAL SYSTEMS ENGINEER",
            bio="Building high throughput distributed systems.",
            status="AVAILABLE FOR HIRE", location="SAN FRANCISCO // UTC-7"
        )
        root_prof = ET.fromstring(svg_prof)
        self.assertEqual(root_prof.tag, "{http://www.w3.org/2000/svg}svg")


class TestModernThemesAndModes(unittest.TestCase):
    """Verifies that all modern themes and modes work seamlessly together."""

    def test_all_modern_themes_and_modes(self):
        themes = ["slate-dark", "nordic-frost", "linear-violet", "emerald-clean"]
        modes = ["auto", "dark", "light", "transparent"]

        for theme in themes:
            for mode in modes:
                with self.subTest(theme=theme, mode=mode):
                    svg = generate_header(style="modern", theme=theme, mode=mode, title="TEST THEME")
                    root = ET.fromstring(svg)
                    self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


class TestModernCompilerIntegration(unittest.TestCase):
    """Verifies compilation of Markdown documents with style='modern'."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.compiler = MarkdownCompiler(assets_dir=self.tmp_dir, use_cache=False)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_compile_modern_markdown(self):
        md_input = """# Modern Readme

<!-- pixel-kit:header style="modern" theme="slate-dark" title="MODERN APP" subtitle="CLEAN VECTOR ARCHITECTURE" -->

<!-- pixel-kit:metrics style="modern" theme="slate-dark" -->
- label="SPEED" value="10X" trend="up"
- label="TESTS" value="100%" status="PASSED"
<!-- /pixel-kit:metrics -->

<!-- pixel-kit:window style="modern" theme="slate-dark" title="SYSTEM WINDOW" -->
Content inside modern window.
<!-- /pixel-kit:window -->

<!-- pixel-kit:footer style="modern" theme="slate-dark" title="ALL RIGHTS RESERVED" -->
"""
        compiled = self.compiler.compile_text(md_input)
        self.assertIn("<table", compiled)
        self.assertIn("header-slate-dark-1.svg", compiled)

        # Verify generated SVG files exist and are valid XML
        files = os.listdir(self.tmp_dir)
        self.assertGreaterEqual(len(files), 4)
        for f in files:
            if f.endswith(".svg"):
                path = os.path.join(self.tmp_dir, f)
                with open(path, "r", encoding="utf-8") as fp:
                    content = fp.read()
                root = ET.fromstring(content)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


class TestModernTemplates(unittest.TestCase):
    """Verifies that modern templates exist and can be scaffolded."""

    def test_templates_registered(self):
        avail = get_available_templates()
        self.assertIn("repo/modern", avail)
        self.assertIn("profile/modern", avail)

    def test_scaffold_modern_templates(self):
        tmp_repo = tempfile.mktemp(suffix=".md")
        res_repo = scaffold_readme(project_type="repo/modern", title="MODERN LIB", output_path=tmp_repo)
        with open(res_repo, "r", encoding="utf-8") as f:
            repo_md = f.read()
        self.assertIn("style=\"modern\"", repo_md)
        self.assertIn("MODERN LIB", repo_md)

        tmp_prof = tempfile.mktemp(suffix=".md")
        res_prof = scaffold_readme(project_type="profile/modern", title="JANE DOE", output_path=tmp_prof)
        with open(res_prof, "r", encoding="utf-8") as f:
            prof_md = f.read()
        self.assertIn("style=\"modern\"", prof_md)
        self.assertIn("JANE DOE", prof_md)

        for p in (tmp_repo, tmp_prof):
            if os.path.exists(p):
                os.remove(p)


if __name__ == "__main__":
    unittest.main()
