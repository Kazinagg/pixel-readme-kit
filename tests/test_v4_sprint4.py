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

from generator.server import ThreadedStudioServer, StudioRequestHandler

class TestV4Sprint4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.template_file = os.path.join(cls.temp_dir, "README.template.md")
        cls.output_file = os.path.join(cls.temp_dir, "README.md")
        cls.assets_dir = os.path.join(cls.temp_dir, "assets").replace("\\", "/")

        # Create basic template
        with open(cls.template_file, "w", encoding="utf-8") as f:
            f.write("# Studio Test\n<!-- pixel-kit:chip text=\"STUDIO_ACTIVE\" -->\n")

        # Configure handler
        StudioRequestHandler.template_file = cls.template_file
        StudioRequestHandler.output_file = cls.output_file
        StudioRequestHandler.assets_dir = cls.assets_dir

        # Start server on dynamic port (port 0)
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

    def test_01_studio_ui_html(self):
        req = urllib.request.urlopen(f"{self.base_url}/")
        self.assertEqual(req.status, 200)
        content_type = req.headers.get("Content-Type")
        self.assertIn("text/html", content_type)
        html = req.read().decode("utf-8")
        self.assertIn("PIXEL README KIT", html)
        self.assertIn("HUD STUDIO", html)
        self.assertIn("LIVE SVG PREVIEW", html)

    def test_02_api_presets(self):
        req = urllib.request.urlopen(f"{self.base_url}/api/presets")
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode("utf-8"))
        self.assertIn("presets", data)
        self.assertIn("icons", data)
        self.assertIn("cyberpunk", data["presets"])
        self.assertIn("python", data["icons"])

    def test_03_api_render_svg_blocks(self):
        block_types = [
            "header", "footer", "callout", "frame", "chip",
            "divider", "splitter", "metrics", "progress", "techstack",
            "timeline", "social"
        ]
        for btype in block_types:
            url = f"{self.base_url}/api/render?block_type={btype}&style=cyberpunk&title=TEST_{btype.upper()}"
            req = urllib.request.urlopen(url)
            self.assertEqual(req.status, 200, f"Render failed for {btype}")
            self.assertIn("image/svg+xml", req.headers.get("Content-Type"))
            svg_content = req.read().decode("utf-8")
            # Must be valid XML
            root = ET.fromstring(svg_content)
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_04_api_preview_and_recompile(self):
        req = urllib.request.urlopen(f"{self.base_url}/api/preview")
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode("utf-8"))
        self.assertEqual(data["status"], "success")
        self.assertIn("html", data)
        self.assertIn("Studio Test", data["html"])

        # Recompile
        req_rec = urllib.request.Request(f"{self.base_url}/api/recompile", data=b"", method="POST")
        resp = urllib.request.urlopen(req_rec)
        self.assertEqual(resp.status, 200)

    def test_05_api_insert_directive(self):
        directive = "<!-- pixel-kit:divider style=\"cyberpunk\" -->"
        payload = json.dumps({"directive": directive}).encode("utf-8")
        req_ins = urllib.request.Request(
            f"{self.base_url}/api/insert",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req_ins)
        self.assertEqual(resp.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            updated_content = f.read()
        self.assertIn("pixel-kit:divider", updated_content)

    def test_06_api_template_blocks(self):
        req = urllib.request.urlopen(f"{self.base_url}/api/template/blocks")
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode("utf-8"))
        self.assertEqual(data["status"], "success")
        self.assertIn("blocks", data)
        self.assertGreaterEqual(len(data["blocks"]), 1)
        first_blk = data["blocks"][0]
        self.assertEqual(first_blk["type"], "chip")
        self.assertEqual(first_blk["attrs"].get("text"), "STUDIO_ACTIVE")

    def test_07_api_template_update_block(self):
        # Update the first block (chip)
        new_directive = '<!-- pixel-kit:chip text="UPDATED_TEXT" style="tactical" -->'
        payload = json.dumps({"id": 0, "directive_raw": new_directive}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/template/update_block",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req)
        self.assertEqual(resp.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('UPDATED_TEXT', content)
        self.assertIn('style="tactical"', content)

    def test_08_api_template_delete_block(self):
        # Delete block 0
        payload = json.dumps({"id": 0}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/template/delete_block",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req)
        self.assertEqual(resp.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn('UPDATED_TEXT', content)

    def test_09_api_template_insert_block(self):
        # Insert a block after position -1 (at top)
        new_directive = '<!-- pixel-kit:callout style="cyberpunk" title="INSERTED_AT_TOP" -->'
        payload = json.dumps({"after_id": -1, "directive_raw": new_directive}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/template/insert_block",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req)
        self.assertEqual(resp.status, 200)

        with open(self.template_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('INSERTED_AT_TOP', content)

    def test_10_api_render_extended_specs(self):
        url = (
            f"{self.base_url}/api/render?block_type=header&style=cyberpunk"
            "&title=SPEC_TEST&spec1=CORE+5.15&spec2=10Gbps+NET&spec3=STATUS+NOMINAL"
        )
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = resp.read().decode("utf-8")
            self.assertIn("CORE 5.15", data)
            self.assertIn("10Gbps NET", data)
            self.assertIn("STATUS NOMINAL", data)

    def test_11_api_render_extended_chip_and_metrics(self):
        # Chip with decay_dir
        chip_url = f"{self.base_url}/api/render?block_type=chip&style=cyberpunk&title=TEST_CHIP&type=decay&decay_dir=both&width=180"
        with urllib.request.urlopen(chip_url) as resp:
            self.assertEqual(resp.status, 200)
            chip_svg = resp.read().decode("utf-8")
            self.assertIn("<svg", chip_svg)

        # Metrics with items
        metrics_url = f"{self.base_url}/api/render?block_type=metrics&style=cyberpunk&items=FPS:+120|MEM:+64MB"
        with urllib.request.urlopen(metrics_url) as resp:
            self.assertEqual(resp.status, 200)
            metrics_svg = resp.read().decode("utf-8")
            self.assertIn("120", metrics_svg)
            self.assertIn("64MB", metrics_svg)

    def test_12_markdown_gfm_rendering(self):
        handler = StudioRequestHandler
        gfm_md = """| Header 1 | Header 2 |
| :--- | :--- |
| Cell 1 | Cell 2 |

- [x] Completed task
- [ ] Open task

> [!NOTE]
> Important advisory info.
"""
        html = handler.markdown_to_html(handler, gfm_md)
        self.assertIn("<table>", html)
        self.assertIn("<th", html)
        self.assertIn("task-list-item-checkbox", html)
        self.assertIn("markdown-alert-note", html)

    def test_13_timeline_and_global_theme(self):
        # 1. Timeline render with milestones
        t_url = f"{self.base_url}/api/render?block_type=timeline&body=" + urllib.parse.quote('milestone title="ALPHA" date="2026-Q1" status="COMPLETED" desc="Testing"')
        with urllib.request.urlopen(t_url) as resp:
            self.assertEqual(resp.status, 200)
            t_svg = resp.read().decode("utf-8")
            self.assertIn("<svg", t_svg)
            self.assertIn("ALPHA", t_svg)

        # 2. Apply global theme endpoint
        apply_url = f"{self.base_url}/api/template/apply_global_theme"
        payload = json.dumps({
            "style": "tactical",
            "preset": "amber",
            "mode": "auto",
            "primary": "",
            "accent": ""
        }).encode("utf-8")
        req = urllib.request.Request(apply_url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)

        # 3. Preview theme injection
        with urllib.request.urlopen(f"{self.base_url}/api/preview?theme=light") as resp:
            self.assertEqual(resp.status, 200)
            p_data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("theme=light", p_data["html"])

if __name__ == "__main__":
    unittest.main()


