import os
import unittest
import shutil
import tempfile
from generator.themes.registry import (
    THEME_PALETTES,
    THEME_ALIASES,
    VALID_STYLES,
    STYLE_THEMES,
    normalize_style_and_theme,
    get_themes_for_style,
    resolve_theme
)
from generator.engine import (
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
    generate_social,
    generate_starchart,
    generate_profile_card,
    validate_svg
)
from generator.compiler import MarkdownCompiler
from generator.scaffolder import scaffold_readme


class TestStyleThemeOrthogonal(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.assets_dir = os.path.join(self.test_dir, "assets")
        os.makedirs(self.assets_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_normalize_style_and_theme(self):
        # 1. Explicit orthogonal style and theme
        s, t = normalize_style_and_theme("pixel", "tactical")
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "tactical")

        # 2. Modern style with theme
        s, t = normalize_style_and_theme("modern", "nordic-frost")
        self.assertEqual(s, "modern")
        self.assertEqual(t, "nordic-frost")

        # 3. Corporate style with theme
        s, t = normalize_style_and_theme("corporate", "enterprise-navy")
        self.assertEqual(s, "corporate")
        self.assertEqual(t, "enterprise-navy")

        # 4. Backward compatibility: legacy style name passed as style
        s, t = normalize_style_and_theme("cyberpunk", None)
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "cyberpunk")

        s, t = normalize_style_and_theme("tactical", None)
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "tactical")

        s, t = normalize_style_and_theme("minimal", None)
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "minimal")

        # 5. Theme alias resolution
        s, t = normalize_style_and_theme("pixel", "academic")
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "academic-paper")

        s, t = normalize_style_and_theme(None, "amber")
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "amber")

        # 6. Default fallback
        s, t = normalize_style_and_theme(None, None)
        self.assertEqual(s, "pixel")
        self.assertEqual(t, "cyberpunk")

    def test_get_themes_for_style(self):
        pixel_themes = get_themes_for_style("pixel")
        self.assertIn("cyberpunk", pixel_themes)
        self.assertIn("tactical", pixel_themes)
        self.assertIn("minimal", pixel_themes)
        self.assertIn("amber", pixel_themes)
        self.assertIn("tokyo", pixel_themes)

        modern_themes = get_themes_for_style("modern")
        self.assertIn("slate-dark", modern_themes)
        self.assertIn("nordic-frost", modern_themes)
        self.assertIn("linear-violet", modern_themes)

        corp_themes = get_themes_for_style("corporate")
        self.assertIn("enterprise-navy", corp_themes)
        self.assertIn("swiss-mono", corp_themes)
        self.assertIn("executive-slate", corp_themes)

    def test_all_components_render_with_orthogonal_themes(self):
        # Verify that all components render and pass SVG validation
        # across different themes
        themes_to_test = [
            "cyberpunk",
            "tactical",
            "minimal",
            "slate-dark",
            "nordic-frost",
            "linear-violet",
            "enterprise-navy",
            "swiss-mono",
            "executive-slate"
        ]

        for th in themes_to_test:
            # Header
            svg = generate_header(style="pixel", theme=th, title="TEST", subtitle="SUB")
            validate_svg(svg)

            # Footer
            svg = generate_footer(style="pixel", theme=th, status="ONLINE", nav_text="TOP")
            validate_svg(svg)

            # Callout
            svg = generate_callout(style="pixel", theme=th, title="NOTICE", subtitle="INFO")
            validate_svg(svg)

            # Frame
            svg = generate_frame(style="pixel", theme=th, frame_type="top", title="WINDOW")
            validate_svg(svg)

            # Chip
            svg = generate_chip(style="pixel", theme=th, chip_type="closed", text="CHIP")
            validate_svg(svg)

            # Divider
            svg = generate_divider(style="pixel", theme=th)
            validate_svg(svg)

            # Splitter
            svg = generate_splitter(style="pixel", theme=th, label="SPLIT")
            validate_svg(svg)

            # Metrics
            svg = generate_metrics(style="pixel", theme=th, metrics=[{"label": "FPS", "value": "60"}])
            validate_svg(svg)

            # Progress
            svg = generate_progress(style="pixel", theme=th, value=75, label="PROG")
            validate_svg(svg)

            # Techstack
            svg = generate_techstack(style="pixel", theme=th, items=["python", "rust"])
            validate_svg(svg)

            # Timeline
            svg = generate_timeline(style="pixel", theme=th, items=[{"title": "P1", "date": "Q1", "status": "DONE"}])
            validate_svg(svg)

            # Social
            svg = generate_social(style="pixel", theme=th, title="SOC", subtitle="MEDIA")
            validate_svg(svg)

            # Starchart
            svg = generate_starchart(style="pixel", theme=th, repo="user/repo", points=[10, 20, 30])
            validate_svg(svg)

            # Profile
            svg = generate_profile_card(style="pixel", theme=th, name="DEV", role="ENG", bio="CODE")
            validate_svg(svg)

    def test_compiler_orthogonal_directive_parsing(self):
        compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False)
        md_input = """# Test Document

<!-- pixel-kit:header style="pixel" theme="nordic-frost" title="NORDIC HEADER" subtitle="SUBTITLE" -->

<!-- pixel-kit:chip style="pixel" theme="tokyo" type="closed" text="TOKYO CHIP" -->

<!-- pixel-kit:callout style="pixel" theme="slate-dark" type="note" title="SLATE NOTE" -->

<!-- pixel-kit:window style="pixel" theme="minimal" title="MINIMAL WINDOW" -->
Inner window content goes here.
<!-- /pixel-kit:window -->

<!-- pixel-kit:header style="cyberpunk" title="LEGACY CYBERPUNK HEADER" -->
"""
        compiled_output = compiler.compile_text(md_input)

        # Check compiled HTML links
        self.assertIn("header-nordic-frost", compiled_output)
        self.assertIn("chip-tokyo", compiled_output)
        self.assertIn("callout-slate-dark", compiled_output)
        self.assertIn("frame-top-minimal", compiled_output)
        self.assertIn("header-cyberpunk", compiled_output)

        # Verify generated files exist in assets_dir
        generated_files = os.listdir(self.assets_dir)
        self.assertTrue(any("header-nordic-frost" in f for f in generated_files))
        self.assertTrue(any("chip-tokyo" in f for f in generated_files))
        self.assertTrue(any("callout-slate-dark" in f for f in generated_files))
        self.assertTrue(any("frame-top-minimal" in f for f in generated_files))
        self.assertTrue(any("header-cyberpunk" in f for f in generated_files))

    def test_scaffolder_with_style_and_theme(self):
        out_path = os.path.join(self.test_dir, "SCAFFOLD_TEST.template.md")
        scaffold_readme(
            project_type="repo/library",
            title="ORTHOGONAL PROJECT",
            style="pixel",
            theme="nordic-frost",
            output_path=out_path
        )
        self.assertTrue(os.path.exists(out_path))
        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('theme="nordic-frost"', content)
        self.assertIn("ORTHOGONAL PROJECT", content)


if __name__ == "__main__":
    unittest.main()
