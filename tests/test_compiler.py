"""
Unit tests for Compiler (generator/compiler.py)
Validates directive parsing, table wrapping, live stats, and Markdown transformation.
"""

import os
import shutil
import tempfile
import unittest
from generator.compiler import (
    parse_directive_attrs,
    fetch_github_stat,
    MarkdownCompiler,
)


class TestCompiler(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="pixel_kit_test_")
        self.compiler = MarkdownCompiler(assets_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_directive_attrs(self):
        s = 'style="cyberpunk" primary="#00C8D7" title=\'MY SYSTEM\' mode=auto out="assets/test.svg"'
        attrs = parse_directive_attrs(s)
        self.assertEqual(attrs["style"], "cyberpunk")
        self.assertEqual(attrs["primary"], "#00C8D7")
        self.assertEqual(attrs["title"], "MY SYSTEM")
        self.assertEqual(attrs["mode"], "auto")
        self.assertEqual(attrs["out"], "assets/test.svg")

    def test_fetch_github_stat_fallback(self):
        # Invalid repo returns fallback without throwing
        stat, link = fetch_github_stat("non_existent_owner/non_existent_repo_xyz_123", "stars")
        self.assertTrue(stat.startswith("★"))
        self.assertIn("github.com", link)

    def test_compile_header_directive(self):
        md = '<!-- pixel-kit:header style="cyberpunk" title="COMPILER TEST" subtitle="SUBTITLE" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn('<img src="', compiled)
        self.assertIn('alt="COMPILER TEST"', compiled)
        self.assertIn('width="100%"', compiled)

    def test_compile_window_directive(self):
        md = """<!-- pixel-kit:window style="cyberpunk" title="TEST WINDOW" -->
### Live Content
- Item 1
- Item 2
<!-- /pixel-kit:window -->"""
        compiled = self.compiler.compile_text(md)
        self.assertIn('<table width="100%">', compiled)
        self.assertIn('<td width="2000">', compiled)
        self.assertIn('### Live Content', compiled)

    def test_compile_terminal_directive(self):
        md = """<!-- pixel-kit:terminal style="cyberpunk" title="CONSOLE" state="closed" -->
```bash
echo hello
```
<!-- /pixel-kit:terminal -->"""
        compiled = self.compiler.compile_text(md)
        self.assertIn('<details >', compiled)
        self.assertIn('<summary><kbd>▶ CONSOLE</kbd>', compiled)
        self.assertNotIn('<img', compiled.split('<summary>')[1].split('</summary>')[0])

    def test_compile_quote_directive(self):
        md = """<!-- pixel-kit:quote style="tactical" title="NOTICE" subtitle="Info" -->
Line of quote text
Another line
<!-- /pixel-kit:quote -->"""
        compiled = self.compiler.compile_text(md)
        self.assertIn('> <img src="', compiled)
        self.assertIn('> Line of quote text', compiled)

    def test_compile_github_chip_directive(self):
        md = '<!-- pixel-kit:chip github="stars" repo="Kazinagg/pixel-readme-kit" style="cyberpunk" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn('<a href="https://github.com/Kazinagg/pixel-readme-kit/stargazers">', compiled)
        self.assertIn('<img src="', compiled)

    def test_compile_modes(self):
        # mode="gh" generates dark and light mode only tags
        md_gh = '<!-- pixel-kit:divider style="cyberpunk" mode="gh" -->'
        compiled_gh = self.compiler.compile_text(md_gh)
        self.assertIn('#gh-dark-mode-only', compiled_gh)
        self.assertIn('#gh-light-mode-only', compiled_gh)

        # mode="picture" generates HTML5 picture
        md_pic = '<!-- pixel-kit:divider style="cyberpunk" mode="picture" -->'
        compiled_pic = self.compiler.compile_text(md_pic)
        self.assertIn('<picture>', compiled_pic)
        self.assertIn('prefers-color-scheme: dark', compiled_pic)


if __name__ == "__main__":
    unittest.main()
