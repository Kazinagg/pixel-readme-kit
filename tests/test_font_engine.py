"""
Unit tests for Font Engine (generator/font_engine.py)
Validates smart downscaling, word-wrapping, Cyrillic glyphs, and 3D rendering.
"""

import unittest
import xml.etree.ElementTree as ET
from generator.font_engine import (
    calculate_smart_layout,
    render_3d_text,
    GLYPHS,
)


class TestFontEngine(unittest.TestCase):

    def test_short_title_layout(self):
        # Short title uses maximum px_size (6) on single line
        lines, px_size = calculate_smart_layout("PIXEL-KIT", max_width=480)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "PIXEL-KIT")
        self.assertGreaterEqual(px_size, 5)

    def test_long_title_word_wrap(self):
        # Long multi-word title wraps cleanly to 2 lines
        text = "RETRO CYBERPUNK HUD DESIGN SYSTEM"
        lines, px_size = calculate_smart_layout(text, max_width=480)
        self.assertEqual(len(lines), 2)
        # Verify no words were lost or concatenated weirdly
        reconstructed = " ".join(lines)
        self.assertEqual(reconstructed, text)

    def test_cyrillic_glyph_coverage(self):
        # Verify common Russian letters exist in glyph matrix
        test_chars = "ПРОЕКТКИБЕРПАНКЁ0123456789"
        for char in test_chars:
            self.assertIn(char, GLYPHS, f"Missing glyph for character: {char}")

    def test_render_3d_text_xml_validity(self):
        markup, total_w, total_h = render_3d_text(
            "HUD V3.0",
            x=20,
            y=40,
            front_color="#00C8D7",
            mid_shadow="#006B74",
            dark_shadow="#002B2F"
        )
        self.assertGreater(total_w, 0)
        self.assertGreater(total_h, 0)
        # Wrap in a mini SVG to test XML validity
        test_svg = f'<svg xmlns="http://www.w3.org/2000/svg">{markup}</svg>'
        root = ET.fromstring(test_svg)
        self.assertIsNotNone(root)


if __name__ == "__main__":
    unittest.main()
