"""
Unit tests for Pixel Readme Kit v4.0 Sprint 2:
- Vector Pixel Icon Registry (generator/icons.py)
- Metrics Card Generator (generate_metrics)
- Progress Bar Generator (generate_progress)
- Tech Stack Matrix Generator (generate_techstack)
- Timeline Generator (generate_timeline)
- Compiler directives integration for Sprint 2 widgets
- MCP Server render_block integration
"""

import os
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from generator.icons import get_icon, list_available_icons
from generator.engine import (
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
)
from generator.compiler import MarkdownCompiler
from generator.mcp_server import tool_render_block


class TestSprint2(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="pixel_kit_sprint2_")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _assert_valid_xml(self, svg_content: str):
        try:
            root = ET.fromstring(svg_content)
            self.assertEqual(root.tag.split("}")[-1], "svg")
            return root
        except ET.ParseError as e:
            self.fail(f"Invalid XML generated: {e}\nContent snippet:\n{svg_content[:400]}")

    # --------------------------------------------------------------------------
    # 1. ICON REGISTRY
    # --------------------------------------------------------------------------
    def test_icon_registry(self):
        icons = list_available_icons()
        self.assertIn("python", icons)
        self.assertIn("cpp", icons)
        self.assertIn("docker", icons)
        self.assertIn("git", icons)
        self.assertIn("rust", icons)

        py_icon = get_icon("python")
        self.assertIsNotNone(py_icon)
        self.assertIn("<path", py_icon)

        # Fallback for unknown icon
        unknown = get_icon("nonexistent_tool_xyz")
        self.assertIsNone(unknown)

    # --------------------------------------------------------------------------
    # 2. METRICS GENERATOR
    # --------------------------------------------------------------------------
    def test_metrics_single_card(self):
        cards = [{"label": "CPU LOAD", "value": "24%", "delta": "+2.4% vs baseline", "trend": "up", "status": "NOMINAL"}]
        svg = generate_metrics(cards=cards, style="cyberpunk", mode="dark")
        root = self._assert_valid_xml(svg)
        self.assertIn("CPU LOAD", svg)
        self.assertIn("24%", svg)
        self.assertIn("+2.4% vs baseline", svg)

    def test_metrics_multi_card_styles(self):
        cards = [
            {"label": "REQUESTS", "value": "1.2M", "delta": "+15%", "trend": "up"},
            {"label": "LATENCY", "value": "12ms", "delta": "-4ms", "trend": "down"},
            {"label": "UPTIME", "value": "99.98%", "status": "STEADY", "trend": "neutral"},
        ]
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_metrics(cards=cards, style=style, mode="auto")
            self._assert_valid_xml(svg)

    # --------------------------------------------------------------------------
    # 3. PROGRESS GENERATOR
    # --------------------------------------------------------------------------
    def test_progress_bar_values(self):
        for val in [0, 25, 75, 100]:
            svg = generate_progress(value=val, label="DEPLOYMENT", sub=f"STAGE {val}%", style="cyberpunk")
            self._assert_valid_xml(svg)
            self.assertIn("DEPLOYMENT", svg)
            self.assertIn(f"{val}%", svg)

    def test_progress_bar_styles(self):
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_progress(value=60, label="BUILD PROGRESS", style=style, mode="light")
            self._assert_valid_xml(svg)

    # --------------------------------------------------------------------------
    # 4. TECHSTACK GENERATOR
    # --------------------------------------------------------------------------
    def test_techstack_generation(self):
        items = [
            {"name": "Python", "icon": "python", "label": "Backend"},
            {"name": "C++", "icon": "cpp", "label": "Engine"},
            {"name": "Docker", "icon": "docker", "label": "Infra"},
            {"name": "Git", "icon": "git", "label": "VCS"},
        ]
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_techstack(items=items, columns=4, style=style, mode="auto")
            root = self._assert_valid_xml(svg)
            self.assertIn("PYTHON", svg)
            self.assertIn("BACKEND", svg)

    # --------------------------------------------------------------------------
    # 5. TIMELINE GENERATOR
    # --------------------------------------------------------------------------
    def test_timeline_generation(self):
        milestones = [
            {"date": "2024-Q1", "title": "Architecture Setup", "desc": "Initial design and core primitives", "status": "completed"},
            {"date": "2024-Q2", "title": "Engine v2.0", "desc": "Vector rasterizer and retro themes", "status": "completed"},
            {"date": "2024-Q3", "title": "Widgets v4.0", "desc": "KPI, Progress, and Timeline rollout", "status": "current"},
            {"date": "2024-Q4", "title": "Live Studio Preview", "desc": "Web studio and ecosystem tools", "status": "pending"},
        ]
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_timeline(milestones=milestones, style=style, mode="dark")
            root = self._assert_valid_xml(svg)
            self.assertIn("WIDGETS V4.0", svg)
            self.assertIn("ARCHITECTURE SETUP", svg)

    # --------------------------------------------------------------------------
    # 6. COMPILER DIRECTIVES INTEGRATION
    # --------------------------------------------------------------------------
    def test_compiler_progress_directive(self):
        svg_path = os.path.join(self.temp_dir, "progress.svg").replace("\\", "/")
        template = f"""# Test Project
<!-- pixel-kit:progress value="82" label="BATTERY CAPACITY" sub="VOLTAGE STABLE" out="{svg_path}" -->
"""
        compiler = MarkdownCompiler(assets_dir=self.temp_dir)
        compiled = compiler.compile_text(template)
        self.assertIn("progress.svg", compiled)
        self.assertTrue(os.path.exists(svg_path))
        with open(svg_path, "r", encoding="utf-8") as f:
            self._assert_valid_xml(f.read())

    def test_compiler_techstack_directive(self):
        svg_path = os.path.join(self.temp_dir, "tech.svg").replace("\\", "/")
        template = f"""# Test Project
<!-- pixel-kit:techstack items="python,cpp,docker,git" columns="4" out="{svg_path}" -->
"""
        compiler = MarkdownCompiler(assets_dir=self.temp_dir)
        compiled = compiler.compile_text(template)
        self.assertIn("tech.svg", compiled)
        self.assertTrue(os.path.exists(svg_path))
        with open(svg_path, "r", encoding="utf-8") as f:
            self._assert_valid_xml(f.read())

    def test_compiler_metrics_container_directive(self):
        svg_path = os.path.join(self.temp_dir, "metrics.svg").replace("\\", "/")
        template = f"""# Metrics Section
<!-- pixel-kit:metrics style="tactical" out="{svg_path}" -->
<!-- card label="OPERATIONS" value="98.4%" delta="+1.2%" trend="up" status="HEALTHY" -->
<!-- card label="MEM USAGE" value="4.2 GB" delta="-300MB" trend="down" -->
<!-- /pixel-kit:metrics -->
"""
        compiler = MarkdownCompiler(assets_dir=self.temp_dir)
        compiled = compiler.compile_text(template)
        self.assertIn("metrics.svg", compiled)
        self.assertTrue(os.path.exists(svg_path))
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
            self._assert_valid_xml(content)
            self.assertIn("OPERATIONS", content)
            self.assertIn("MEM USAGE", content)

    def test_compiler_timeline_container_directive(self):
        svg_path = os.path.join(self.temp_dir, "timeline.svg").replace("\\", "/")
        template = f"""# Roadmap Section
<!-- pixel-kit:timeline style="minimal" out="{svg_path}" -->
<!-- milestone date="V1.0" title="Genesis" desc="Initial CLI release" status="completed" -->
<!-- milestone date="V2.0" title="V2 Rollout" desc="Extended directives" status="current" -->
<!-- /pixel-kit:timeline -->
"""
        compiler = MarkdownCompiler(assets_dir=self.temp_dir)
        compiled = compiler.compile_text(template)
        self.assertIn("timeline.svg", compiled)
        self.assertTrue(os.path.exists(svg_path))
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
            self._assert_valid_xml(content)
            self.assertIn("GENESIS", content)
            self.assertIn("V2 ROLLOUT", content)

    # --------------------------------------------------------------------------
    # 7. MCP SERVER TOOL_RENDER_BLOCK INTEGRATION
    # --------------------------------------------------------------------------
    def test_mcp_render_block_new_types(self):
        out_metrics = os.path.join(self.temp_dir, "mcp_metrics.svg")
        res1 = tool_render_block({
            "block_type": "metrics",
            "output_path": out_metrics,
            "params": {"label": "PING", "value": "14ms", "delta": "-2ms", "trend": "down"},
            "style": "cyberpunk"
        })
        self.assertTrue(res1["success"])
        self.assertTrue(os.path.exists(out_metrics))

        out_progress = os.path.join(self.temp_dir, "mcp_progress.svg")
        res2 = tool_render_block({
            "block_type": "progress",
            "output_path": out_progress,
            "params": {"value": 88, "label": "SYNC"},
            "style": "tactical"
        })
        self.assertTrue(res2["success"])
        self.assertTrue(os.path.exists(out_progress))

        out_tech = os.path.join(self.temp_dir, "mcp_tech.svg")
        res3 = tool_render_block({
            "block_type": "techstack",
            "output_path": out_tech,
            "params": {"items": "python,rust,docker", "columns": 3},
            "style": "minimal"
        })
        self.assertTrue(res3["success"])
        self.assertTrue(os.path.exists(out_tech))

        out_time = os.path.join(self.temp_dir, "mcp_time.svg")
        res4 = tool_render_block({
            "block_type": "timeline",
            "output_path": out_time,
            "params": {
                "milestones": [
                    {"date": "PHASE 1", "title": "Launch", "status": "completed"},
                    {"date": "PHASE 2", "title": "Scale", "status": "pending"},
                ]
            },
            "style": "cyberpunk"
        })
        self.assertTrue(res4["success"])
        self.assertTrue(os.path.exists(out_time))


if __name__ == "__main__":
    unittest.main()
