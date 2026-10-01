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

if __name__ == "__main__":
    unittest.main()
