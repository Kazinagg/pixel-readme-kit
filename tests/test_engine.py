"""
Unit tests for Core Engine (generator/engine.py)
Validates XML integrity, theming modes, presets, responsive callouts, and SVG generation.
"""

import unittest
import xml.etree.ElementTree as ET
from generator.engine import (
    load_preset,
    resolve_theme,
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    validate_svg,
)


class TestEngine(unittest.TestCase):

    def assert_valid_svg(self, svg_str):
        self.assertIsInstance(svg_str, str)
        self.assertTrue(svg_str.startswith("<svg"))
        self.assertTrue(svg_str.rstrip().endswith("</svg>"))
        # Parse XML - throws on syntax error
        root = ET.fromstring(svg_str)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_load_preset(self):
        for name in ["cyberpunk", "amber", "matrix", "tokyo"]:
            data = load_preset(name)
            self.assertIsNotNone(data, f"Failed to load preset: {name}")
            self.assertIn("primary", data)

        self.assertIsNone(load_preset(None))
        self.assertIsNone(load_preset("non_existent_preset_xyz"))

    def test_resolve_theme_modes(self):
        # Auto mode returns CSS variables
        colors, css_vars = resolve_theme("cyberpunk", mode="auto")
        self.assertIn("var(--primary)", colors["primary"])
        self.assertIn("@media (prefers-color-scheme: dark)", css_vars)

        # Dark mode returns direct hex/rgba
        colors_dark, css_dark = resolve_theme("cyberpunk", mode="dark")
        self.assertEqual(css_dark, "")
        self.assertTrue(colors_dark["primary"].startswith("#"))

        # Light mode returns direct hex/rgba
        colors_light, css_light = resolve_theme("cyberpunk", mode="light")
        self.assertEqual(css_light, "")
        self.assertTrue(colors_light["primary"].startswith("#"))

        # Transparent mode removes background
        colors_tr, _ = resolve_theme("cyberpunk", mode="transparent")
        self.assertEqual(colors_tr["bg"], "none")

    def test_resolve_theme_preset_override(self):
        colors, css_vars = resolve_theme("cyberpunk", mode="auto", preset="matrix")
        self.assertIn("#00FF66", css_vars)  # Matrix green primary

    def test_generate_header_all_styles(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_header(
                style=style,
                title="TEST HEADER",
                subtitle="TEST SUBTITLE",
                tag="UNIT_TEST",
                specs=[("SPEC 1", "VAL 1", "#00FF66"), ("SPEC 2", "VAL 2", "#00C8D7")]
            )
            self.assert_valid_svg(svg)

    def test_generate_header_links(self):
        svg = generate_header(
            style="cyberpunk",
            title="LINKED HEADER",
            tag="RELEASE",
            tag_url="https://github.com/test/repo/releases",
            close_url="https://github.com/test/repo/issues"
        )
        self.assert_valid_svg(svg)
        self.assertIn('href="https://github.com/test/repo/releases"', svg)
        self.assertIn('href="https://github.com/test/repo/issues"', svg)

    def test_generate_header_long_title_wrap(self):
        svg = generate_header(
            style="cyberpunk",
            title="THIS IS AN EXTREMELY LONG PROJECT TITLE FOR WORD WRAPPING",
            subtitle="SUBTITLE UNDER MULTILINE TITLE",
            specs=[("SPEC 1", "VAL 1"), ("SPEC 2", "VAL 2"), ("SPEC 3", "VAL 3")]
        )
        self.assert_valid_svg(svg)
        # Check that viewBox height dynamically increased past 260
        root = ET.fromstring(svg)
        vb = root.attrib.get("viewBox", "")
        h = int(vb.split()[-1])
        self.assertGreater(h, 260)

    def test_generate_footer(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_footer(style=style, status="ALL_SYSTEMS_GO", nav_text="RETURN UP")
            self.assert_valid_svg(svg)
            self.assertIn(".btn-hover", svg)

    def test_generate_callout_responsive_wrap(self):
        # Short subtitle
        svg_short = generate_callout(
            style="cyberpunk",
            title="NOTE TITLE",
            subtitle="Short description"
        )
        self.assert_valid_svg(svg_short)
        h_short = int(ET.fromstring(svg_short).attrib["viewBox"].split()[-1])
        self.assertEqual(h_short, 48)

        # Long subtitle (> 105 chars) -> expands to 62px
        long_sub = "This is a very detailed architectural warning message that provides extensive operational context and requires line wrapping."
        svg_long = generate_callout(
            style="cyberpunk",
            title="WARNING TITLE",
            subtitle=long_sub
        )
        self.assert_valid_svg(svg_long)
        h_long = int(ET.fromstring(svg_long).attrib["viewBox"].split()[-1])
        self.assertEqual(h_long, 62)

    def test_generate_callout_quote_mode(self):
        svg_q = generate_callout(
            style="tactical",
            title="QUOTE TITLE",
            subtitle="Flows into live text",
            is_quote=True
        )
        self.assert_valid_svg(svg_q)
        self.assertIn("stroke-dasharray", svg_q)

    def test_generate_frame(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg_top = generate_frame(
                style=style,
                frame_type="top",
                title="WINDOW_TOP",
                tag="[OPEN]",
                tag_url="https://github.com",
                close_url="https://github.com/issues"
            )
            self.assert_valid_svg(svg_top)
            self.assertIn("href=\"https://github.com\"", svg_top)

            svg_bot = generate_frame(style=style, frame_type="bottom", tag="[SYSTEM.CLOSED]")
            self.assert_valid_svg(svg_bot)

    def test_generate_chip(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            for ctype in ["closed", "decay", "pulse"]:
                svg = generate_chip(style=style, chip_type=ctype, text="⚡ v3.0.0")
                self.assert_valid_svg(svg)

    def test_generate_divider_and_splitter(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg_div = generate_divider(style=style)
            self.assert_valid_svg(svg_div)

            svg_spl = generate_splitter(style=style, label="[MODULE: DATABASE]")
            self.assert_valid_svg(svg_spl)


if __name__ == "__main__":
    unittest.main()
