"""
Unit tests for the modular Themes domain and Studio HTTP server.
Validates ThemeRegistry, ThemeCreator, color mathematics, and Theme API endpoints.
"""

import os
import json
import time
import shutil
import tempfile
import unittest
import threading
import urllib.request
import urllib.error

from generator.themes import (
    theme_registry,
    theme_creator,
    ThemeCreator,
    ThemeRegistry,
    ModePalette,
    ThemeDefinition,
    BASE_THEME_PALETTES,
    THEME_ALIASES,
)
from generator.themes.color_utils import (
    darken_hex,
    lighten_hex,
    is_light_color,
    contrast_ratio,
    get_shadow_colors,
    hex_to_rgb,
    rgb_to_hex,
)
from generator.studio.server import ThreadedStudioServer, StudioRequestHandler


class TestColorUtils(unittest.TestCase):
    def test_hex_rgb_conversions(self):
        r, g, b = hex_to_rgb("#ffffff")
        self.assertEqual((r, g, b), (255, 255, 255))
        self.assertEqual(rgb_to_hex(r, g, b), "#ffffff")

        r, g, b = hex_to_rgb("#000000")
        self.assertEqual((r, g, b), (0, 0, 0))
        self.assertEqual(rgb_to_hex(r, g, b), "#000000")

    def test_is_light_color(self):
        self.assertTrue(is_light_color("#ffffff"))
        self.assertTrue(is_light_color("#ffff00"))
        self.assertFalse(is_light_color("#000000"))
        self.assertFalse(is_light_color("#07090e"))

    def test_darken_and_lighten(self):
        darker = darken_hex("#808080", 0.5)
        self.assertNotEqual(darker, "#808080")
        lighter = lighten_hex("#808080", 0.5)
        self.assertNotEqual(lighter, "#808080")

    def test_contrast_ratio(self):
        cr = contrast_ratio("#ffffff", "#000000")
        self.assertGreater(cr, 20.0)
        cr_same = contrast_ratio("#123456", "#123456")
        self.assertAlmostEqual(cr_same, 1.0, places=1)

    def test_get_shadow_colors(self):
        mid, dark = get_shadow_colors("#00c8d7")
        self.assertTrue(mid.startswith("#"))
        self.assertTrue(dark.startswith("#"))


class TestThemeRegistry(unittest.TestCase):
    def test_registry_contains_base_themes(self):
        presets = theme_registry.list_presets()
        self.assertIn("cyberpunk", presets)
        self.assertIn("amber", presets)
        self.assertIn("matrix", presets)

    def test_resolve_theme_dark_and_light(self):
        dark_colors, css_dark = theme_registry.resolve_theme("cyberpunk", mode="dark")
        self.assertIsInstance(dark_colors, dict)
        self.assertTrue(dark_colors["primary"].startswith("#"))

        light_colors, css_light = theme_registry.resolve_theme("cyberpunk", mode="light")
        self.assertIsInstance(light_colors, dict)
        self.assertTrue(light_colors["primary"].startswith("#"))

    def test_resolve_fallback_for_unknown_theme(self):
        colors, _ = theme_registry.resolve_theme("completely_nonexistent_theme", mode="dark")
        self.assertEqual(colors["primary"], BASE_THEME_PALETTES["cyberpunk"]["dark"]["primary"])

    def test_resolve_colors_tuple(self):
        prim, acc, tert = theme_registry.resolve_colors("matrix", mode="dark")
        self.assertTrue(prim.startswith("#"))
        self.assertTrue(acc.startswith("#"))
        self.assertTrue(tert.startswith("#"))


class TestThemeCreator(unittest.TestCase):
    def test_generate_theme_strategies(self):
        for strategy in ["triadic", "complementary", "analogous"]:
            result = theme_creator.generate_theme(
                primary_hex="#ff007f",
                name=f"Test {strategy}",
                accent_strategy=strategy,
            )
            self.assertIn("preset", result)
            self.assertIn("dark", result)
            self.assertIn("light", result)
            self.assertEqual(result["preset"]["primary"].lower(), "#ff007f")

    def test_save_preset_and_load(self):
        temp_dir = tempfile.mkdtemp()
        try:
            creator = ThemeCreator(presets_dir=temp_dir)
            generated = creator.generate_theme("#39ff14", "Acid Green", "triadic")
            saved_path = creator.save_preset("acid-green", generated["preset"])
            self.assertTrue(os.path.isfile(saved_path))

            with open(saved_path, "r", encoding="utf-8") as f:
                saved_json = json.load(f)
            self.assertEqual(saved_json["theme"], "acid-green")
            self.assertEqual(saved_json["name"], "Acid Green")
            self.assertEqual(saved_json["primary"], "#39ff14")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestStudioThemeApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.template_file = os.path.join(cls.temp_dir, "README.template.md")
        cls.output_file = os.path.join(cls.temp_dir, "README.md")
        cls.assets_dir = os.path.join(cls.temp_dir, "assets").replace("\\", "/")

        with open(cls.template_file, "w", encoding="utf-8") as f:
            f.write("# Studio API Test\n")

        StudioRequestHandler.template_file = cls.template_file
        StudioRequestHandler.output_file = cls.output_file
        StudioRequestHandler.assets_dir = cls.assets_dir

        cls.server = ThreadedStudioServer(("127.0.0.1", 0), StudioRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.server.shutdown()
            cls.server.server_close()
        except Exception:
            pass
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_api_themes_endpoint(self):
        url = f"{self.base_url}/api/themes"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("themes", data)
            self.assertIn("presets", data)
            self.assertIn("cyberpunk", data["themes"])

    def test_api_theme_generate_endpoint(self):
        url = f"{self.base_url}/api/themes/generate"
        payload = json.dumps({
            "primary": "#e11d48",
            "name": "Rose Cyber",
            "strategy": "triadic"
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data["status"], "success")
            self.assertIn("theme", data)
            theme_obj = data["theme"]
            self.assertEqual(theme_obj["preset"]["primary"].lower(), "#e11d48")

    def test_api_theme_save_endpoint(self):
        url = f"{self.base_url}/api/themes/save"
        test_slug = "test-ephemeral-theme"
        payload = json.dumps({
            "slug": test_slug,
            "name": "Test Ephemeral Theme",
            "preset": {
                "theme": test_slug,
                "name": "Test Ephemeral Theme",
                "primary": "#10b981",
                "secondary": "#6366f1",
                "accent": "#f59e0b",
                "dark": {"primary": "#10b981", "accent": "#6366f1", "tertiary": "#f59e0b"},
                "light": {"primary": "#059669", "accent": "#4f46e5", "tertiary": "#d97706"},
            }
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data["status"], "saved")
            self.assertEqual(data["slug"], test_slug)

        # Cleanup saved preset file from presets/
        preset_file = os.path.join(theme_creator.presets_dir, f"{test_slug}.json")
        if os.path.isfile(preset_file):
            os.remove(preset_file)
        if test_slug in theme_registry._palettes:
            del theme_registry._palettes[test_slug]


if __name__ == "__main__":
    unittest.main()
