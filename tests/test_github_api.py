"""
Tests for GitHub API integration (generator/github_api.py)
"""

import json
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError

from generator.github_api import (
    _get_auth_token,
    fetch_repo_data,
    fetch_user_data,
    fetch_star_trajectory
)


class TestGitHubAPI(unittest.TestCase):

    def test_get_auth_token_precedence(self):
        # Explicit token takes highest priority
        self.assertEqual(_get_auth_token("my_token"), "my_token")

        # Env vars
        with patch.dict("os.environ", {"GITHUB_TOKEN": "env_token", "GH_TOKEN": "gh_token"}):
            self.assertEqual(_get_auth_token(None), "env_token")

        with patch.dict("os.environ", {"GH_TOKEN": "gh_token"}, clear=True):
            self.assertEqual(_get_auth_token(None), "gh_token")

        with patch.dict("os.environ", {}, clear=True):
            self.assertIsNone(_get_auth_token(None))

    def test_fetch_repo_data_invalid_format(self):
        data, err = fetch_repo_data("invalid_no_slash")
        self.assertIsNone(data)
        self.assertIn("Invalid repository format", err)

    @patch("generator.github_api._github_request")
    def test_fetch_repo_data_success(self, mock_request):
        mock_request.return_value = ({
            "full_name": "Kazinagg/pixel-readme-kit",
            "name": "pixel-readme-kit",
            "owner": {"login": "Kazinagg"},
            "description": "HUD infographics generator",
            "stargazers_count": 420,
            "forks_count": 35,
            "subscribers_count": 18,
            "open_issues_count": 3,
            "license": {"spdx_id": "MIT"},
            "language": "Python",
            "archived": False
        }, None)

        data, err = fetch_repo_data("Kazinagg/pixel-readme-kit")
        self.assertIsNone(err)
        self.assertIsNotNone(data)
        self.assertEqual(data["stars"], 420)
        self.assertEqual(data["forks"], 35)
        self.assertEqual(data["license"], "MIT")

    @patch("generator.github_api._github_request")
    def test_fetch_repo_data_http_error(self, mock_request):
        mock_request.return_value = (None, "Resource not found (404): https://api.github.com/repos/unknown/repo")
        data, err = fetch_repo_data("unknown/repo")
        self.assertIsNone(data)
        self.assertIn("404", err)

    @patch("generator.github_api._github_request")
    def test_fetch_user_data_success(self, mock_request):
        mock_request.return_value = ({
            "login": "Kazinagg",
            "name": "Alex",
            "bio": "Systems architect & hacker",
            "company": "CyberCorp",
            "location": "Cyberspace // UTC+3",
            "public_repos": 45,
            "followers": 150,
            "following": 12,
            "avatar_url": "https://avatars.githubusercontent.com/u/123",
            "blog": "https://example.com"
        }, None)

        data, err = fetch_user_data("Kazinagg")
        self.assertIsNone(err)
        self.assertIsNotNone(data)
        self.assertEqual(data["username"], "Kazinagg")
        self.assertEqual(data["name"], "Alex")
        self.assertEqual(data["public_repos"], 45)

    def test_fetch_user_data_empty(self):
        data, err = fetch_user_data("   ")
        self.assertIsNone(data)
        self.assertIn("Empty username", err)

    @patch("generator.github_api.fetch_repo_data")
    def test_fetch_star_trajectory_success(self, mock_fetch_repo):
        mock_fetch_repo.return_value = ({
            "repo": "Kazinagg/pixel-readme-kit",
            "stars": 1000,
            "forks": 50,
            "watchers": 25
        }, None)

        # Mock the second request for stargazers
        with patch("generator.github_api._github_request") as mock_req:
            mock_req.return_value = (None, "Rate limited")
            data, err = fetch_star_trajectory("Kazinagg/pixel-readme-kit")

            self.assertIsNone(err)
            self.assertEqual(data["stars"], 1000)
            self.assertEqual(data["current"], "1,000")
            self.assertEqual(len(data["points"]), 6)
            self.assertEqual(data["points"][-1], 1000.0)
            self.assertIn("+", data["delta"])

    @patch("generator.github_api.fetch_repo_data")
    def test_fetch_star_trajectory_fallback_on_network_failure(self, mock_fetch_repo):
        mock_fetch_repo.return_value = (None, "Network failure")

        data, err = fetch_star_trajectory("offline/repo")
        self.assertIsNotNone(err)
        self.assertIn("Network failure", err)
        # Still returns safe fallback points so render doesn't crash
        self.assertEqual(len(data["points"]), 6)
        self.assertEqual(data["current"], "1,650")


if __name__ == "__main__":
    unittest.main()
