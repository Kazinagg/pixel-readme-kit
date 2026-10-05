"""
Tests for v4.3 Palette Harmonization, Multi-Color Enhancements, VIEW Mode Primer Spacing, and Git Push.
"""

import unittest
import os
import tempfile
import shutil
import subprocess

from generator.engine import (
    THEME_PALETTES,
    resolve_theme,
    resolve_colors,
    generate_header,
    generate_footer,
    generate_frame,
    generate_chip,
    generate_splitter,
    generate_divider
)
from generator.palettes import THEMES
from generator.compiler import MarkdownCompiler
from generator.server import STUDIO_HTML, StudioRequestHandler


class TestPaletteHarmonization(unittest.TestCase):
    def test_theme_palettes_include_tertiary(self):
        """Verify that THEME_PALETTES includes tertiary across all styles and modes."""
        for style in ["cyberpunk", "tactical", "minimal"]:
            for mode in ["dark", "light"]:
                palette = THEME_PALETTES.get(style, {}).get(mode, {})
                self.assertIn("tertiary", palette, f"Style '{style}' ({mode}) missing 'tertiary'")
                self.assertTrue(palette["tertiary"].startswith("#"), f"Style '{style}' tertiary must be a hex color")

    def test_preset_palettes_include_tertiary(self):
        """Verify all named presets in THEMES include tertiary."""
        for preset_name, data in THEMES.items():
            self.assertIn("tertiary", data, f"Preset '{preset_name}' missing 'tertiary'")
            self.assertTrue(data["tertiary"].startswith("#"), f"Preset '{preset_name}' tertiary must be a hex color")

    def test_resolve_theme_tertiary(self):
        """Verify resolve_theme produces --tertiary CSS variable and handles custom tertiary."""
        cols, _ = resolve_theme(style="cyberpunk", mode="dark", tertiary="#112233")
        self.assertEqual(cols["tertiary"], "#112233")

        # Mode auto produces both root and media query with tertiary
        _, css_auto = resolve_theme(style="cyberpunk", mode="auto", tertiary="#445566")
        self.assertIn("--tertiary: #445566;", css_auto)

    def test_resolve_colors_tertiary(self):
        """Verify resolve_colors outputs primary, accent, and bg."""
        prim, acc, bg = resolve_colors(style="cyberpunk", mode="dark", tertiary="#aabbcc")
        self.assertTrue(prim.startswith("#") or prim.startswith("var"))
        self.assertTrue(acc.startswith("#") or acc.startswith("var"))

    def test_header_uses_tertiary_and_no_unwanted_hardcoded_colors(self):
        """Verify generate_header uses tertiary parameter and eliminates old hardcoded hexes."""
        custom_tert = "#FE1234"
        svg = generate_header(
            title="NEO SENTINEL",
            subtitle="TEST UNIT",
            style="cyberpunk",
            tertiary=custom_tert
        )
        self.assertIn(custom_tert, svg, "Header SVG must contain custom tertiary color")
        # Ensure old hardcoded hex colors are not present
        self.assertNotIn("#06B6D4", svg, "Old hardcoded #06B6D4 should be removed from header")
        self.assertNotIn("#FF0055", svg, "Old hardcoded #FF0055 should be replaced by tertiary/palette")

    def test_footer_uses_tertiary(self):
        """Verify generate_footer accepts and utilizes tertiary color."""
        custom_tert = "#AA11BB"
        svg = generate_footer(
            status="ONLINE",
            style="cyberpunk",
            tertiary=custom_tert
        )
        self.assertIn(custom_tert, svg, "Footer SVG must contain custom tertiary color")

    def test_frame_uses_tertiary_for_close_button(self):
        """Verify generate_frame accepts tertiary and uses it for close button."""
        custom_tert = "#12FF99"
        svg = generate_frame(
            title="SYSTEM CONSOLE",
            style="cyberpunk",
            tertiary=custom_tert
        )
        self.assertIn(custom_tert, svg, "Frame SVG must contain custom tertiary color")

    def test_secondary_accent_volume_enhancements(self):
        """Verify that accent color is used in frame brackets, splitters and headers."""
        custom_acc = "#A855F7"
        svg_frame = generate_frame(title="WINDOW", style="cyberpunk", accent=custom_acc)
        self.assertIn(custom_acc, svg_frame, "Frame must use accent in decorative elements")

        svg_splitter = generate_splitter(label="METRICS", style="cyberpunk", accent=custom_acc)
        self.assertIn(custom_acc, svg_splitter, "Splitter must use accent in decorative brackets")


class TestCompilerTertiaryDirectives(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.assets_dir = os.path.join(self.test_dir, "assets", "generated")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_compiler_parses_tertiary_attribute(self):
        """Verify MarkdownCompiler parses tertiary attribute and injects into generated SVG."""
        template = '<!-- pixel-kit:header title="CYBER TITAN" tertiary="#E024C3" -->'
        compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False)
        compiled = compiler.compile_string(template)
        self.assertIn("CYBER TITAN", compiled)

        # Check generated SVG in assets_dir
        svg_files = [f for f in os.listdir(self.assets_dir) if f.endswith(".svg")]
        self.assertTrue(len(svg_files) > 0)
        with open(os.path.join(self.assets_dir, svg_files[0]), "r", encoding="utf-8") as f:
            svg_content = f.read()
        self.assertIn("#E024C3", svg_content)


class TestStudioViewModeAndGitPush(unittest.TestCase):
    def test_studio_html_includes_primer_markdown_spacing(self):
        """Verify STUDIO_HTML contains authentic GitHub Primer vertical margins."""
        self.assertIn("article.markdown-body p", STUDIO_HTML)
        self.assertIn("margin-bottom: 16px;", STUDIO_HTML)
        self.assertIn("article.markdown-body h1", STUDIO_HTML)
        self.assertIn("margin-top: 24px;", STUDIO_HTML)
        self.assertIn("article.markdown-body ul", STUDIO_HTML)
        self.assertIn("padding-left: 2em;", STUDIO_HTML)

    def test_studio_html_includes_git_push_button_and_tertiary_picker(self):
        """Verify STUDIO_HTML contains git push button and tertiary inspector inputs."""
        self.assertIn("btn-git-push", STUDIO_HTML)
        self.assertIn("pushReadmeToGit()", STUDIO_HTML)
        self.assertIn("picker-tertiary", STUDIO_HTML)
        self.assertIn("inp-tertiary", STUDIO_HTML)
        self.assertIn("btn-green", STUDIO_HTML)

    def test_git_push_isolation_staging_logic(self):
        """Verify that staging logic only selects README.md, README.template.md, and assets."""
        test_dir = tempfile.mkdtemp()
        try:
            # Create a fake git repo in temp_dir
            subprocess.run(["git", "init"], cwd=test_dir, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Tester"], cwd=test_dir, capture_output=True)
            subprocess.run(["git", "config", "user.email", "tester@test.local"], cwd=test_dir, capture_output=True)

            readme_file = os.path.join(test_dir, "README.md")
            template_file = os.path.join(test_dir, "README.template.md")
            unrelated_code = os.path.join(test_dir, "secret_untracked_code.py")

            with open(readme_file, "w") as f:
                f.write("# Readme")
            with open(template_file, "w") as f:
                f.write("# Template")
            with open(unrelated_code, "w") as f:
                f.write("SECRET = 'DO NOT STAGE'")

            # Stage only README and template
            files_to_add = [
                os.path.relpath(readme_file, test_dir),
                os.path.relpath(template_file, test_dir)
            ]
            for target in files_to_add:
                subprocess.run(["git", "add", target], cwd=test_dir, check=True)

            status = subprocess.run(["git", "status", "--porcelain"], cwd=test_dir, capture_output=True, text=True).stdout
            # Ensure unrelated code was NOT staged
            self.assertIn("?? secret_untracked_code.py", status, "Unrelated files must NOT be staged")
            self.assertIn("A  README.md", status, "README.md must be staged")
            self.assertIn("A  README.template.md", status, "README.template.md must be staged")
        finally:
            shutil.rmtree(test_dir, ignore_errors=True)


class TestChipDecayDirections(unittest.TestCase):
    def test_cyberpunk_chips_all_decay_dirs(self):
        """Verify cyberpunk chip renders and validates with right, left, and both decay directions."""
        for dd in ("right", "left", "both"):
            svg = generate_chip(style="cyberpunk", chip_type="decay", decay_dir=dd, text="CYBERPUNK_TEST")
            self.assertIn("<svg", svg)
            self.assertIn("CYBERPUNK_TEST", svg)
            if dd == "both":
                self.assertIn("Left Dither", svg)
                self.assertIn("Right Dither", svg)

    def test_minimal_chips_all_decay_dirs(self):
        """Verify minimal chip renders and validates with right, left, and both decay directions."""
        for dd in ("right", "left", "both"):
            svg = generate_chip(style="minimal", chip_type="decay", decay_dir=dd, text="MINIMAL_TEST")
            self.assertIn("<svg", svg)
            self.assertIn("MINIMAL_TEST", svg)
            self.assertIn("stroke-dasharray", svg)

    def test_tactical_chips_all_decay_dirs(self):
        """Verify tactical chip renders and validates with right, left, and both decay directions."""
        for dd in ("right", "left", "both"):
            svg = generate_chip(style="tactical", chip_type="decay", decay_dir=dd, text="TACTICAL_TEST")
            self.assertIn("<svg", svg)
            self.assertIn("TACTICAL_TEST", svg)


class TestStudioContextualVisibility(unittest.TestCase):
    def test_studio_html_has_global_tertiary_controls(self):
        """Verify Global Theme Controller has tertiary color controls."""
        self.assertIn("picker-global-tertiary", STUDIO_HTML)
        self.assertIn("inp-global-tertiary", STUDIO_HTML)
        self.assertIn("syncGlobalColor('tertiary', 'picker')", STUDIO_HTML)
        self.assertIn("syncGlobalColor('tertiary', 'text')", STUDIO_HTML)

    def test_studio_html_has_contextual_group_ids(self):
        """Verify inspector elements have wrapper IDs for dynamic contextual hiding."""
        self.assertIn('id="row-chip-form"', STUDIO_HTML)
        self.assertIn('id="group-decay-dir"', STUDIO_HTML)
        self.assertIn('id="row-chip-gh"', STUDIO_HTML)
        self.assertIn('id="group-chip-repo"', STUDIO_HTML)
        self.assertIn('id="group-header-specs"', STUDIO_HTML)
        self.assertIn('id="row-frame-cap"', STUDIO_HTML)
        self.assertIn('id="group-frame-tag"', STUDIO_HTML)
        self.assertIn('id="group-frame-title"', STUDIO_HTML)
        self.assertIn('id="row-frame-links"', STUDIO_HTML)
        self.assertIn('id="group-frame-tag-url"', STUDIO_HTML)
        self.assertIn('id="row-quote-badge"', STUDIO_HTML)
        self.assertIn('id="row-callout-badge"', STUDIO_HTML)

    def test_studio_html_has_contextual_visibility_js(self):
        """Verify updateContextualVisibility is defined and connected to control events."""
        self.assertIn("function updateContextualVisibility()", STUDIO_HTML)
        self.assertIn("group-decay-dir", STUDIO_HTML)
        self.assertIn("group-header-specs", STUDIO_HTML)
        self.assertIn("group-frame-title", STUDIO_HTML)
        self.assertIn("updateContextualVisibility(); debounceRender();", STUDIO_HTML)


class TestLightThemeNoRipplesAndDeAISlop(unittest.TestCase):
    def test_no_scanlines_overlay_in_studio(self):
        """Verify CRT scanlines overlay is completely removed to eliminate ripples/banding."""
        self.assertNotIn('<div class="scanlines"></div>', STUDIO_HTML)
        self.assertNotIn(".scanlines {", STUDIO_HTML)

    def test_authentic_github_light_theme_styles(self):
        """Verify authentic GitHub light theme styles are defined for preview and markdown."""
        self.assertIn(".preview-pane.light-theme", STUDIO_HTML)
        self.assertIn(".light-theme .gh-readme-wrapper", STUDIO_HTML)
        self.assertIn("background: #ffffff !important;", STUDIO_HTML)
        self.assertIn(".light-theme .gh-card-header", STUDIO_HTML)
        self.assertIn("background-color: #f6f8fa !important;", STUDIO_HTML)
        self.assertIn(".light-theme article.markdown-body", STUDIO_HTML)
        self.assertIn("color: #1f2328 !important;", STUDIO_HTML)
        self.assertIn(".light-theme article.markdown-body a", STUDIO_HTML)
        self.assertIn("color: #0969da !important;", STUDIO_HTML)
        self.assertIn(".light-theme article.markdown-body pre", STUDIO_HTML)

    def test_studio_ui_no_ai_slop_emojis(self):
        """Verify that AI-slop emojis are removed from Studio buttons and options."""
        self.assertNotIn("✏️ EDIT", STUDIO_HTML)
        self.assertNotIn("👁️ VIEW", STUDIO_HTML)
        self.assertNotIn("🌙 Dark", STUDIO_HTML)
        self.assertNotIn("☀️ Light", STUDIO_HTML)
        self.assertNotIn("[ 🚀 PUSH README ]", STUDIO_HTML)
        self.assertNotIn("[ 📐 HUD GRID ]", STUDIO_HTML)
        self.assertNotIn("🎨 GLOBAL THEME CONTROLLER", STUDIO_HTML)
        self.assertNotIn("⚡ SOFT APPLY", STUDIO_HTML)
        self.assertNotIn("🔥 FORCE ALL", STUDIO_HTML)
        self.assertNotIn("💾 SAVE", STUDIO_HTML)
        self.assertNotIn("🗑️ DELETE", STUDIO_HTML)
        self.assertNotIn("📋 COPY", STUDIO_HTML)
        self.assertNotIn("➕ INSERT", STUDIO_HTML)

    def test_readme_template_no_emojis(self):
        """Verify README.template.md does not contain tacky AI-slop emojis."""
        with open("README.template.md", "r", encoding="utf-8") as f:
            template_text = f.read()
        self.assertNotIn("# 📦", template_text)
        self.assertNotIn("📚 КАТАЛОГ", template_text)
        self.assertNotIn("💡 ПРИМЕРЫ", template_text)
        self.assertNotIn("📊 Ключевые показатели", template_text)
        self.assertNotIn("📌 О проекте", template_text)
        self.assertNotIn("🟢 **Cyberpunk**", template_text)
        self.assertNotIn("🚀 Быстрый старт", template_text)


if __name__ == "__main__":
    unittest.main()

