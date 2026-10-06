"""
Unit tests for GitHub Auto-Fetching, Metrics directive, and Sync functionality.
"""

import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from generator.compiler import MarkdownCompiler
from generator.studio.handlers.render_handler import handle_github_fetch


class TestAutoFetchAndSync(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="pixel_kit_sync_test_")
        self.compiler = MarkdownCompiler(assets_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_compile_metrics_directive_manual(self):
        md = '<!-- pixel-kit:metrics style="cyberpunk" items="STARS: 450|FORKS: 42" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn('<img src="', compiled)
        self.assertIn('metrics-cyberpunk', compiled)

    @patch("generator.compiler.fetch_repo_data")
    def test_compile_metrics_directive_auto_fetch(self, mock_fetch_repo):
        mock_fetch_repo.return_value = ({
            "repo": "Kazinagg/pixel-readme-kit",
            "stars": 880,
            "forks": 95,
            "watchers": 40,
            "license": "MIT"
        }, None)

        md = '<!-- pixel-kit:metrics style="tactical" repo="Kazinagg/pixel-readme-kit" auto_fetch="true" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn('<img src="', compiled)
        self.assertIn('metrics-tactical', compiled)
        mock_fetch_repo.assert_called_with("Kazinagg/pixel-readme-kit")

    @patch("generator.compiler.fetch_star_trajectory")
    def test_compile_starchart_auto_fetch(self, mock_fetch_traj):
        mock_fetch_traj.return_value = ({
            "repo": "Kazinagg/pixel-readme-kit",
            "points": [10.0, 50.0, 150.0, 300.0, 600.0, 1200.0],
            "current": "1,200",
            "delta": "+140% past 6m"
        }, None)

        md = '<!-- pixel-kit:starchart style="cyberpunk" repo="Kazinagg/pixel-readme-kit" auto_fetch="true" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn('<img src="', compiled)
        self.assertIn('starchart-cyberpunk', compiled)
        mock_fetch_traj.assert_called_with("Kazinagg/pixel-readme-kit")

    @patch("generator.compiler.fetch_user_data")
    def test_compile_profile_auto_fetch(self, mock_fetch_user):
        mock_fetch_user.return_value = ({
            "username": "Kazinagg",
            "name": "Alex",
            "bio": "Systems Engineer & Architect",
            "location": "Cyberspace // UTC+3",
            "public_repos": 42
        }, None)

        md = '<!-- pixel-kit:profile style="cyberpunk" username="Kazinagg" auto_fetch="true" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn('<img src="', compiled)
        self.assertIn('profile-cyberpunk', compiled)
        mock_fetch_user.assert_called_with("Kazinagg")

    @patch("generator.github_api.fetch_repo_data")
    @patch("generator.github_api.fetch_star_trajectory")
    def test_handle_github_fetch_endpoint(self, mock_traj, mock_repo):
        mock_repo.return_value = ({"stars": 100, "forks": 10}, None)
        mock_traj.return_value = ({"current": "100", "points": [10, 50, 100]}, None)

        mock_handler = MagicMock()
        mock_handler.wfile = MagicMock()

        query = {"repo": ["owner/test-repo"]}
        handle_github_fetch(mock_handler, query)

        mock_handler.send_response.assert_called_with(200)
        # Check written json
        written_bytes = mock_handler.wfile.write.call_args[0][0]
        data = json.loads(written_bytes.decode("utf-8"))
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["repo"]["stars"], 100)
        self.assertEqual(data["trajectory"]["current"], "100")


if __name__ == "__main__":
    unittest.main()
