import os
import time
import json
import shutil
import tempfile
import unittest
import urllib.request
import urllib.error
import threading
import xml.etree.ElementTree as ET

from generator.engine import generate_callout, GITHUB_ALERT_COLORS
from generator.compiler import MarkdownCompiler
from generator.server import ThreadedStudioServer, StudioRequestHandler
from generator.cli import build_parser


class TestV42Studio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.template_file = os.path.join(cls.temp_dir, "README.template.md")
        cls.output_file = os.path.join(cls.temp_dir, "README.md")
        cls.assets_dir = os.path.join(cls.temp_dir, "assets").replace("\\", "/")

        # Initial template with custom accent and custom badge_color
        initial_template = (
            "# Sprint 4.2 Test\n\n"
            '<!-- pixel-kit:chip text="CHIP_1" accent="#ff0000" badge_color="#00ff00" -->\n\n'
            '<!-- pixel-kit:metric label="CPU" value="99" style="cyberpunk" -->\n'
        )
        with open(cls.template_file, "w", encoding="utf-8") as f:
            f.write(initial_template)

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
        cls.server.shutdown()
        cls.server.server_close()
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_callout_github_alert_colors(self):
        """Test automatic mapping to GitHub Alert standard colors."""
        alerts = {
            "NOTE": GITHUB_ALERT_COLORS["NOTE"],
            "TIP": GITHUB_ALERT_COLORS["TIP"],
            "WARNING": GITHUB_ALERT_COLORS["WARNING"],
            "CRITICAL": GITHUB_ALERT_COLORS["CRITICAL"],
            "IMPORTANT": GITHUB_ALERT_COLORS["IMPORTANT"],
        }
        for alert_type, expected_color in alerts.items():
            svg = generate_callout(
                title=f"Body for {alert_type}",
                callout_type=alert_type.lower(),
                style="tactical"
            )
            # Check that SVG contains the GitHub standard color
            self.assertIn(
                expected_color.lower(),
                svg.lower(),
                f"Callout type {alert_type} should contain {expected_color}"
            )

    def test_02_callout_custom_badge_color(self):
        """Test explicit custom hex badge_color overrides."""
        custom_color = "#e024c3"
        svg = generate_callout(
            title="Custom badge color test",
            callout_type="note",
            style="tactical",
            badge_color=custom_color
        )
        self.assertIn(custom_color.lower(), svg.lower())

        # Test quote author with custom badge_color
        quote_color = "#38ef7d"
        quote_svg = generate_callout(
            title="Knowledge is power",
            is_quote=True,
            style="cyberpunk",
            badge_color=quote_color
        )
        self.assertIn(quote_color.lower(), quote_svg.lower())

    def test_03_compiler_callout_and_quote_badge_color(self):
        """Test markdown compiler parsing and forwarding badge_color in directives."""
        test_assets = os.path.join(self.temp_dir, "test_assets")
        compiler = MarkdownCompiler(assets_dir=test_assets)

        content = (
            '<!-- pixel-kit:callout type="warning" badge_color="#ab12cd" title="Alert title" subtitle="Alert message" -->\n\n'
            '<!-- pixel-kit:quote badge_color="#45ab89" title="ADA" subtitle="Computing poetry" -->\n'
            'The Analytical Engine weaves algebraic patterns just as the Jacquard loom weaves flowers.\n'
            '<!-- /pixel-kit:quote -->\n'
        )
        compiled = compiler.compile_text(content)
        self.assertIn("<img", compiled)

        # Check compiled assets
        asset_files = os.listdir(test_assets)
        self.assertGreaterEqual(len(asset_files), 2)

        found_callout = False
        found_quote = False
        for f in asset_files:
            if f.endswith(".svg"):
                with open(os.path.join(test_assets, f), "r", encoding="utf-8") as svg_file:
                    svg_data = svg_file.read().lower()
                    if "#ab12cd" in svg_data:
                        found_callout = True
                    if "#45ab89" in svg_data:
                        found_quote = True

        self.assertTrue(found_callout, "Compiled callout asset should contain custom badge_color #ab12cd")
        self.assertTrue(found_quote, "Compiled quote asset should contain custom badge_color #45ab89")

    def test_04_api_apply_global_theme_soft_vs_force(self):
        """Test /api/template/apply_global_theme with force=false vs force=true."""
        # Reset template with custom accent and badge_color
        initial_template = (
            "# Global Theme Test\n\n"
            '<!-- pixel-kit:chip text="CHIP_1" accent="#ff0000" badge_color="#00ff00" -->\n\n'
            '<!-- pixel-kit:metric label="CPU" value="99" style="cyberpunk" -->\n'
        )
        with open(self.template_file, "w", encoding="utf-8") as f:
            f.write(initial_template)

        # 1. Soft Apply (force = False)
        payload_soft = {
            "style": "tactical",
            "preset": "amber",
            "mode": "dark",
            "force": False
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/template/apply_global_theme",
            data=json.dumps(payload_soft).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        self.assertEqual(res.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            soft_content = f.read()

        # In Soft Apply, accent="#ff0000" and badge_color="#00ff00" MUST BE PRESERVED
        self.assertIn('accent="#ff0000"', soft_content)
        self.assertIn('badge_color="#00ff00"', soft_content)
        self.assertIn('style="tactical"', soft_content)

        # 2. Force Override (force = True)
        payload_force = {
            "style": "cyberpunk",
            "preset": "matrix",
            "mode": "dark",
            "force": True
        }
        req_force = urllib.request.Request(
            f"{self.base_url}/api/template/apply_global_theme",
            data=json.dumps(payload_force).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res_force = urllib.request.urlopen(req_force)
        self.assertEqual(res_force.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            force_content = f.read()

        # In Force Override, custom accents and badge_color MUST BE STRIPPED
        self.assertNotIn('accent="#ff0000"', force_content)
        self.assertNotIn('badge_color="#00ff00"', force_content)
        self.assertIn('preset="matrix"', force_content)

        # 3. Custom Preset Apply
        payload_custom = {
            "style": "minimal",
            "preset": "custom",
            "primary": "#334455",
            "accent": "#667788",
            "mode": "transparent",
            "force": True
        }
        req_custom = urllib.request.Request(
            f"{self.base_url}/api/template/apply_global_theme",
            data=json.dumps(payload_custom).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res_custom = urllib.request.urlopen(req_custom)
        self.assertEqual(res_custom.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            custom_content = f.read()

        self.assertIn('primary="#334455"', custom_content)
        self.assertIn('accent="#667788"', custom_content)
        self.assertNotIn('preset="custom"', custom_content)

    def test_05_studio_markup_and_css(self):
        """Test presence of Studio UI elements for View Mode, Custom Preset, and Badge Colors."""
        req = urllib.request.urlopen(f"{self.base_url}/")
        self.assertEqual(req.status, 200)
        html = req.read().decode("utf-8")

        # View Mode Switcher
        self.assertIn('id="tab-mode-edit"', html)
        self.assertIn('id="tab-mode-view"', html)

        # CSS View Mode Rules
        self.assertIn('.view-mode .pk-insert-divider', html)
        self.assertIn('.view-mode .pk-block-hud-bar', html)
        self.assertIn('.view-mode .pk-block-wrapper[data-pk-type="chip"]', html)

        # Global Theme buttons & Custom Preset
        self.assertIn('SOFT APPLY', html)
        self.assertIn('FORCE ALL', html)
        self.assertIn('value="custom"', html)

        # Inspector Badge Color controls
        self.assertIn('inp-quote-badge-color', html)
        self.assertIn('inp-callout-badge-color', html)
        self.assertIn('chk-quote-custom-badge', html)
        self.assertIn('chk-callout-custom-badge', html)

    def test_06_cli_and_render_endpoint(self):
        """Test CLI arguments and /api/render endpoint badge_color support."""
        # Test CLI parser accepts --badge-color
        parser = build_parser()
        args = parser.parse_args([
            "callout",
            "--title", "Warning message",
            "--type", "warning",
            "--badge-color", "#f85149"
        ])
        self.assertEqual(args.badge_color, "#f85149")

        # Test /api/render with badge_color
        url = f"{self.base_url}/api/render?block_type=callout&title=RenderTest&callout_type=tip&badge_color=%23129934"
        req = urllib.request.urlopen(url)
        self.assertEqual(req.status, 200)
        svg = req.read().decode("utf-8")
        self.assertIn("#129934", svg.lower())

    def test_07_preview_view_html(self):
        """Test that /api/preview returns authentic view_html without interactive block wrappers."""
        req = urllib.request.urlopen(f"{self.base_url}/api/preview")
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode("utf-8"))
        self.assertIn("html", data)
        self.assertIn("view_html", data)

        # In edit html, wrappers and dividers must exist
        self.assertIn("pk-block-wrapper", data["html"])
        self.assertIn("pk-insert-divider", data["html"])

        # In view_html, no interactive wrappers or dividers should exist (100% authentic GitHub render)
        self.assertNotIn("pk-block-wrapper", data["view_html"])
        self.assertNotIn("pk-insert-divider", data["view_html"])
        self.assertNotIn("pk-block-hud-bar", data["view_html"])

    def test_08_inspector_width_and_custom_scrollbars(self):
        """Test presence of custom HUD scrollbars and widened inspector drawer."""
        req = urllib.request.urlopen(f"{self.base_url}/")
        self.assertEqual(req.status, 200)
        html = req.read().decode("utf-8")

        # Custom scrollbar CSS
        self.assertIn("::-webkit-scrollbar", html)
        self.assertIn("scrollbar-width: thin", html)

        # Inspector width 580px and overflow-x hidden
        self.assertIn("width: 580px", html)
        self.assertIn("margin-right: -580px", html)
        self.assertIn("overflow-x: hidden", html)


if __name__ == "__main__":
    unittest.main()

