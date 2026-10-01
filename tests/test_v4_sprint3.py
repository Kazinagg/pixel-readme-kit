import os
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from generator.engine import (
    generate_header,
    generate_social,
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
    generate_callout,
    generate_footer
)
from generator.compiler import MarkdownCompiler
from generator.mcp_server import tool_render_block, tool_compile_readme

class TestV4Sprint3(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.assets_dir = os.path.join(self.temp_dir, "assets").replace("\\", "/")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # --------------------------------------------------------------------------
    # 1. Compact Header Mode (Task 3.2)
    # --------------------------------------------------------------------------
    def test_compact_header_dimensions_and_validity(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_header(
                style=style,
                title="MICRO-CLI",
                subtitle="LEAN FAST RUNTIME",
                tag="V1.0",
                compact=True
            )
            # Must be valid XML
            root = ET.fromstring(svg)
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            self.assertEqual(root.attrib.get("viewBox"), "0 0 850 84")
            self.assertEqual(root.attrib.get("width"), "100%")
            self.assertIn("LEAN FAST RUNTIME", svg)
            self.assertIn("V1.0", svg)

    def test_compact_header_directive_compilation(self):
        template = """# Project
<!-- pixel-kit:header style="tactical" title="FAST-API" subtitle="LIGHTWEIGHT SERVICE" compact="true" -->
Some content here.
"""
        template_path = os.path.join(self.temp_dir, "README.template.md")
        output_path = os.path.join(self.temp_dir, "README.md")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template)

        compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False)
        compiler.compile_file(template_path, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            compiled = f.read()

        self.assertIn("FAST-API", compiled)
        # Check generated asset
        generated_files = os.listdir(self.assets_dir)
        self.assertTrue(any("header-tactical" in f for f in generated_files))
        for f in generated_files:
            if "header-tactical" in f:
                with open(os.path.join(self.assets_dir, f), "r", encoding="utf-8") as svg_f:
                    svg_content = svg_f.read()
                root = ET.fromstring(svg_content)
                self.assertEqual(root.attrib.get("viewBox"), "0 0 850 84")

    # --------------------------------------------------------------------------
    # 2. Camo Cache-Buster (Task 3.3)
    # --------------------------------------------------------------------------
    def test_camo_cache_buster(self):
        template = """<!-- pixel-kit:chip text="CACHE_TEST" -->"""
        template_path = os.path.join(self.temp_dir, "README.template.md")
        output_path = os.path.join(self.temp_dir, "README.md")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template)

        # 1. Without cache-buster
        compiler_plain = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False, bust_cache=False)
        compiler_plain.compile_file(template_path, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            plain_content = f.read()
        self.assertNotIn("?v=", plain_content)

        # 2. With cache-buster
        compiler_busting = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False, bust_cache=True)
        compiler_busting.compile_file(template_path, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            busted_content = f.read()
        self.assertIn("?v=", busted_content)

        # Check fragment preservation (#gh-dark-mode-only) if present in table wrappers
        template_dual = """<!-- pixel-kit:header title="DUAL" mode="auto" -->"""
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_dual)
        compiler_busting.compile_file(template_path, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            dual_content = f.read()
        # Verify that if #gh-dark-mode-only exists, ?v= precedes it
        if "#gh-dark-mode-only" in dual_content:
            import re
            match = re.search(r'\?v=[a-f0-9]+#gh-dark-mode-only', dual_content)
            self.assertIsNotNone(match, "Cache bust hash must appear before the #gh-dark-mode-only anchor")

    # --------------------------------------------------------------------------
    # 3. OpenGraph 1280x640 Social Card (Task 3.4)
    # --------------------------------------------------------------------------
    def test_social_card_generation(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_social(
                style=style,
                title="NEURAL MATRIX",
                subtitle="ADVANCED DEEP LEARNING COMPILATION ENGINE",
                repo="Kazinagg/neural-matrix",
                tags=["PYTHON", "CUDA", "PYTORCH", "NEURAL-ENGINE"]
            )
            root = ET.fromstring(svg)
            self.assertEqual(root.attrib.get("viewBox"), "0 0 1280 640")
            self.assertEqual(root.attrib.get("width"), "100%")
            self.assertIn("ADVANCED DEEP LEARNING COMPILATION ENGINE", svg)
            self.assertIn("KAZINAGG/NEURAL-MATRIX", svg)
            self.assertIn("CUDA", svg)

    def test_social_card_directive_compilation(self):
        template = """<!-- pixel-kit:social style="cyberpunk" title="DEMO SOCIAL" subtitle="TEST CARD" repo="author/repo" tags="AI,ML" -->"""
        template_path = os.path.join(self.temp_dir, "README.template.md")
        output_path = os.path.join(self.temp_dir, "README.md")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template)

        compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False)
        compiler.compile_file(template_path, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            compiled = f.read()

        self.assertIn("DEMO SOCIAL", compiled)
        self.assertIn("social-cyberpunk", compiled)

    # --------------------------------------------------------------------------
    # 4. Safe Mobile Font Hierarchy (Task 3.1)
    # --------------------------------------------------------------------------
    def test_safe_mobile_font_sizes(self):
        # Generate various components and verify that text elements have font-size >= 11
        svgs = [
            generate_callout(style="cyberpunk", callout_type="note", title="NOTE", subtitle="Checking font legibility"),
            generate_footer(style="tactical", status="ONLINE", nav_text="BACK TO TOP"),
            generate_progress(style="minimal", value=80, label="BUILD PROGRESS", sub="COMPILING ASSETS"),
            generate_techstack(style="cyberpunk", items=["python", "docker"]),
            generate_timeline(style="tactical")
        ]

        import re
        font_size_pattern = re.compile(r'font-size[:=]["\']?(\d+(?:\.\d+)?)')
        for svg in svgs:
            # Parse XML to find all text elements
            root = ET.fromstring(svg)
            for elem in root.iter():
                if elem.tag.endswith("text") or elem.tag.endswith("tspan"):
                    text_str = "".join(elem.itertext()).strip()
                    # Skip decorative single-char ascii symbols or empty texts
                    if not text_str or len(text_str) <= 1:
                        continue
                    fs = elem.attrib.get("font-size")
                    if fs:
                        val = float(re.sub(r'[^\d.]', '', fs))
                        self.assertGreaterEqual(val, 11, f"Found readable text with sub-11px font size {val}: {text_str}")

    # --------------------------------------------------------------------------
    # 5. MCP Server Extensions for Sprint 3
    # --------------------------------------------------------------------------
    def test_mcp_social_and_compact_header(self):
        # Test compact header via MCP
        res_hdr = tool_render_block(block_type="header", title="MCP COMPACT", compact=True)
        self.assertTrue(res_hdr["success"])
        root_hdr = ET.fromstring(res_hdr["svg"])
        self.assertEqual(root_hdr.attrib.get("viewBox"), "0 0 850 84")

        # Test social block via MCP
        res_soc = tool_render_block(
            block_type="social",
            title="MCP SOCIAL CARD",
            subtitle="TESTING MCP SOCIAL INTEGRATION",
            tags="PYTHON,MCP,TEST"
        )
        self.assertTrue(res_soc["success"])
        root_soc = ET.fromstring(res_soc["svg"])
        self.assertEqual(root_soc.attrib.get("viewBox"), "0 0 1280 640")

if __name__ == "__main__":
    unittest.main()
