"""
Unit tests for Pixel Readme Kit v4.0 Sprint 1:
- BuildCache & Incremental Caching (generator/cache.py)
- Garbage Collection & Dry Run (generator/compiler.py)
- Project Scaffolder (generator/scaffolder.py)
- Native MCP Server Tools (generator/mcp_server.py)
"""

import os
import shutil
import tempfile
import unittest

from generator.cache import BuildCache
from generator.compiler import MarkdownCompiler
from generator.scaffolder import scaffold_readme, get_available_templates
from generator.mcp_server import (
    tool_compile_readme,
    tool_render_block,
    tool_validate_template,
    tool_scaffold_project,
    tool_inspect_safe_zones
)

class TestSprint1(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="pixel_kit_sprint1_")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # --------------------------------------------------------------------------
    # 1. BUILD CACHE
    # --------------------------------------------------------------------------
    def test_build_cache_lifecycle(self):
        cache_file = os.path.join(self.temp_dir, ".test-cache.json")
        cache = BuildCache(cache_file=cache_file)

        dummy_file = os.path.join(self.temp_dir, "test.svg")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("<svg></svg>")

        content_hash = cache.compute_hash({"key": "val"})

        # Initial check should be invalid (not yet recorded)
        self.assertFalse(cache.is_valid(dummy_file, content_hash))

        # Record and save
        cache.record(dummy_file, content_hash)
        cache.save()

        # Should now be valid
        self.assertTrue(cache.is_valid(dummy_file, content_hash))

        # Reload cache from disk
        reloaded = BuildCache(cache_file=cache_file)
        self.assertTrue(reloaded.is_valid(dummy_file, content_hash))

        # Different hash should be invalid
        diff_hash = cache.compute_hash({"key": "different"})
        self.assertFalse(reloaded.is_valid(dummy_file, diff_hash))

    # --------------------------------------------------------------------------
    # 2. INCREMENTAL COMPILATION & GARBAGE COLLECTION
    # --------------------------------------------------------------------------
    def test_compiler_incremental_cache_and_gc(self):
        assets_dir = os.path.join(self.temp_dir, "assets")
        cache_file = os.path.join(assets_dir, ".pixel-cache.json")
        compiler = MarkdownCompiler(assets_dir=assets_dir, cache_file=cache_file)

        tpl_file = os.path.join(self.temp_dir, "test.template.md")
        out_file = os.path.join(self.temp_dir, "test.md")

        chip1_file = os.path.join(assets_dir, "chip1.svg").replace("\\", "/")
        orphan_file = os.path.join(assets_dir, "chip_orphan.svg").replace("\\", "/")

        # Initial template with 2 directives
        with open(tpl_file, "w", encoding="utf-8") as f:
            f.write(f"""
<!-- pixel-kit:chip style="cyberpunk" text="ACTIVE_CHIP" out="{chip1_file}" -->
<!-- pixel-kit:chip style="tactical" text="ORPHAN_CHIP" out="{orphan_file}" -->
""")

        # First compile: 2 generated, 0 cached
        compiler.compile_file(tpl_file, out_file)
        self.assertEqual(compiler.stats["generated"], 2)
        self.assertEqual(compiler.stats["cached"], 0)
        self.assertTrue(os.path.exists(os.path.join(assets_dir, "chip1.svg")))
        self.assertTrue(os.path.exists(os.path.join(assets_dir, "chip_orphan.svg")))

        # Second compile: 0 generated, 2 cached
        compiler.compile_file(tpl_file, out_file)
        self.assertEqual(compiler.stats["generated"], 0)
        self.assertEqual(compiler.stats["cached"], 2)

        # Now remove ORPHAN_CHIP from template
        with open(tpl_file, "w", encoding="utf-8") as f:
            f.write(f"""
<!-- pixel-kit:chip style="cyberpunk" text="ACTIVE_CHIP" out="{chip1_file}" -->
""")

        # Dry run clean assets
        compiler.compile_file(tpl_file, out_file, clean_assets=False, dry_run_clean=True)
        orphan_names = [os.path.basename(p) for p in compiler.orphans]
        self.assertIn("chip_orphan.svg", orphan_names)
        # File should still exist on disk after dry run
        self.assertTrue(os.path.exists(os.path.join(assets_dir, "chip_orphan.svg")))

        # Actual clean assets
        compiler.compile_file(tpl_file, out_file, clean_assets=True, dry_run_clean=False)
        self.assertFalse(os.path.exists(os.path.join(assets_dir, "chip_orphan.svg")))
        self.assertTrue(os.path.exists(os.path.join(assets_dir, "chip1.svg")))

    # --------------------------------------------------------------------------
    # 3. SCAFFOLDER
    # --------------------------------------------------------------------------
    def test_scaffolder_all_templates(self):
        for ptype in get_available_templates():
            out_path = os.path.join(self.temp_dir, f"{ptype}.template.md")
            res_path = scaffold_readme(
                project_type=ptype,
                title=f"TEST {ptype.upper()}",
                output_path=out_path
            )
            self.assertTrue(os.path.exists(res_path))
            with open(res_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(f"TEST {ptype.upper()}", content)
            self.assertIn("pixel-kit:", content)

    # --------------------------------------------------------------------------
    # 4. MCP TOOLS
    # --------------------------------------------------------------------------
    def test_mcp_tools(self):
        # 1. inspect_safe_zones
        safe_res = tool_inspect_safe_zones("header", "SHORT")
        self.assertEqual(safe_res["status"], "optimal")
        self.assertEqual(safe_res["pixel_scale"], 6)

        long_res = tool_inspect_safe_zones("header", "A" * 35)
        self.assertEqual(long_res["status"], "danger")

        # 2. validate_template
        valid_res = tool_validate_template(content='<!-- pixel-kit:header title="SHORT" -->')
        self.assertEqual(valid_res["status"], "success")
        self.assertEqual(valid_res["directives_found"], 1)

        # 3. render_block
        out_svg = os.path.join(self.temp_dir, "rendered.svg")
        render_res = tool_render_block("chip", title="TEST_CHIP", output_path=out_svg)
        self.assertEqual(render_res["status"], "success")
        self.assertTrue(os.path.exists(out_svg))

        # 4. scaffold_project tool
        scaffold_out = os.path.join(self.temp_dir, "scaffolded.template.md")
        scaff_res = tool_scaffold_project("library", title="AWESOME LIB", output_path=scaffold_out)
        self.assertEqual(scaff_res["status"], "success")
        self.assertTrue(os.path.exists(scaffold_out))

        # 5. compile_readme tool
        compile_out = os.path.join(self.temp_dir, "scaffolded.md")
        assets_out = os.path.join(self.temp_dir, "assets_mcp")
        comp_res = tool_compile_readme(
            template_path=scaffold_out,
            output_path=compile_out,
            assets_dir=assets_out
        )
        self.assertEqual(comp_res["status"], "success")
        self.assertTrue(os.path.exists(compile_out))


if __name__ == "__main__":
    unittest.main()
