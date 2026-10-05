"""
Pixel Readme Kit v4.1 - Live Preview & HUD Studio Server.
Zero-dependency HTTP server with Server-Sent Events (SSE) live reload,
real-time SVG rendering API, and interactive HUD Studio Web UI.
"""

import os
import sys
import re
import json
import time
import urllib.parse
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import subprocess

# Add parent directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generator.engine import (
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
    generate_social,
    THEME_PALETTES,
    validate_svg
)
from generator.icons import list_available_icons
from generator.compiler import MarkdownCompiler, parse_directive_attrs, fetch_github_stat

def extract_template_blocks(template_content: str):
    """
    Parses all pixel-kit directives from markdown text with their exact span indices,
    attributes, and inner body contents.
    """
    block_pattern = re.compile(
        r'(<!--\s*pixel-kit:(window|terminal|quote|metrics|timeline)\b(.*?)-->([\s\S]*?)<!--\s*/pixel-kit:\2\s*-->)',
        re.IGNORECASE
    )
    single_pattern = re.compile(
        r'(<!--\s*pixel-kit:(header|footer|callout|frame|chip|divider|splitter|progress|techstack|social)\b(.*?)-->)',
        re.IGNORECASE
    )

    blocks = []
    for m in block_pattern.finditer(template_content):
        btype = m.group(2).lower()
        attrs = parse_directive_attrs(m.group(3))
        blocks.append({
            "id": 0,
            "type": btype,
            "attrs": attrs,
            "body": m.group(4).strip(),
            "is_container": True,
            "start": m.start(),
            "end": m.end(),
            "raw": m.group(1)
        })
    for m in single_pattern.finditer(template_content):
        btype = m.group(2).lower()
        attrs = parse_directive_attrs(m.group(3))
        blocks.append({
            "id": 0,
            "type": btype,
            "attrs": attrs,
            "body": "",
            "is_container": False,
            "start": m.start(),
            "end": m.end(),
            "raw": m.group(1)
        })

    blocks.sort(key=lambda x: x["start"])
    for i, b in enumerate(blocks):
        b["id"] = i
    return blocks

# ==============================================================================
# EMBEDDED HUD STUDIO HTML/CSS/JS INTERFACE
# ==============================================================================

STUDIO_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIXEL README KIT // HUD STUDIO v4.2</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Orbitron:wght@600;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css" crossorigin="anonymous">
  <style>
    :root {
      /* Studio Chrome Theme Variables (Completely Isolated from SVG tokens) */
      --studio-bg: #07090e;
      --studio-panel: rgba(13, 19, 33, 0.96);
      --studio-panel-border: rgba(0, 200, 215, 0.32);
      --studio-cyan: #00c8d7;
      --studio-purple: #a855f7;
      --studio-amber: #f59e0b;
      --studio-green: #00d26a;
      --studio-danger: #ef4444;
      --studio-text: #f1f5f9;
      --studio-text-dim: #94a3b8;
      --studio-font-mono: 'JetBrains Mono', monospace;
      --studio-font-hud: 'Orbitron', monospace;

      /* GitHub Container Emulation Variables */
      --gh-font: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
      --gh-bg: #0d1117;
      --gh-card-bg: #161b22;
      --gh-border: #30363d;
      --gh-text: #e6edf3;
      --gh-text-dim: #8b949e;
    }

    .light-theme {
      --gh-bg: #ffffff;
      --gh-card-bg: #ffffff;
      --gh-border: #d0d7de;
      --gh-text: #1f2328;
      --gh-text-dim: #656d76;
    }

    * { 
      box-sizing: border-box; 
      margin: 0; 
      padding: 0; 
      scrollbar-width: thin;
      scrollbar-color: rgba(0, 200, 215, 0.35) rgba(7, 9, 14, 0.85);
    }

    /* Custom Retro-Cyberpunk HUD Scrollbars */
    ::-webkit-scrollbar {
      width: 7px;
      height: 7px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(7, 9, 14, 0.85);
      border-left: 1px solid rgba(0, 200, 215, 0.12);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(0, 200, 215, 0.3);
      border-radius: 4px;
      border: 1px solid rgba(0, 200, 215, 0.45);
      box-shadow: inset 0 0 6px rgba(0, 200, 215, 0.2);
      transition: all 0.2s ease;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--studio-cyan);
      border-color: #ffffff;
      box-shadow: 0 0 10px rgba(0, 200, 215, 0.7);
    }
    ::-webkit-scrollbar-corner {
      background: rgba(7, 9, 14, 0.95);
    }

    /* Light Theme Custom Scrollbar for Preview Pane */
    .preview-pane.light-theme {
      scrollbar-color: rgba(110, 118, 129, 0.4) #f6f8fa;
    }
    .preview-pane.light-theme::-webkit-scrollbar-track {
      background: #f6f8fa;
      border-left: 1px solid #d0d7de;
    }
    .preview-pane.light-theme::-webkit-scrollbar-thumb {
      background: rgba(110, 118, 129, 0.35);
      border: 1px solid rgba(110, 118, 129, 0.5);
      box-shadow: none;
    }
    .preview-pane.light-theme::-webkit-scrollbar-thumb:hover {
      background: rgba(110, 118, 129, 0.7);
    }

    body {
      background: var(--studio-bg);
      color: var(--studio-text);
      font-family: var(--studio-font-mono);
      font-size: 13px;
      line-height: 1.5;
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(0, 200, 215, 0.08) 0%, transparent 60%),
        linear-gradient(rgba(0, 200, 215, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 200, 215, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 32px 32px, 32px 32px;
    }

    /* Top HUD Navbar */
    header.hud-nav {
      height: 52px;
      background: rgba(10, 14, 23, 0.98);
      border-bottom: 1px solid var(--studio-panel-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 100;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .brand {
      font-family: var(--studio-font-hud);
      font-size: 14px;
      font-weight: 900;
      color: var(--studio-cyan);
      letter-spacing: 2px;
      display: flex;
      align-items: center;
      gap: 12px;
      text-shadow: 0 0 10px rgba(0, 200, 215, 0.5);
    }
    .brand-badge {
      font-family: var(--studio-font-mono);
      font-size: 10px;
      background: rgba(0, 200, 215, 0.15);
      border: 1px solid var(--studio-cyan);
      padding: 2px 6px;
      border-radius: 3px;
      color: #fff;
    }
    .nav-status {
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 11.5px;
    }
    .status-indicator {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--studio-text-dim);
    }
    .pulse-dot {
      width: 7px;
      height: 7px;
      background: var(--studio-green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--studio-green);
      animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
    .nav-btn {
      background: rgba(0, 200, 215, 0.1);
      border: 1px solid var(--studio-panel-border);
      color: var(--studio-text);
      font-family: var(--studio-font-mono);
      font-size: 11px;
      padding: 6px 12px;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .nav-btn:hover, .nav-btn.active-btn {
      background: var(--studio-cyan);
      color: #000;
      border-color: var(--studio-cyan);
      box-shadow: 0 0 12px rgba(0, 200, 215, 0.5);
    }
    .nav-btn.btn-amber:hover, .nav-btn.btn-amber.active-btn {
      background: var(--studio-amber);
      color: #000;
      border-color: var(--studio-amber);
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.6);
    }
    .nav-btn.btn-green {
      background: rgba(0, 210, 106, 0.12);
      border-color: rgba(0, 210, 106, 0.4);
      color: #00d26a;
    }
    .nav-btn.btn-green:hover, .nav-btn.btn-green.active-btn {
      background: #00d26a;
      color: #000;
      border-color: #00d26a;
      box-shadow: 0 0 12px rgba(0, 210, 106, 0.6);
    }
    .theme-switch-group {
      display: flex;
      border: 1px solid var(--studio-panel-border);
      border-radius: 4px;
      overflow: hidden;
    }
    .theme-tab {
      background: transparent;
      border: none;
      color: var(--studio-text-dim);
      font-family: var(--studio-font-mono);
      font-size: 11px;
      padding: 5px 10px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .theme-tab:hover {
      color: #fff;
    }
    .theme-tab.active {
      background: var(--studio-cyan);
      color: #000;
      font-weight: 700;
    }

    .mode-switch-group {
      display: flex;
      border: 1px solid var(--studio-panel-border);
      border-radius: 4px;
      overflow: hidden;
    }
    .mode-tab {
      background: transparent;
      border: none;
      color: var(--studio-text-dim);
      font-family: var(--studio-font-mono);
      font-size: 11px;
      padding: 5px 10px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .mode-tab:hover {
      color: #fff;
    }
    .mode-tab.active {
      background: var(--studio-purple);
      color: #fff;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
    }

    /* Main Split Layout */
    .studio-container {
      display: flex;
      flex: 1;
      height: calc(100vh - 52px);
      position: relative;
      overflow: hidden;
    }

    /* LEFT: GITHUB-STYLE PREVIEW SCROLL AREA */
    .preview-pane {
      flex: 1;
      overflow-y: auto;
      background: var(--gh-bg);
      padding: 30px 40px 100px;
      transition: background 0.2s;
      position: relative;
    }
    .preview-pane.light-theme {
      background: #ffffff;
    }
    .gh-readme-wrapper {
      max-width: 980px;
      margin: 0 auto;
      background: var(--gh-card-bg);
      border: 1px solid var(--gh-border);
      border-radius: 6px;
      padding: 0;
      box-shadow: 0 8px 30px rgba(0,0,0,0.4);
      position: relative;
      overflow: hidden;
    }
    .gh-card-header {
      padding: 12px 16px;
      background: rgba(255, 255, 255, 0.02);
      border-bottom: 1px solid var(--gh-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--gh-font);
      font-size: 13px;
      color: var(--gh-text);
      font-weight: 600;
    }
    .gh-card-title {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .gh-card-title svg {
      fill: var(--gh-text-dim);
    }
    .gh-badge {
      font-size: 11px;
      background: rgba(110, 118, 129, 0.2);
      color: var(--gh-text-dim);
      padding: 2px 7px;
      border-radius: 12px;
      font-weight: normal;
    }
    .gh-card-meta {
      font-size: 11.5px;
      color: var(--gh-text-dim);
      font-family: var(--studio-font-mono);
    }

    /* GitHub Markdown Container */
    article.markdown-body {
      padding: 32px 32px 48px;
      background: transparent !important;
      color: var(--gh-text);
      font-family: var(--gh-font);
      font-size: 14px;
      line-height: 1.6;
    }
    article.markdown-body p,
    article.markdown-body blockquote,
    article.markdown-body ul,
    article.markdown-body ol,
    article.markdown-body dl,
    article.markdown-body table,
    article.markdown-body pre,
    article.markdown-body details {
      margin-top: 0;
      margin-bottom: 16px;
    }
    article.markdown-body h1,
    article.markdown-body h2,
    article.markdown-body h3,
    article.markdown-body h4,
    article.markdown-body h5,
    article.markdown-body h6 {
      margin-top: 24px;
      margin-bottom: 16px;
      font-weight: 600;
      line-height: 1.25;
    }
    article.markdown-body h1 {
      font-size: 2em;
      padding-bottom: 0.3em;
      border-bottom: 1px solid var(--gh-border);
    }
    article.markdown-body h2 {
      font-size: 1.5em;
      padding-bottom: 0.3em;
      border-bottom: 1px solid var(--gh-border);
    }
    article.markdown-body h3 {
      font-size: 1.25em;
    }
    article.markdown-body h4 {
      font-size: 1em;
    }
    article.markdown-body h5 {
      font-size: 0.875em;
    }
    article.markdown-body h6 {
      font-size: 0.85em;
      color: var(--gh-text-dim);
    }
    article.markdown-body ul,
    article.markdown-body ol {
      padding-left: 2em;
    }
    article.markdown-body ul ul,
    article.markdown-body ul ol,
    article.markdown-body ol ol,
    article.markdown-body ol ul {
      margin-top: 0;
      margin-bottom: 0;
    }
    article.markdown-body li {
      word-wrap: break-all;
    }
    article.markdown-body li > p {
      margin-top: 16px;
    }
    article.markdown-body li + li {
      margin-top: 0.25em;
    }
    article.markdown-body img {
      max-width: 100%;
      box-sizing: content-box;
      vertical-align: middle;
    }
    article.markdown-body > *:first-child {
      margin-top: 0 !important;
    }
    article.markdown-body > *:last-child {
      margin-bottom: 0 !important;
    }
    article.markdown-body a {
      color: #58a6ff;
      text-decoration: none;
    }
    article.markdown-body a:hover {
      text-decoration: underline;
    }
    article.markdown-body hr {
      height: 1px;
      background-color: var(--gh-border);
      border: 0;
      margin: 24px 0;
    }
    article.markdown-body pre {
      background-color: rgba(110, 118, 129, 0.15) !important;
      border: 1px solid var(--gh-border);
      border-radius: 6px;
      padding: 16px;
      overflow: auto;
      font-family: var(--studio-font-mono);
      font-size: 12.5px;
    }
    article.markdown-body table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
      border-spacing: 0;
    }
    article.markdown-body table th,
    article.markdown-body table td {
      padding: 6px 13px;
      border: 1px solid var(--gh-border);
    }
    article.markdown-body table tr:nth-child(2n) {
      background-color: rgba(110, 118, 129, 0.05);
    }
    article.markdown-body blockquote {
      border-left: 0.25em solid #30363d;
      color: var(--gh-text-dim);
      padding: 0 1em;
      margin: 16px 0;
    }

    /* =========================================================================
       AUTHENTIC GITHUB LIGHT THEME STYLES (100% Matching Real GitHub)
       ========================================================================= */
    .preview-pane.light-theme {
      background: #ffffff !important;
    }
    .light-theme .gh-readme-wrapper {
      background: #ffffff !important;
      border: 1px solid #d0d7de !important;
      box-shadow: 0 1px 3px rgba(31, 35, 40, 0.12), 0 8px 24px rgba(66, 74, 83, 0.08) !important;
    }
    .light-theme .gh-card-header {
      background-color: #f6f8fa !important;
      border-bottom: 1px solid #d0d7de !important;
      color: #1f2328 !important;
    }
    .light-theme .gh-card-title {
      color: #1f2328 !important;
    }
    .light-theme .gh-card-title svg {
      fill: #656d76 !important;
    }
    .light-theme .gh-badge {
      background: rgba(175, 184, 193, 0.2) !important;
      color: #656d76 !important;
    }
    .light-theme .gh-card-meta {
      color: #656d76 !important;
    }

    /* Markdown Body Overrides for Light Theme */
    .light-theme article.markdown-body {
      color-scheme: light !important;
      color: #1f2328 !important;
      background: transparent !important;
      --fgColor-default: #1f2328 !important;
      --fgColor-muted: #656d76 !important;
      --fgColor-accent: #0969da !important;
      --fgColor-success: #1a7f37 !important;
      --fgColor-attention: #9a6700 !important;
      --fgColor-danger: #cf222e !important;
      --bgColor-default: #ffffff !important;
      --bgColor-muted: #f6f8fa !important;
      --borderColor-default: #d0d7de !important;
      --borderColor-muted: #d0d7de !important;
      --color-fg-default: #1f2328 !important;
      --color-fg-muted: #656d76 !important;
      --color-canvas-default: #ffffff !important;
      --color-canvas-subtle: #f6f8fa !important;
      --color-border-default: #d0d7de !important;
      --color-border-muted: #d0d7de !important;
      --color-accent-fg: #0969da !important;
    }
    .light-theme article.markdown-body h1,
    .light-theme article.markdown-body h2,
    .light-theme article.markdown-body h3,
    .light-theme article.markdown-body h4,
    .light-theme article.markdown-body h5,
    .light-theme article.markdown-body h6 {
      color: #1f2328 !important;
      border-bottom-color: #d0d7de !important;
    }
    .light-theme article.markdown-body h6 {
      color: #656d76 !important;
    }
    .light-theme article.markdown-body p,
    .light-theme article.markdown-body li,
    .light-theme article.markdown-body span,
    .light-theme article.markdown-body strong {
      color: #1f2328 !important;
    }
    .light-theme article.markdown-body a {
      color: #0969da !important;
    }
    .light-theme article.markdown-body a:hover {
      color: #0969da !important;
      text-decoration: underline !important;
    }
    .light-theme article.markdown-body hr {
      background-color: #d0d7de !important;
    }
    .light-theme article.markdown-body pre {
      background-color: #f6f8fa !important;
      border: 1px solid #d0d7de !important;
      color: #1f2328 !important;
    }
    .light-theme article.markdown-body code {
      background-color: rgba(175, 184, 193, 0.2) !important;
      color: #1f2328 !important;
    }
    .light-theme article.markdown-body pre code {
      background-color: transparent !important;
      color: #1f2328 !important;
    }
    .light-theme article.markdown-body blockquote {
      border-left: 0.25em solid #d0d7de !important;
      color: #656d76 !important;
    }
    .light-theme article.markdown-body table th,
    .light-theme article.markdown-body table td {
      border: 1px solid #d0d7de !important;
      color: #1f2328 !important;
    }
    .light-theme article.markdown-body table th {
      background-color: #f6f8fa !important;
      color: #1f2328 !important;
      font-weight: 600 !important;
    }
    .light-theme article.markdown-body table tr:nth-child(2n) {
      background-color: #f6f8fa !important;
    }
    .light-theme .markdown-alert {
      border-left: 0.25em solid #d0d7de !important;
      color: #1f2328 !important;
    }
    .light-theme .markdown-alert-note {
      border-left-color: #0969da !important;
      background: rgba(9, 105, 218, 0.08) !important;
    }
    .light-theme .markdown-alert-note .markdown-alert-title {
      color: #0969da !important;
    }
    .light-theme .markdown-alert-tip {
      border-left-color: #1a7f37 !important;
      background: rgba(26, 127, 55, 0.08) !important;
    }
    .light-theme .markdown-alert-tip .markdown-alert-title {
      color: #1a7f37 !important;
    }
    .light-theme .markdown-alert-important {
      border-left-color: #8250df !important;
      background: rgba(130, 80, 223, 0.08) !important;
    }
    .light-theme .markdown-alert-important .markdown-alert-title {
      color: #8250df !important;
    }
    .light-theme .markdown-alert-warning {
      border-left-color: #9a6700 !important;
      background: rgba(154, 103, 0, 0.08) !important;
    }
    .light-theme .markdown-alert-warning .markdown-alert-title {
      color: #9a6700 !important;
    }
    .light-theme .markdown-alert-caution {
      border-left-color: #cf222e !important;
      background: rgba(207, 34, 46, 0.08) !important;
    }
    .light-theme .markdown-alert-caution .markdown-alert-title {
      color: #cf222e !important;
    }

    /* GitHub Mode Image Fragments */
    [data-color-mode="light"] img[src*="#gh-dark-mode-only"],
    [data-color-mode="light"] picture source[media*="prefers-color-scheme: dark"] {
      display: none !important;
    }
    [data-color-mode="dark"] img[src*="#gh-light-mode-only"],
    [data-color-mode="dark"] picture source[media*="prefers-color-scheme: light"] {
      display: none !important;
    }

    /* GFM Alert Callouts */
    .markdown-alert {
      padding: 8px 16px;
      margin-bottom: 16px;
      color: inherit;
      border-left: 0.25em solid var(--gh-border);
      border-radius: 0 6px 6px 0;
    }
    .markdown-alert-title {
      display: flex;
      align-items: center;
      font-weight: 600;
      line-height: 1;
      gap: 6px;
      margin-bottom: 4px;
    }
    .markdown-alert-title svg {
      fill: currentColor;
    }
    .markdown-alert-note { border-left-color: #2f81f7; background: rgba(56, 139, 253, 0.1); }
    .markdown-alert-note .markdown-alert-title { color: #2f81f7; }
    .markdown-alert-tip { border-left-color: #238636; background: rgba(46, 160, 67, 0.1); }
    .markdown-alert-tip .markdown-alert-title { color: #238636; }
    .markdown-alert-important { border-left-color: #8957e5; background: rgba(163, 113, 247, 0.1); }
    .markdown-alert-important .markdown-alert-title { color: #a371f7; }
    .markdown-alert-warning { border-left-color: #9e6a03; background: rgba(187, 128, 9, 0.1); }
    .markdown-alert-warning .markdown-alert-title { color: #d29922; }
    .markdown-alert-caution { border-left-color: #da3633; background: rgba(248, 81, 73, 0.1); }
    .markdown-alert-caution .markdown-alert-title { color: #f85149; }

    /* View Mode: 100% Authentic GitHub View */
    .view-mode .pk-insert-divider {
      display: none !important;
    }
    .view-mode .pk-block-hud-bar {
      display: none !important;
    }
    .view-mode .pk-block-wrapper {
      border: none !important;
      outline: none !important;
      box-shadow: none !important;
      margin: 0 !important;
      padding: 0 !important;
      background: transparent !important;
      cursor: default !important;
      display: inline !important;
    }
    .view-mode .pk-block-wrapper:hover {
      outline: none !important;
      background: transparent !important;
    }
    .view-mode .pk-block-wrapper.selected-block {
      outline: none !important;
      background: transparent !important;
    }
    .view-mode .pk-block-wrapper[data-pk-type="chip"] {
      display: inline-block !important;
      margin-right: 4px !important;
      margin-bottom: 4px !important;
      vertical-align: middle !important;
    }
    .view-mode .pk-block-wrapper[data-pk-type="chip"] .pk-block-content,
    .view-mode .pk-block-wrapper[data-pk-type="chip"] .pk-block-content > p {
      display: inline !important;
      margin: 0 !important;
      padding: 0 !important;
    }

    /* Interactive Block Wrapper inside Preview */
    .pk-block-wrapper {
      position: relative;
      border: 1px solid transparent;
      border-radius: 4px;
      margin: 8px 0;
      transition: all 0.15s ease-out;
      cursor: pointer;
    }
    .pk-block-wrapper:hover {
      outline: 2px dashed rgba(0, 200, 215, 0.6) !important;
      background: rgba(0, 200, 215, 0.03);
    }
    .pk-block-wrapper.selected-block {
      outline: 2px solid var(--studio-cyan) !important;
      background: rgba(0, 200, 215, 0.06);
    }
    .pk-block-hud-bar {
      display: none;
      position: absolute;
      top: -14px;
      left: 12px;
      z-index: 40;
      background: rgba(10, 14, 23, 0.96);
      border: 1px solid var(--studio-cyan);
      padding: 3px 8px;
      border-radius: 4px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.8);
      font-family: var(--studio-font-mono);
      font-size: 10.5px;
    }
    .pk-block-wrapper:hover .pk-block-hud-bar,
    .pk-block-wrapper.selected-block .pk-block-hud-bar {
      display: flex;
    }
    .pk-hud-badge {
      color: var(--studio-cyan);
      font-weight: 700;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .pk-hud-dot {
      color: var(--studio-green);
      font-size: 8px;
    }
    .pk-hud-num {
      color: var(--studio-text-dim);
      font-weight: normal;
    }
    .pk-hud-actions {
      display: flex;
      gap: 4px;
      margin-left: 6px;
      border-left: 1px solid rgba(0, 200, 215, 0.3);
      padding-left: 6px;
    }
    .pk-hud-btn {
      background: rgba(0, 200, 215, 0.15);
      border: 1px solid var(--studio-cyan);
      color: #fff;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 3px;
      cursor: pointer;
      font-family: var(--studio-font-mono);
      transition: all 0.15s;
    }
    .pk-hud-btn:hover {
      background: var(--studio-cyan);
      color: #000;
    }
    .pk-hud-btn.del-btn {
      border-color: #ef4444;
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
    }
    .pk-hud-btn.del-btn:hover {
      background: #ef4444;
      color: #fff;
    }

    /* Insertion Divider between Blocks */
    .pk-insert-divider {
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      margin: 6px 0;
      opacity: 0.25;
      transition: opacity 0.2s, height 0.2s;
    }
    .pk-insert-divider:hover {
      opacity: 1;
      height: 36px;
    }
    .pk-insert-divider::before {
      content: "";
      position: absolute;
      left: 10%;
      right: 10%;
      top: 50%;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(0, 200, 215, 0.5), transparent);
      z-index: 1;
    }
    .pk-insert-btn {
      position: relative;
      z-index: 2;
      background: rgba(13, 19, 33, 0.95);
      border: 1px dashed var(--studio-cyan);
      color: var(--studio-cyan);
      font-family: var(--studio-font-mono);
      font-size: 11px;
      font-weight: 600;
      padding: 4px 14px;
      border-radius: 12px;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(0, 200, 215, 0.2);
      transition: all 0.2s;
    }
    .pk-insert-btn:hover {
      background: var(--studio-cyan);
      color: #000;
      border-style: solid;
      box-shadow: 0 0 16px rgba(0, 200, 215, 0.6);
      transform: scale(1.04);
    }

    /* RIGHT: HUD INSPECTOR DRAWER */
    .inspector-pane {
      width: 580px;
      max-width: 90vw;
      background: var(--studio-panel);
      border-left: 1px solid var(--studio-panel-border);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 20px;
      gap: 14px;
      z-index: 50;
      box-shadow: -8px 0 30px rgba(0, 0, 0, 0.6);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), margin-right 0.25s ease;
    }
    .inspector-pane.collapsed {
      margin-right: -580px;
      transform: translateX(580px);
    }
    .pane-title {
      font-family: var(--studio-font-hud);
      font-size: 12px;
      color: var(--studio-cyan);
      letter-spacing: 1.5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px dashed rgba(0, 200, 215, 0.3);
      padding-bottom: 6px;
    }

    .inspector-section {
      display: flex;
      flex-direction: column;
      gap: 10px;
      background: rgba(10, 14, 23, 0.7);
      border: 1px solid rgba(0, 200, 215, 0.2);
      border-radius: 4px;
      padding: 12px;
      min-width: 0;
    }
    .inspector-section.global-theme-card {
      border: 1px solid rgba(168, 85, 247, 0.4);
      background: rgba(16, 12, 28, 0.7);
    }
    .section-header {
      font-family: var(--studio-font-hud);
      font-size: 11px;
      color: var(--studio-cyan);
      letter-spacing: 1px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px dashed rgba(0, 200, 215, 0.25);
      padding-bottom: 4px;
    }
    .global-theme-card .section-header {
      color: var(--studio-purple);
      border-bottom-color: rgba(168, 85, 247, 0.3);
    }

    .control-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
      min-width: 0;
    }
    .control-group label {
      font-size: 10.5px;
      color: var(--studio-text-dim);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .control-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      min-width: 0;
    }
    .control-row.tri {
      grid-template-columns: 1fr 1fr 1fr;
      min-width: 0;
    }

    select, input[type="text"], input[type="number"], textarea {
      min-width: 0;
      max-width: 100%;
      box-sizing: border-box;
      background: rgba(10, 14, 23, 0.85);
      border: 1px solid rgba(0, 200, 215, 0.3);
      color: var(--studio-text);
      font-family: var(--studio-font-mono);
      font-size: 12px;
      padding: 7px 10px;
      outline: none;
      transition: border-color 0.2s;
      border-radius: 3px;
    }
    select:focus, input:focus, textarea:focus {
      border-color: var(--studio-cyan);
      box-shadow: 0 0 8px rgba(0, 200, 215, 0.3);
    }
    select:disabled, input:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      border-color: rgba(255, 255, 255, 0.15);
    }

    .checkbox-row {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      font-size: 11.5px;
      color: var(--studio-text);
    }
    .checkbox-row input {
      accent-color: var(--studio-cyan);
    }

    .color-picker-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .color-picker-row input[type="color"] {
      width: 32px;
      height: 32px;
      padding: 0;
      border: 1px solid rgba(0, 200, 215, 0.4);
      background: transparent;
      border-radius: 3px;
      cursor: pointer;
    }

    /* Live Component Preview Card inside Inspector */
    .live-card {
      border: 1px solid rgba(0, 200, 215, 0.4);
      background: rgba(6, 9, 15, 0.95);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
      border-radius: 4px;
    }
    .live-preview-box {
      width: 100%;
      min-height: 120px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0d1117;
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 12px;
      overflow: hidden;
      position: relative;
      border-radius: 3px;
      transition: background 0.2s, border-color 0.2s;
    }
    .live-preview-box.light-preview {
      background: #ffffff !important;
      border-color: #d0d7de !important;
    }
    .live-preview-box svg {
      max-width: 100%;
      height: auto;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
    }
    .debug-grid-overlay {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      pointer-events: none;
      border: 2px dashed rgba(245, 158, 11, 0.8);
      background-image: 
        linear-gradient(rgba(245, 158, 11, 0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(245, 158, 11, 0.12) 1px, transparent 1px);
      background-size: 20px 20px;
      display: none;
      z-index: 10;
    }
    .debug-active .debug-grid-overlay {
      display: block;
    }
    .debug-active #readme-preview-content .pk-block-wrapper {
      outline: 1px dashed rgba(245, 158, 11, 0.7) !important;
      position: relative;
    }
    .debug-active #readme-preview-content .pk-block-wrapper::after {
      content: "HUD // " attr(data-pk-type) " #" attr(data-pk-id);
      position: absolute;
      top: 2px;
      right: 6px;
      font-family: var(--studio-font-mono);
      font-size: 9px;
      color: var(--studio-amber);
      background: rgba(10, 14, 23, 0.9);
      padding: 1px 4px;
      border: 1px solid var(--studio-amber);
      border-radius: 2px;
      pointer-events: none;
      z-index: 50;
    }

    .char-badge {
      font-size: 9.5px;
      padding: 1px 5px;
      border-radius: 2px;
      font-weight: 600;
      text-transform: none;
    }
    .badge-optimal { background: rgba(0, 210, 106, 0.2); color: #00d26a; border: 1px solid #00d26a; }
    .badge-warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
    .badge-danger  { background: rgba(239, 68, 68, 0.2);  color: #ef4444; border: 1px solid #ef4444; }

    /* Raw Directive Code Textarea */
    .raw-directive-editor {
      width: 100%;
      height: 80px;
      font-family: var(--studio-font-mono);
      font-size: 11px;
      background: #000;
      color: #00d26a;
      border: 1px solid rgba(0, 200, 215, 0.3);
      padding: 8px;
      border-radius: 3px;
      resize: vertical;
    }

    .action-btn-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 4px;
    }
    .action-btn-row.tri-btn {
      grid-template-columns: 2fr 1fr 1fr;
    }
    .btn-save {
      background: var(--studio-cyan);
      color: #000;
      font-weight: 700;
      border-color: var(--studio-cyan);
    }
    .btn-save:hover {
      box-shadow: 0 0 16px rgba(0, 200, 215, 0.8);
    }
    .btn-cyan {
      background: var(--studio-cyan);
      color: #000;
      font-weight: 700;
      border-color: var(--studio-cyan);
    }
    .btn-cyan:hover {
      box-shadow: 0 0 16px rgba(0, 200, 215, 0.8);
    }
    .btn-purple {
      background: var(--studio-purple);
      color: #fff;
      font-weight: 700;
      border-color: var(--studio-purple);
    }
    .btn-purple:hover {
      box-shadow: 0 0 16px rgba(168, 85, 247, 0.8);
    }
    .btn-danger {
      background: rgba(239, 68, 68, 0.15);
      border-color: var(--studio-danger);
      color: var(--studio-danger);
    }
    .btn-danger:hover {
      background: var(--studio-danger);
      color: #fff;
      box-shadow: 0 0 12px rgba(239, 68, 68, 0.6);
    }

    /* Milestones List Item in Inspector */
    .milestone-item-row {
      display: grid;
      grid-template-columns: 1fr 85px 110px 30px;
      gap: 6px;
      align-items: center;
      margin-bottom: 6px;
    }
    .milestone-item-row input, .milestone-item-row select {
      font-size: 11px;
      padding: 5px 6px;
    }
  </style>
</head>
<body>
  <!-- TOP HUD BAR -->
  <header class="hud-nav">
    <div class="brand">
      <span>PIXEL-KIT</span>
      <span class="brand-badge">STUDIO v4.2</span>
    </div>

    <div class="nav-status">
      <div class="status-indicator">
        <span class="pulse-dot"></span>
        <span id="sse-status">HUD STUDIO SYNC: ONLINE</span>
      </div>

      <div class="mode-switch-group">
        <button class="mode-tab active" id="tab-mode-edit" onclick="setStudioMode('edit')" title="Edit Mode: click-to-edit blocks, hover HUD actions, add block dividers"><svg viewBox="0 0 16 16" width="12" height="12" fill="currentColor" style="vertical-align:-1px;margin-right:4px;"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25a1.75 1.75 0 0 1 .445-.758l8.61-8.61Zm1.414 1.06a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354l-1.086-1.086ZM11.189 6.25 9.75 4.81 3.292 11.268a.25.25 0 0 0-.063.108l-.547 1.912 1.912-.547a.25.25 0 0 0 .108-.063L11.189 6.25Z"/></svg>EDIT</button>
        <button class="mode-tab" id="tab-mode-view" onclick="setStudioMode('view')" title="View Mode: 100% authentic GitHub render with inline chips"><svg viewBox="0 0 16 16" width="12" height="12" fill="currentColor" style="vertical-align:-1px;margin-right:4px;"><path d="M8 2c1.981 0 3.67.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 0 1 0 1.798c-.45.678-1.367 1.932-2.637 3.023C11.67 13.008 9.981 14 8 14c-1.981 0-3.67-.992-4.933-2.078C1.797 10.83.88 9.577.43 8.899a1.62 1.62 0 0 1 0-1.798c.45-.678 1.367-1.932 2.637-3.023C4.33 2.992 6.019 2 8 2ZM1.679 8c.373.534 1.144 1.554 2.21 2.47C4.945 11.379 6.37 12.25 8 12.25c1.63 0 3.055-.871 4.111-1.78 1.066-.916 1.837-1.936 2.21-2.47-.373-.534-1.144-1.554-2.21-2.47C10.945 4.621 9.52 3.75 8 3.75c-1.63 0-3.055.871-4.111 1.78C2.823 6.446 2.052 7.466 1.679 8ZM8 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 1.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Z"/></svg>VIEW</button>
      </div>

      <div class="theme-switch-group">
        <button class="theme-tab active" id="tab-dark" onclick="switchPreviewTheme('dark')"><svg viewBox="0 0 16 16" width="11" height="11" fill="currentColor" style="vertical-align:-1px;margin-right:4px;"><path d="M9.598 1.591a.749.749 0 0 1 .785-.175 7.001 7.001 0 1 1-8.967 8.967.75.75 0 0 1 .961-.96 5.5 5.5 0 0 0 7.046-7.046.75.75 0 0 1 .175-.786Zm1.616 1.945a7 7 0 0 1-7.668 7.668 8.501 8.501 0 1 0 7.668-7.668Z"/></svg>DARK</button>
        <button class="theme-tab" id="tab-light" onclick="switchPreviewTheme('light')"><svg viewBox="0 0 16 16" width="11" height="11" fill="currentColor" style="vertical-align:-1px;margin-right:4px;"><path d="M8 12a4 4 0 1 1 0-8 4 4 0 0 1 0 8Zm0-1.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Zm0-8.5a.75.75 0 0 1 .75.75v1a.75.75 0 0 1-1.5 0v-1A.75.75 0 0 1 8 2Zm0 10.5a.75.75 0 0 1 .75.75v1a.75.75 0 0 1-1.5 0v-1a.75.75 0 0 1 .75-.75ZM2.75 7.25h1a.75.75 0 0 1 0 1.5h-1a.75.75 0 0 1 0-1.5Zm10.5 0h1a.75.75 0 0 1 0 1.5h-1a.75.75 0 0 1 0-1.5ZM4.28 4.28a.75.75 0 0 1 1.06 0l.707.707a.75.75 0 0 1-1.06 1.06l-.707-.707a.75.75 0 0 1 0-1.06Zm6.727 6.727a.75.75 0 0 1 1.06 0l.707.707a.75.75 0 1 1-1.06 1.06l-.707-.707a.75.75 0 0 1 0-1.06Zm-6.727 1.767a.75.75 0 0 1 0-1.06l.707-.707a.75.75 0 1 1 1.06 1.06l-.707.707a.75.75 0 0 1-1.06 0Zm6.727-6.727a.75.75 0 0 1 0-1.06l.707-.707a.75.75 0 1 1 1.06 1.06l-.707.707a.75.75 0 0 1 0-1.06Z"/></svg>LIGHT</button>
      </div>

      <button class="nav-btn btn-green" id="btn-git-push" onclick="pushReadmeToGit()" title="Safely stage only README and assets and push to git"><svg viewBox="0 0 16 16" width="12" height="12" fill="currentColor" style="vertical-align:-1px;margin-right:4px;"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 13.25 15H2.75A1.75 1.75 0 0 1 1 13.25Zm7.75 2.5a.75.75 0 0 0-1.5 0v3.44l-1.22-1.22a.75.75 0 0 0-1.06 1.06l2.5 2.5a.75.75 0 0 0 1.06 0l2.5-2.5a.75.75 0 1 0-1.06-1.06L8.75 8.69Z"/></svg>[ PUSH README ]</button>
      <button class="nav-btn btn-amber" id="btn-debug" onclick="toggleDebugMode()" title="Toggle Pixel Alignment & HUD Grid Overlay">[ HUD GRID ]</button>
      <button class="nav-btn active-btn" id="btn-toggle-inspector" onclick="toggleInspector()">INSPECTOR [TAB]</button>
    </div>
  </header>

  <!-- MAIN VIEWPORT SPLIT -->
  <div class="studio-container" id="main-studio-container">
    <!-- LEFT: GITHUB-LIKE PREVIEW -->
    <main class="preview-pane" id="preview-scroll-area">
      <div class="gh-readme-wrapper">
        <div class="gh-card-header">
          <div class="gh-card-title">
            <svg viewBox="0 0 16 16" width="16" height="16">
              <path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501A3.743 3.743 0 0 1 11.006 1h4.245a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.507a2.25 2.25 0 0 0-1.591.659l-.622.621a.75.75 0 0 1-1.06 0l-.622-.621A2.25 2.25 0 0 0 5.258 13H.75a.75.75 0 0 1-.75-.75Zm7.251 10.324.004-5.073-.002-2.253A2.25 2.25 0 0 0 5.003 2.5H1.5v9h3.757a3.75 3.75 0 0 1 1.994.574ZM8.755 4.75l-.004 7.322a3.752 3.752 0 0 1 1.992-.572H14.5v-9h-3.494a2.25 2.25 0 0 0-2.251 2.25Z"></path>
            </svg>
            <span id="template-filename">README.md</span>
            <span class="gh-badge">Preview</span>
          </div>
          <div class="gh-card-meta">
            <span id="gh-stats-lines">-- lines</span> • <span id="gh-stats-bytes">-- KB</span>
          </div>
        </div>
        <article class="markdown-body entry-content" id="readme-preview-content" data-color-mode="dark">
          <!-- Compiled README HTML Injected Here -->
        </article>
      </div>
    </main>

    <!-- RIGHT: HUD INSPECTOR DRAWER -->
    <aside class="inspector-pane" id="inspector-panel">
      <div class="pane-title">
        <span id="lbl-inspector-heading">■ BLOCK INSPECTOR</span>
        <button class="nav-btn" style="padding:2px 8px;font-size:10px;" onclick="toggleInspector()">✕</button>
      </div>

      <!-- Quick Template Blocks Jump Selector -->
      <div class="control-group" id="group-existing-blocks">
        <label>
          <span>Jump to Block</span>
          <span id="block-counter-badge" class="char-badge badge-optimal">0 blocks</span>
        </label>
        <select id="sel-existing-block" onchange="onSelectExistingBlock()" style="border-color:var(--studio-cyan);font-weight:600;">
          <option value="">(Loading blocks...)</option>
        </select>
      </div>

      <!-- SECTION 0: GLOBAL THEME CONTROLLER (Batch 1-Click Update) -->
      <div class="inspector-section global-theme-card" id="section-global-theme">
        <div class="section-header">
          <span>// GLOBAL THEME CONTROLLER</span>
          <span style="font-size:9.5px;color:var(--studio-purple);">ALL BLOCKS</span>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Global Style</label>
            <select id="sel-global-style" onchange="onGlobalThemeParamChange()">
              <option value="cyberpunk">Cyberpunk</option>
              <option value="tactical">Tactical</option>
              <option value="minimal">Minimal Glass</option>
            </select>
          </div>
          <div class="control-group">
            <label>Global Preset</label>
            <select id="sel-global-preset" onchange="onGlobalPresetChange()">
              <option value="cyberpunk">Cyan / Purple</option>
              <option value="amber">Amber Tactical</option>
              <option value="matrix">Matrix Green</option>
              <option value="tokyo">Tokyo Neon</option>
              <option value="custom">Custom (Hex Pickers)</option>
            </select>
          </div>
        </div>

        <div class="control-row">
          <div class="control-group">
            <label>Global Theme Mode</label>
            <select id="sel-global-mode">
              <option value="auto">Auto (Dark + Light)</option>
              <option value="dark">Dark Only</option>
              <option value="light">Light Only</option>
              <option value="transparent">Transparent</option>
            </select>
          </div>
          <div class="control-group">
            <label>Primary Hex</label>
            <div class="color-picker-row">
              <input type="color" id="picker-global-primary" value="#00c8d7" oninput="syncGlobalColor('primary', 'picker')">
              <input type="text" id="inp-global-primary" value="#00c8d7" oninput="syncGlobalColor('primary', 'text')" style="flex:1;">
            </div>
          </div>
        </div>

        <div class="control-row">
          <div class="control-group">
            <label>Accent Hex</label>
            <div class="color-picker-row">
              <input type="color" id="picker-global-accent" value="#a855f7" oninput="syncGlobalColor('accent', 'picker')">
              <input type="text" id="inp-global-accent" value="#a855f7" oninput="syncGlobalColor('accent', 'text')" style="flex:1;">
            </div>
          </div>
          <div class="control-group">
            <label>Tertiary Hex</label>
            <div class="color-picker-row">
              <input type="color" id="picker-global-tertiary" value="#ff0055" oninput="syncGlobalColor('tertiary', 'picker')">
              <input type="text" id="inp-global-tertiary" value="#ff0055" oninput="syncGlobalColor('tertiary', 'text')" style="flex:1;">
            </div>
          </div>
        </div>

        <div class="control-row" style="margin-top:6px;">
          <div class="control-group" style="width:100%;">
            <div style="display:flex;gap:6px;width:100%;">
              <button class="nav-btn btn-cyan" style="flex:1;" onclick="applyGlobalThemeToAllBlocks(false)" title="Soft Apply: updates style and Primary, preserves block custom accents">[ SOFT APPLY ]</button>
              <button class="nav-btn btn-purple" style="flex:1;" onclick="applyGlobalThemeToAllBlocks(true)" title="Force Apply: overrides all blocks, wiping custom colors">[ FORCE ALL ]</button>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 1: CORE BLOCK TYPE & THEME -->
      <div class="inspector-section">
        <div class="section-header">
          <span>1. CORE IDENTIFIER & THEME</span>
          <span id="badge-lock-type" class="char-badge" style="display:none;background:rgba(245,158,11,0.2);color:#f59e0b;border:1px solid #f59e0b;">LOCKED (EDIT)</span>
        </div>

        <div class="control-group">
          <label>Block Type</label>
          <select id="sel-type" onchange="onTypeChange(true)">
            <option value="header">Header Banner</option>
            <option value="timeline">PCB Timeline / Roadmap</option>
            <option value="window">Window Frame Monolith</option>
            <option value="terminal">Terminal (Details/Summary)</option>
            <option value="quote">Quote Box Alert</option>
            <option value="metrics">Metrics KPI Card</option>
            <option value="progress">Progress HUD Bar</option>
            <option value="techstack">Tech Stack Matrix</option>
            <option value="callout">Callout Alert</option>
            <option value="frame">Window Cap (Top/Bottom)</option>
            <option value="chip">Holographic Chip</option>
            <option value="divider">Chapter Divider</option>
            <option value="splitter">Sub-Module Splitter</option>
            <option value="footer">Closing Footer Plate</option>
            <option value="social">OpenGraph Social Card</option>
          </select>
        </div>

        <!-- Inherit Global Theme Checkbox -->
        <div class="control-group">
          <label class="checkbox-row" style="margin:2px 0 6px 0;">
            <input type="checkbox" id="chk-inherit-theme" checked onchange="onInheritThemeToggle()">
            <span style="font-weight:600;color:var(--studio-cyan);">[x] Inherit Global Theme (Default)</span>
          </label>
        </div>

        <div id="block-theme-override-controls" style="display:none;">
          <div class="control-row">
            <div class="control-group">
              <label>Style</label>
              <select id="sel-style" onchange="debounceRender()">
                <option value="cyberpunk">Cyberpunk</option>
                <option value="tactical">Tactical</option>
                <option value="minimal">Minimal Glass</option>
              </select>
            </div>
            <div class="control-group">
              <label>Palette Preset</label>
              <select id="sel-preset" onchange="onBlockPresetChange()">
                <option value="cyberpunk">Cyan / Purple</option>
                <option value="amber">Amber Tactical</option>
                <option value="matrix">Matrix Green</option>
                <option value="tokyo">Tokyo Neon</option>
              </select>
            </div>
          </div>

          <div class="control-row">
            <div class="control-group">
              <label>Theme Mode</label>
              <select id="sel-mode" onchange="debounceRender()">
                <option value="auto">Auto (Dark + Light)</option>
                <option value="dark">Dark Only</option>
                <option value="light">Light Only</option>
                <option value="transparent">Transparent</option>
              </select>
            </div>
            <div class="control-group">
              <label>Color Mode</label>
              <div style="display:flex;gap:12px;margin-top:7px;font-size:11px;">
                <label style="cursor:pointer;display:flex;align-items:center;gap:4px;">
                  <input type="radio" name="block-color-mode" id="rad-preset" value="preset" checked onchange="onBlockColorModeToggle()">
                  <span>Preset</span>
                </label>
                <label style="cursor:pointer;display:flex;align-items:center;gap:4px;">
                  <input type="radio" name="block-color-mode" id="rad-custom" value="custom" onchange="onBlockColorModeToggle()">
                  <span>Custom Hex</span>
                </label>
              </div>
            </div>
          </div>

          <div class="control-row" id="row-custom-colors" style="opacity:0.4;pointer-events:none;">
            <div class="control-group">
              <label>Custom Primary</label>
              <div class="color-picker-row">
                <input type="color" id="picker-primary" value="#00c8d7" oninput="syncBlockColor('primary', 'picker')">
                <input type="text" id="inp-primary" value="#00c8d7" oninput="syncBlockColor('primary', 'text')" style="flex:1;">
              </div>
            </div>
            <div class="control-group">
              <label>Custom Accent</label>
              <div class="color-picker-row">
                <input type="color" id="picker-accent" value="#a855f7" oninput="syncBlockColor('accent', 'picker')">
                <input type="text" id="inp-accent" value="#a855f7" oninput="syncBlockColor('accent', 'text')" style="flex:1;">
              </div>
            </div>
            <div class="control-group">
              <label>Custom Tertiary</label>
              <div class="color-picker-row">
                <input type="color" id="picker-tertiary" value="#ff0055" oninput="syncBlockColor('tertiary', 'picker')">
                <input type="text" id="inp-tertiary" value="#ff0055" oninput="syncBlockColor('tertiary', 'text')" style="flex:1;">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- DYNAMIC CONTEXTUAL FIELD SECTIONS -->

      <!-- 1. HEADER ATTRIBUTES -->
      <div class="inspector-section" id="section-header">
        <div class="section-header">
          <span>2. BANNER PARAMETERS & LEVEL-3 SPECS</span>
        </div>
        <div class="control-group">
          <label>Title <span id="badge-title-budget" class="char-badge badge-optimal">0 chars</span></label>
          <input type="text" id="inp-title" value="PIXEL README KIT" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Subtitle <span id="badge-sub-budget" class="char-badge badge-optimal">0 chars</span></label>
          <input type="text" id="inp-subtitle" value="RETRO-FUTURISTIC HUD & SCI-FI INFOGRAPHICS" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Tag / Status Badge</label>
          <input type="text" id="inp-tag" value="SYSTEM_ONLINE" oninput="debounceRender()">
        </div>
        <div id="group-header-specs" style="display:flex;flex-direction:column;gap:10px;">
          <div class="control-group">
            <label>Spec 1 (Telemetry Line 1) <span id="badge-spec1-budget" class="char-badge badge-optimal">0 chars</span></label>
            <input type="text" id="inp-spec1" placeholder="e.g. CORE // KERNEL 5.15" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Spec 2 (Telemetry Line 2) <span id="badge-spec2-budget" class="char-badge badge-optimal">0 chars</span></label>
            <input type="text" id="inp-spec2" placeholder="e.g. NET // 10Gbps SECURE" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Spec 3 (Telemetry Line 3) <span id="badge-spec3-budget" class="char-badge badge-optimal">0 chars</span></label>
            <input type="text" id="inp-spec3" placeholder="e.g. STATUS // NOMINAL" oninput="debounceRender()">
          </div>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Tag URL (Right Link)</label>
            <input type="text" id="inp-tag-url" placeholder="https://..." oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Close URL ([X] Link)</label>
            <input type="text" id="inp-close-url" placeholder="#top" oninput="debounceRender()">
          </div>
        </div>
        <div class="control-group">
          <label class="checkbox-row" style="margin-top:4px;">
            <input type="checkbox" id="chk-compact" onchange="updateContextualVisibility(); debounceRender();">
            <span>Compact Banner Mode (Mobile Viewport ~84px)</span>
          </label>
        </div>
      </div>

      <!-- 2. TIMELINE ATTRIBUTES -->
      <div class="inspector-section" id="section-timeline" style="display:none;">
        <div class="section-header">
          <span>2. PCB TIMELINE / ROADMAP STAGES</span>
        </div>
        <div class="control-group">
          <label>Milestones (One per line: milestone title="..." date="..." status="..." desc="...")</label>
          <textarea id="inp-timeline-milestones" rows="7" style="font-size:11px;" placeholder='milestone title="STAGE 1" date="2026-Q1" status="COMPLETED" desc="Research & architecture"&#10;milestone title="STAGE 2" date="2026-Q2" status="IN_PROGRESS" desc="Core runtime & tests"&#10;milestone title="STAGE 3" date="2026-Q3" status="PLANNED" desc="HUD Studio & launch"' oninput="debounceRender()"></textarea>
        </div>
        <div style="display:flex;gap:8px;">
          <button class="nav-btn" type="button" style="font-size:10px;padding:3px 8px;" onclick="addSampleMilestone()">+ Add Milestone Template</button>
        </div>
      </div>

      <!-- 3. WINDOW MONOLITH ATTRIBUTES -->
      <div class="inspector-section" id="section-window" style="display:none;">
        <div class="section-header">
          <span>2. WINDOW FRAME CONTAINER</span>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Window Title</label>
            <input type="text" id="inp-window-title" value="SYSTEM.WINDOW" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Window Tag</label>
            <input type="text" id="inp-window-tag" value="[SYS_LOG]" oninput="debounceRender()">
          </div>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Tag URL</label>
            <input type="text" id="inp-window-tag-url" placeholder="https://..." oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Close URL</label>
            <input type="text" id="inp-window-close-url" placeholder="#top" oninput="debounceRender()">
          </div>
        </div>
      </div>

      <!-- 4. TERMINAL (DETAILS/SUMMARY) ATTRIBUTES -->
      <div class="inspector-section" id="section-terminal" style="display:none;">
        <div class="section-header">
          <span>2. TERMINAL (DETAILS/SUMMARY)</span>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Terminal Title</label>
            <input type="text" id="inp-terminal-title" value="HUD.TERMINAL" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Initial State</label>
            <select id="sel-terminal-state" onchange="debounceRender()">
              <option value="open">Expanded (open)</option>
              <option value="closed">Collapsed (closed)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 5. QUOTE CALLOUT ATTRIBUTES -->
      <div class="inspector-section" id="section-quote" style="display:none;">
        <div class="section-header">
          <span>2. QUOTE BLOCKQUOTE HEADER</span>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Quote Title</label>
            <input type="text" id="inp-quote-title" value="SPECIFICATION NOTICE" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Badge</label>
            <select id="sel-quote-badge" onchange="onQuoteBadgeChange()">
              <option value="NOTE">NOTE (Blue #2f81f7)</option>
              <option value="TIP">TIP (Green #238636)</option>
              <option value="IMPORTANT">IMPORTANT (Purple #8957e5)</option>
              <option value="WARNING">WARNING (Amber #d29922)</option>
              <option value="CAUTION">CAUTION (Red #f85149)</option>
              <option value="CRITICAL">CRITICAL (Red #f85149)</option>
              <option value="SUCCESS">SUCCESS (Green #238636)</option>
              <option value="INFO">INFO (Purple #8957e5)</option>
            </select>
          </div>
        </div>
        <div class="control-row" id="row-quote-badge">
          <div class="control-group">
            <label class="checkbox-row" style="margin-top:6px;">
              <input type="checkbox" id="chk-quote-custom-badge" onchange="onQuoteCustomBadgeToggle()">
              <span>Custom Badge Color</span>
            </label>
          </div>
          <div class="control-group" id="quote-badge-color-group" style="display:none;">
            <label>Badge Hex</label>
            <div class="color-picker-row">
              <input type="color" id="picker-quote-badge-color" value="#2f81f7" oninput="syncQuoteBadgeColor('picker')">
              <input type="text" id="inp-quote-badge-color" value="#2f81f7" oninput="syncQuoteBadgeColor('text')" style="flex:1;">
            </div>
          </div>
        </div>
        <div class="control-group">
          <label>Subtitle</label>
          <input type="text" id="inp-quote-sub" value="Content flows into live blockquote text" oninput="debounceRender()">
        </div>
      </div>

      <!-- 6. CHIP ATTRIBUTES -->
      <div class="inspector-section" id="section-chip" style="display:none;">
        <div class="section-header">
          <span>2. CHIP PARAMETERS & GITHUB STATS</span>
        </div>
        <div class="control-group">
          <label>Chip Text</label>
          <input type="text" id="inp-chip-text" value="CHIP" oninput="debounceRender()">
        </div>
        <div class="control-row" id="row-chip-form">
          <div class="control-group">
            <label>Chip Form</label>
            <select id="sel-chip-type" onchange="updateContextualVisibility(); debounceRender();">
              <option value="closed">Closed Hologram</option>
              <option value="decay">Decay Wireframe</option>
              <option value="pulse">Pulse Reactor</option>
            </select>
          </div>
          <div class="control-group" id="group-decay-dir">
            <label>Decay Direction</label>
            <select id="sel-decay-dir" onchange="debounceRender()">
              <option value="right">Right</option>
              <option value="left">Left</option>
              <option value="both">Both</option>
            </select>
          </div>
        </div>
        <div class="control-row" id="row-chip-gh">
          <div class="control-group">
            <label>GitHub Auto Stat</label>
            <select id="sel-chip-gh" onchange="updateContextualVisibility(); debounceRender();">
              <option value="">(None - Custom Text)</option>
              <option value="stars">Stars</option>
              <option value="forks">Forks</option>
              <option value="issues">Open Issues</option>
              <option value="license">License</option>
              <option value="watchers">Watchers</option>
              <option value="version">Latest Release</option>
            </select>
          </div>
          <div class="control-group" id="group-chip-repo">
            <label>Repository (owner/repo)</label>
            <input type="text" id="inp-chip-repo" placeholder="Kazinagg/pixel-readme-kit" oninput="debounceRender()">
          </div>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Custom Width (px)</label>
            <input type="number" id="inp-chip-width" placeholder="Auto" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Link URL</label>
            <input type="text" id="inp-chip-url" placeholder="https://..." oninput="debounceRender()">
          </div>
        </div>
      </div>

      <!-- 7. METRICS ATTRIBUTES -->
      <div class="inspector-section" id="section-metrics" style="display:none;">
        <div class="section-header">
          <span>2. METRICS & KPI CARDS</span>
        </div>
        <div class="control-group">
          <label>Quick Cards (LABEL: VAL (+DELTA) [STATUS] | ...)</label>
          <textarea id="inp-metrics-items" rows="3" placeholder="FPS: 120+ (+24%) [OPTIMAL] | LATENCY: 2.1ms | MEM: 64MB" oninput="debounceRender()"></textarea>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Card Label</label>
            <input type="text" id="inp-metrics-label" placeholder="BENCHMARK" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Card Value</label>
            <input type="text" id="inp-metrics-val" placeholder="1,200+" oninput="debounceRender()">
          </div>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Delta / Benchmark</label>
            <input type="text" id="inp-metrics-delta" placeholder="+24% vs base" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Status Badge</label>
            <input type="text" id="inp-metrics-status" placeholder="OPTIMAL" oninput="debounceRender()">
          </div>
        </div>
      </div>

      <!-- 8. PROGRESS ATTRIBUTES -->
      <div class="inspector-section" id="section-progress" style="display:none;">
        <div class="section-header">
          <span>2. PROGRESS HUD BAR</span>
        </div>
        <div class="control-group">
          <label>Percentage: <span id="lbl-progress-num" style="color:var(--studio-cyan);font-weight:700;">75%</span></label>
          <div style="display:flex;gap:10px;align-items:center;">
            <input type="range" id="rng-progress-val" min="0" max="100" value="75" style="flex:1;" oninput="syncProgressInput('range')">
            <input type="number" id="inp-progress-val" min="0" max="100" value="75" style="width:65px;" oninput="syncProgressInput('num')">
          </div>
        </div>
        <div class="control-group">
          <label>Label</label>
          <input type="text" id="inp-progress-label" value="CORE SYSTEM PROGRESS" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Subtext Diagnostic</label>
          <input type="text" id="inp-progress-sub" value="STAGE 4/5 // COMPILATION COMPLETE" oninput="debounceRender()">
        </div>
      </div>

      <!-- 9. TECHSTACK ATTRIBUTES -->
      <div class="inspector-section" id="section-techstack" style="display:none;">
        <div class="section-header">
          <span>2. TECH STACK MATRIX</span>
        </div>
        <div class="control-group">
          <label>Tech Icons (comma-separated)</label>
          <input type="text" id="inp-techstack-items" value="python,cpp,docker,git,fastapi" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Grid Columns Count</label>
          <input type="number" id="inp-techstack-cols" value="5" min="1" max="12" oninput="debounceRender()">
        </div>
      </div>

      <!-- 10. CALLOUT ATTRIBUTES -->
      <div class="inspector-section" id="section-callout" style="display:none;">
        <div class="section-header">
          <span>2. CALLOUT & QUOTE ALERT</span>
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Badge Type</label>
            <select id="sel-callout-type" onchange="onCalloutTypeChange()">
              <option value="note">Note (Blue #2f81f7)</option>
              <option value="tip">Tip (Green #238636)</option>
              <option value="important">Important (Purple #8957e5)</option>
              <option value="warning">Warning (Amber #d29922)</option>
              <option value="caution">Caution (Red #f85149)</option>
              <option value="critical">Critical (Red #f85149)</option>
              <option value="success">Success (Green #238636)</option>
              <option value="info">Info (Purple #8957e5)</option>
            </select>
          </div>
          <div class="control-group" style="justify-content:center;">
            <label class="checkbox-row" style="margin-top:14px;">
              <input type="checkbox" id="chk-callout-quote" onchange="debounceRender()">
              <span>Quote Box Styling</span>
            </label>
          </div>
        </div>
        <div class="control-row" id="row-callout-badge">
          <div class="control-group">
            <label class="checkbox-row" style="margin-top:6px;">
              <input type="checkbox" id="chk-callout-custom-badge" onchange="onCalloutCustomBadgeToggle()">
              <span>Custom Badge Color</span>
            </label>
          </div>
          <div class="control-group" id="callout-badge-color-group" style="display:none;">
            <label>Badge Hex</label>
            <div class="color-picker-row">
              <input type="color" id="picker-callout-badge-color" value="#2f81f7" oninput="syncCalloutBadgeColor('picker')">
              <input type="text" id="inp-callout-badge-color" value="#2f81f7" oninput="syncCalloutBadgeColor('text')" style="flex:1;">
            </div>
          </div>
        </div>
        <div class="control-group">
          <label>Alert Title</label>
          <input type="text" id="inp-callout-title" value="SYSTEM SPECIFICATION" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Alert Message / Subtitle</label>
          <input type="text" id="inp-callout-sub" value="Autonomous neural interface loaded successfully." oninput="debounceRender()">
        </div>
      </div>

      <!-- 11. FRAME ATTRIBUTES -->
      <div class="inspector-section" id="section-frame" style="display:none;">
        <div class="section-header">
          <span>2. FRAME WINDOW CAP</span>
        </div>
        <div class="control-row" id="row-frame-cap">
          <div class="control-group">
            <label>Cap Type</label>
            <select id="sel-frame-type" onchange="updateContextualVisibility(); debounceRender();">
              <option value="top">Top Cap</option>
              <option value="bottom">Bottom Cap</option>
            </select>
          </div>
          <div class="control-group" id="group-frame-tag">
            <label>Frame Tag</label>
            <input type="text" id="inp-frame-tag" value="[OPEN_HUD]" oninput="debounceRender()">
          </div>
        </div>
        <div class="control-group" id="group-frame-title">
          <label>Frame Title</label>
          <input type="text" id="inp-frame-title" value="SYSTEM.CORE" oninput="debounceRender()">
        </div>
        <div class="control-row" id="row-frame-links">
          <div class="control-group" id="group-frame-tag-url">
            <label>Tag URL</label>
            <input type="text" id="inp-frame-tag-url" placeholder="https://..." oninput="debounceRender()">
          </div>
          <div class="control-group" id="group-frame-close-url">
            <label>Close URL</label>
            <input type="text" id="inp-frame-close-url" placeholder="#top" oninput="debounceRender()">
          </div>
        </div>
      </div>

      <!-- 12. DIVIDER ATTRIBUTES -->
      <div class="inspector-section" id="section-divider" style="display:none;">
        <div class="section-header">
          <span>2. CHAPTER DIVIDER</span>
        </div>
        <p style="font-size:11.5px;color:var(--studio-text-dim);">
          Vector chapter divider with pixel grid ornaments and style accents. Inherits style, preset, mode, and colors from above.
        </p>
      </div>

      <!-- 13. SPLITTER ATTRIBUTES -->
      <div class="inspector-section" id="section-splitter" style="display:none;">
        <div class="section-header">
          <span>2. SUB-MODULE SPLITTER</span>
        </div>
        <div class="control-group">
          <label>Splitter Label</label>
          <input type="text" id="inp-splitter-label" value="[SUB_MODULE: DATABASE]" oninput="debounceRender()">
        </div>
      </div>

      <!-- 14. FOOTER ATTRIBUTES -->
      <div class="inspector-section" id="section-footer" style="display:none;">
        <div class="section-header">
          <span>2. CLOSING FOOTER PLATE</span>
        </div>
        <div class="control-group">
          <label>Status Message</label>
          <input type="text" id="inp-footer-status" value="SESSION_ACTIVE // STANDBY" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Nav Link Text</label>
          <input type="text" id="inp-footer-nav" value="▲ RETURN TO TOP" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Diagnostic Subtext</label>
          <input type="text" id="inp-footer-sub" value="END OF TELEMETRY STREAM" oninput="debounceRender()">
        </div>
      </div>

      <!-- 15. SOCIAL ATTRIBUTES -->
      <div class="inspector-section" id="section-social" style="display:none;">
        <div class="section-header">
          <span>2. OPENGRAPH SOCIAL CARD</span>
        </div>
        <div class="control-group">
          <label>Main Title</label>
          <input type="text" id="inp-social-title" value="PIXEL README KIT" oninput="debounceRender()">
        </div>
        <div class="control-group">
          <label>Description Subtitle</label>
          <input type="text" id="inp-social-sub" value="Retro-Futuristic HUD & Sci-Fi Infographics" oninput="debounceRender()">
        </div>
        <div class="control-row">
          <div class="control-group">
            <label>Repository</label>
            <input type="text" id="inp-social-repo" value="Kazinagg/pixel-readme-kit" oninput="debounceRender()">
          </div>
          <div class="control-group">
            <label>Tags (comma-separated)</label>
            <input type="text" id="inp-social-tags" value="PYTHON,SVG,CYBERPUNK" oninput="debounceRender()">
          </div>
        </div>
      </div>

      <!-- CONTAINER BODY CONTENT (For window/terminal/quote) -->
      <div class="inspector-section" id="section-body" style="display:none;">
        <div class="section-header">
          <span>3. INNER CONTAINER BODY (MARKDOWN)</span>
        </div>
        <div class="control-group">
          <textarea id="inp-body" rows="6" placeholder="Inner markdown content..." oninput="debounceRender()"></textarea>
        </div>
      </div>

      <!-- LIVE PREVIEW & TWO-WAY RAW DIRECTIVE EDITOR -->
      <div class="live-card">
        <div class="section-header" style="border-bottom:none;">
          <span>LIVE SVG PREVIEW</span>
          <span id="render-latency" style="color:var(--studio-amber);font-size:10px;">REALTIME</span>
        </div>
        <div class="live-preview-box" id="live-svg-box">
          <div class="debug-grid-overlay" id="hud-debug-grid"></div>
          <div id="svg-render-mount" style="width:100%;display:flex;align-items:center;justify-content:center;"></div>
        </div>

        <div class="section-header" style="border-bottom:none; margin-top:4px;">
          <span>RAW DIRECTIVE CODE (TWO-WAY EDITABLE)</span>
        </div>
        <textarea class="raw-directive-editor" id="txt-raw-directive" oninput="onRawDirectiveManualEdit()"></textarea>

        <div class="action-btn-row tri-btn" id="edit-mode-actions">
          <button class="nav-btn btn-save" onclick="saveExistingBlockChanges()">[ SAVE ] (Ctrl+S)</button>
          <button class="nav-btn btn-danger" onclick="deleteExistingBlock()">[ DELETE ]</button>
          <button class="nav-btn" onclick="copyDirective()">[ COPY ]</button>
        </div>

        <div class="action-btn-row" id="insert-mode-actions" style="display:none;">
          <button class="nav-btn btn-save" onclick="executeInsertBlock()">[ INSERT ] (Ctrl+S)</button>
          <button class="nav-btn" onclick="cancelInsertMode()">[ CANCEL ]</button>
        </div>
      </div>
    </aside>
  </div>

  <script>
    let renderTimer = null;
    let sseSource = null;
    let debugMode = false;
    let editorMode = 'edit';
    let templateBlocks = [];
    let currentEditingBlockId = null;
    let currentEditingBlockOriginal = null;
    let targetInsertAfterId = -1;
    let isParsingRaw = false;
    let activePreviewTheme = 'dark';

    const PRESET_COLORS = {
      cyberpunk: { primary: "#00c8d7", accent: "#a855f7", tertiary: "#ff0055" },
      amber:     { primary: "#f59e0b", accent: "#ef4444", tertiary: "#ff0055" },
      matrix:    { primary: "#00ff41", accent: "#008f11", tertiary: "#ff0055" },
      tokyo:     { primary: "#f72585", accent: "#7209b7", tertiary: "#06b6d4" }
    };

    function toggleInspector() {
      const panel = document.getElementById("inspector-panel");
      panel.classList.toggle("collapsed");
      const btn = document.getElementById("btn-toggle-inspector");
      if (panel.classList.contains("collapsed")) {
        btn.classList.remove("active-btn");
      } else {
        btn.classList.add("active-btn");
      }
    }

    function openInspector() {
      const panel = document.getElementById("inspector-panel");
      panel.classList.remove("collapsed");
      document.getElementById("btn-toggle-inspector").classList.add("active-btn");
    }

    function toggleDebugMode() {
      debugMode = !debugMode;
      const box = document.getElementById("live-svg-box");
      const btn = document.getElementById("btn-debug");
      const body = document.body;

      if (debugMode) {
        box.classList.add("debug-active");
        body.classList.add("debug-active");
        btn.classList.add("active-btn");
        btn.style.background = "var(--studio-amber)";
        btn.style.color = "#000";
        btn.style.borderColor = "var(--studio-amber)";
      } else {
        box.classList.remove("debug-active");
        body.classList.remove("debug-active");
        btn.classList.remove("active-btn");
        btn.style.background = "";
        btn.style.color = "";
        btn.style.borderColor = "";
      }
    }

    function switchPreviewTheme(theme) {
      activePreviewTheme = theme;
      try { localStorage.setItem("pk_preview_theme", theme); } catch (_) {}
      const scrollArea = document.getElementById("preview-scroll-area");
      const mdBody = document.getElementById("readme-preview-content");
      const tabDark = document.getElementById("tab-dark");
      const tabLight = document.getElementById("tab-light");
      const liveBox = document.getElementById("live-svg-box");

      if (theme === "light") {
        if (scrollArea) {
          scrollArea.classList.add("light-theme");
          scrollArea.setAttribute("data-color-mode", "light");
          scrollArea.setAttribute("data-theme", "light");
        }
        if (mdBody) {
          mdBody.setAttribute("data-color-mode", "light");
          mdBody.setAttribute("data-theme", "light");
        }
        if (liveBox) liveBox.classList.add("light-preview");
        if (tabLight) tabLight.classList.add("active");
        if (tabDark) tabDark.classList.remove("active");
      } else {
        if (scrollArea) {
          scrollArea.classList.remove("light-theme");
          scrollArea.setAttribute("data-color-mode", "dark");
          scrollArea.setAttribute("data-theme", "dark");
        }
        if (mdBody) {
          mdBody.setAttribute("data-color-mode", "dark");
          mdBody.setAttribute("data-theme", "dark");
        }
        if (liveBox) liveBox.classList.remove("light-preview");
        if (tabDark) tabDark.classList.add("active");
        if (tabLight) tabLight.classList.remove("active");
      }
      loadCompiledPreview();
      renderCurrentBlock(false);
    }

    // --- View Mode vs Edit Mode Logic ---
    let currentStudioMode = "edit";
    let cachedEditHtml = "";
    let cachedViewHtml = "";

    function setStudioMode(mode) {
      currentStudioMode = mode;
      try { localStorage.setItem("pk_studio_mode", mode); } catch (_) {}
      const editTab = document.getElementById("tab-mode-edit");
      const viewTab = document.getElementById("tab-mode-view");
      const previewArea = document.getElementById("readme-preview-content");

      if (mode === "view") {
        if (editTab) editTab.classList.remove("active");
        if (viewTab) viewTab.classList.add("active");
        if (previewArea) {
          previewArea.classList.add("view-mode");
          if (cachedViewHtml) {
            previewArea.innerHTML = cachedViewHtml;
          }
        }
      } else {
        if (editTab) editTab.classList.add("active");
        if (viewTab) viewTab.classList.remove("active");
        if (previewArea) {
          previewArea.classList.remove("view-mode");
          if (cachedEditHtml) {
            previewArea.innerHTML = cachedEditHtml;
          }
          if (currentEditingBlockId !== null) {
            highlightBlockInPreview(currentEditingBlockId);
          }
        }
      }
    }

    // --- Global Theme Logic ---
    function onGlobalPresetChange() {
      const preset = document.getElementById("sel-global-preset").value;
      const primPicker = document.getElementById("picker-global-primary");
      const primText = document.getElementById("inp-global-primary");
      const accPicker = document.getElementById("picker-global-accent");
      const accText = document.getElementById("inp-global-accent");
      const tertPicker = document.getElementById("picker-global-tertiary");
      const tertText = document.getElementById("inp-global-tertiary");

      if (preset === "custom") {
        primPicker.style.boxShadow = "0 0 6px var(--studio-cyan)";
        accPicker.style.boxShadow = "0 0 6px var(--studio-purple)";
        if (tertPicker) tertPicker.style.boxShadow = "0 0 6px #ff0055";
        return;
      }
      primPicker.style.boxShadow = "none";
      accPicker.style.boxShadow = "none";
      if (tertPicker) tertPicker.style.boxShadow = "none";

      if (PRESET_COLORS[preset]) {
        primPicker.value = PRESET_COLORS[preset].primary;
        primText.value = PRESET_COLORS[preset].primary;
        accPicker.value = PRESET_COLORS[preset].accent;
        accText.value = PRESET_COLORS[preset].accent;
        if (tertPicker && tertText) {
          tertPicker.value = PRESET_COLORS[preset].tertiary || "#ff0055";
          tertText.value = PRESET_COLORS[preset].tertiary || "#ff0055";
        }
      }
    }

    function syncGlobalColor(type, from) {
      const picker = document.getElementById(`picker-global-${type}`);
      const text = document.getElementById(`inp-global-${type}`);
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
          picker.value = text.value;
        }
      }
      const selPreset = document.getElementById("sel-global-preset");
      if (selPreset && selPreset.value !== "custom") {
        selPreset.value = "custom";
        onGlobalPresetChange();
      }
    }

    async function applyGlobalThemeToAllBlocks(force = false) {
      const gStyle = document.getElementById("sel-global-style").value;
      const gPreset = document.getElementById("sel-global-preset").value;
      const gMode = document.getElementById("sel-global-mode").value;
      const gPrim = document.getElementById("inp-global-primary").value.trim();
      const gAcc = document.getElementById("inp-global-accent").value.trim();
      const gTert = document.getElementById("inp-global-tertiary") ? document.getElementById("inp-global-tertiary").value.trim() : "";

      try {
        const resp = await fetch("/api/template/apply_global_theme", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            style: gStyle,
            preset: gPreset,
            mode: gMode,
            primary: gPrim,
            accent: gAcc,
            tertiary: gTert,
            force: !!force
          })
        });
        if (resp.ok) {
          const msg = force ? "✓ FORCE OVERRIDE APPLIED TO ALL BLOCKS" : "✓ SOFT APPLY COMPLETED (ACCENTS PRESERVED)";
          flashNotification(msg, "var(--studio-green)");
          await loadTemplateBlocks(currentEditingBlockId);
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to apply global theme: " + err);
        }
      } catch (e) {
        alert("Error applying global theme: " + e);
      }
    }

    // --- Block Level Theme & Preset / Custom Hex Interaction ---
    function onInheritThemeToggle() {
      const inherit = document.getElementById("chk-inherit-theme").checked;
      const overrideBox = document.getElementById("block-theme-override-controls");
      if (inherit) {
        overrideBox.style.display = "none";
      } else {
        overrideBox.style.display = "block";
      }
      debounceRender();
    }

    function onBlockPresetChange() {
      const preset = document.getElementById("sel-preset").value;
      if (PRESET_COLORS[preset]) {
        document.getElementById("picker-primary").value = PRESET_COLORS[preset].primary;
        document.getElementById("inp-primary").value = PRESET_COLORS[preset].primary;
        document.getElementById("picker-accent").value = PRESET_COLORS[preset].accent;
        document.getElementById("inp-accent").value = PRESET_COLORS[preset].accent;
        if (document.getElementById("picker-tertiary")) {
          document.getElementById("picker-tertiary").value = PRESET_COLORS[preset].tertiary || "#ff0055";
          document.getElementById("inp-tertiary").value = PRESET_COLORS[preset].tertiary || "#ff0055";
        }
      }
      debounceRender();
    }

    function onBlockColorModeToggle() {
      const isCustom = document.getElementById("rad-custom").checked;
      const row = document.getElementById("row-custom-colors");
      if (isCustom) {
        row.style.opacity = "1";
        row.style.pointerEvents = "auto";
      } else {
        row.style.opacity = "0.4";
        row.style.pointerEvents = "none";
        onBlockPresetChange();
      }
      debounceRender();
    }

    function syncBlockColor(type, from) {
      document.getElementById("rad-custom").checked = true;
      document.getElementById("row-custom-colors").style.opacity = "1";
      document.getElementById("row-custom-colors").style.pointerEvents = "auto";

      const picker = document.getElementById(`picker-${type}`);
      const text = document.getElementById(`inp-${type}`);
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
          picker.value = text.value;
        }
      }
      debounceRender();
    }

    const GITHUB_ALERT_COLORS = {
      NOTE: "#2f81f7",
      TIP: "#238636",
      IMPORTANT: "#8957e5",
      WARNING: "#d29922",
      CAUTION: "#f85149",
      CRITICAL: "#f85149",
      SUCCESS: "#238636",
      INFO: "#8957e5"
    };

    function onQuoteBadgeChange() {
      const badge = document.getElementById("sel-quote-badge").value.toUpperCase();
      const isCustom = document.getElementById("chk-quote-custom-badge").checked;
      if (!isCustom && GITHUB_ALERT_COLORS[badge]) {
        document.getElementById("picker-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
        document.getElementById("inp-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
      }
      debounceRender();
    }

    function onQuoteCustomBadgeToggle() {
      const isCustom = document.getElementById("chk-quote-custom-badge").checked;
      document.getElementById("quote-badge-color-group").style.display = isCustom ? "block" : "none";
      if (!isCustom) {
        const badge = document.getElementById("sel-quote-badge").value.toUpperCase();
        if (GITHUB_ALERT_COLORS[badge]) {
          document.getElementById("picker-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
          document.getElementById("inp-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
        }
      }
      updateContextualVisibility();
      debounceRender();
    }

    function syncQuoteBadgeColor(from) {
      const picker = document.getElementById("picker-quote-badge-color");
      const text = document.getElementById("inp-quote-badge-color");
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) picker.value = text.value;
      }
      debounceRender();
    }

    function onCalloutTypeChange() {
      const ctype = document.getElementById("sel-callout-type").value.toUpperCase();
      const isCustom = document.getElementById("chk-callout-custom-badge").checked;
      if (!isCustom && GITHUB_ALERT_COLORS[ctype]) {
        document.getElementById("picker-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
        document.getElementById("inp-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
      }
      debounceRender();
    }

    function onCalloutCustomBadgeToggle() {
      const isCustom = document.getElementById("chk-callout-custom-badge").checked;
      document.getElementById("callout-badge-color-group").style.display = isCustom ? "block" : "none";
      if (!isCustom) {
        const ctype = document.getElementById("sel-callout-type").value.toUpperCase();
        if (GITHUB_ALERT_COLORS[ctype]) {
          document.getElementById("picker-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
          document.getElementById("inp-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
        }
      }
      updateContextualVisibility();
      debounceRender();
    }

    function syncCalloutBadgeColor(from) {
      const picker = document.getElementById("picker-callout-badge-color");
      const text = document.getElementById("inp-callout-badge-color");
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) picker.value = text.value;
      }
      debounceRender();
    }

    function syncProgressInput(from) {
      const rng = document.getElementById("rng-progress-val");
      const num = document.getElementById("inp-progress-val");
      const lbl = document.getElementById("lbl-progress-num");
      if (from === "range") {
        num.value = rng.value;
      } else {
        rng.value = num.value;
      }
      lbl.innerText = `${rng.value}%`;
      debounceRender();
    }

    function addSampleMilestone() {
      const area = document.getElementById("inp-timeline-milestones");
      const count = area.value.split("\n").filter(l => l.trim()).length + 1;
      const sample = `milestone title="PHASE ${count}: MILESTONE" date="2026-Q${count % 4 + 1}" status="PLANNED" desc="Milestone deliverables and specification"`;
      if (area.value.trim()) {
        area.value = area.value.trim() + "\n" + sample;
      } else {
        area.value = sample;
      }
      debounceRender();
    }

    function updateContextualVisibility() {
      const btype = document.getElementById("sel-type").value;
      if (btype === "chip") {
        const ct = document.getElementById("sel-chip-type").value;
        const gh = document.getElementById("sel-chip-gh").value;
        const gDecay = document.getElementById("group-decay-dir");
        const rChipForm = document.getElementById("row-chip-form");
        if (gDecay) {
          const isDecay = (ct === "decay");
          gDecay.style.display = isDecay ? "flex" : "none";
          if (rChipForm) rChipForm.style.gridTemplateColumns = isDecay ? "1fr 1fr" : "1fr";
        }
        const gRepo = document.getElementById("group-chip-repo");
        const rChipGh = document.getElementById("row-chip-gh");
        if (gRepo) {
          const hasGh = (gh !== "");
          gRepo.style.display = hasGh ? "flex" : "none";
          if (rChipGh) rChipGh.style.gridTemplateColumns = hasGh ? "1fr 1fr" : "1fr";
        }
      } else if (btype === "header") {
        const isCompact = document.getElementById("chk-compact").checked;
        const gSpecs = document.getElementById("group-header-specs");
        if (gSpecs) {
          gSpecs.style.display = isCompact ? "none" : "flex";
        }
      } else if (btype === "frame") {
        const fType = document.getElementById("sel-frame-type").value;
        const isBottom = (fType === "bottom");
        const gTag = document.getElementById("group-frame-tag");
        const rCap = document.getElementById("row-frame-cap");
        const gTitle = document.getElementById("group-frame-title");
        const gTagUrl = document.getElementById("group-frame-tag-url");
        const rLinks = document.getElementById("row-frame-links");

        if (gTag) gTag.style.display = isBottom ? "none" : "flex";
        if (rCap) rCap.style.gridTemplateColumns = isBottom ? "1fr" : "1fr 1fr";
        if (gTitle) gTitle.style.display = isBottom ? "none" : "flex";
        if (gTagUrl) gTagUrl.style.display = isBottom ? "none" : "flex";
        if (rLinks) rLinks.style.gridTemplateColumns = isBottom ? "1fr" : "1fr 1fr";
      } else if (btype === "quote") {
        const isCustom = document.getElementById("chk-quote-custom-badge").checked;
        const rBadge = document.getElementById("row-quote-badge");
        if (rBadge) rBadge.style.gridTemplateColumns = isCustom ? "1fr 1fr" : "1fr";
      } else if (btype === "callout") {
        const isCustom = document.getElementById("chk-callout-custom-badge").checked;
        const rBadge = document.getElementById("row-callout-badge");
        if (rBadge) rBadge.style.gridTemplateColumns = isCustom ? "1fr 1fr" : "1fr";
      }
    }

    function selectBlockFromPreview(blockId, event) {
      if (event) event.stopPropagation();
      openInspector();
      switchEditorMode('edit');

      const foundIdx = templateBlocks.findIndex(b => b.id === blockId);
      if (foundIdx !== -1) {
        document.getElementById("sel-existing-block").value = foundIdx;
        onSelectExistingBlock();
      }
      highlightBlockInPreview(blockId);
    }

    function highlightBlockInPreview(blockId) {
      document.querySelectorAll(".pk-block-wrapper").forEach(el => {
        el.classList.remove("selected-block");
      });
      const el = document.getElementById(`pk-block-${blockId}`);
      if (el) {
        el.classList.add("selected-block");
      }
    }

    function openInsertAt(afterId, event) {
      if (event) event.stopPropagation();
      targetInsertAfterId = afterId;
      openInspector();
      switchEditorMode('insert');

      const heading = document.getElementById("lbl-inspector-heading");
      heading.innerText = (afterId === -1) ? "■ INSERT BLOCK AT TOP" : `■ INSERT BLOCK AFTER #${afterId}`;

      document.getElementById("sel-type").value = "header";
      onTypeChange(true);
      document.getElementById("inp-title").value = "NEW PIXEL SECTION";
      document.getElementById("inp-subtitle").value = "SECTION DESCRIPTION // SUBTITLE";
      document.getElementById("inp-tag").value = "STATUS_OK";
      renderCurrentBlock();
    }

    function cancelInsertMode() {
      switchEditorMode('edit');
      if (templateBlocks.length > 0) {
        onSelectExistingBlock();
      }
    }

    function switchEditorMode(mode) {
      editorMode = mode;
      const grpExisting = document.getElementById("group-existing-blocks");
      const editActions = document.getElementById("edit-mode-actions");
      const insertActions = document.getElementById("insert-mode-actions");
      const heading = document.getElementById("lbl-inspector-heading");
      const selType = document.getElementById("sel-type");
      const badgeLock = document.getElementById("badge-lock-type");

      if (mode === "edit") {
        grpExisting.style.display = "flex";
        editActions.style.display = "grid";
        insertActions.style.display = "none";
        heading.innerText = "■ EDIT BLOCK PARAMETERS";
        selType.disabled = true;
        selType.title = "Block type cannot be changed after creation. To use another type, insert a new block.";
        if (badgeLock) badgeLock.style.display = "inline-block";
      } else {
        grpExisting.style.display = "none";
        editActions.style.display = "none";
        insertActions.style.display = "grid";
        selType.disabled = false;
        selType.title = "";
        if (badgeLock) badgeLock.style.display = "none";
      }
    }

    async function loadTemplateBlocks(preferredId = null) {
      try {
        const resp = await fetch("/api/template/blocks");
        if (resp.ok) {
          const data = await resp.json();
          templateBlocks = data.blocks || [];
          const sel = document.getElementById("sel-existing-block");
          sel.innerHTML = "";

          const badge = document.getElementById("block-counter-badge");
          if (badge) badge.innerText = `${templateBlocks.length} blocks`;

          if (templateBlocks.length === 0) {
            sel.innerHTML = "<option value=''>No pixel-kit blocks found</option>";
            return;
          }

          templateBlocks.forEach((blk, idx) => {
            const opt = document.createElement("option");
            opt.value = idx;
            const btype = blk.type.toUpperCase();
            const title = blk.attrs.title || blk.attrs.text || blk.attrs.label || blk.attrs.status || (blk.type === "divider" ? "DIVIDER" : "");
            const displayTitle = title ? ` // ${title.slice(0, 30)}` : "";
            opt.innerText = `[#${blk.id}] ${btype}${displayTitle}`;
            sel.appendChild(opt);
          });

          let targetIndex = 0;
          if (preferredId !== null) {
            const foundIdx = templateBlocks.findIndex(b => b.id === preferredId);
            if (foundIdx !== -1) targetIndex = foundIdx;
          }
          sel.value = targetIndex;
          if (editorMode === "edit" && templateBlocks[targetIndex]) {
            onSelectExistingBlock();
          }
        }
      } catch (e) {
        console.error("Failed to load template blocks:", e);
      }
    }

    function onSelectExistingBlock() {
      const sel = document.getElementById("sel-existing-block");
      const idx = parseInt(sel.value, 10);
      if (isNaN(idx) || !templateBlocks[idx]) return;

      const blk = templateBlocks[idx];
      currentEditingBlockId = blk.id;
      currentEditingBlockOriginal = blk;

      const heading = document.getElementById("lbl-inspector-heading");
      heading.innerText = `■ EDIT BLOCK #${blk.id}: ${blk.type.toUpperCase()}`;

      const selType = document.getElementById("sel-type");
      selType.value = blk.type;
      onTypeChange(false);

      const attrs = blk.attrs || {};

      // Check whether this block uses custom theme overrides or inherits
      const hasCustomStyle = !!attrs.style;
      const hasCustomPreset = !!attrs.preset;
      const hasCustomColors = !!(attrs.primary || attrs.accent || attrs.tertiary);
      const isCustomOverride = hasCustomStyle || hasCustomPreset || hasCustomColors;

      const chkInherit = document.getElementById("chk-inherit-theme");
      chkInherit.checked = !isCustomOverride;
      onInheritThemeToggle();

      if (attrs.style) document.getElementById("sel-style").value = attrs.style;
      if (attrs.preset) document.getElementById("sel-preset").value = attrs.preset;
      if (attrs.mode) document.getElementById("sel-mode").value = attrs.mode;

      if (hasCustomColors) {
        document.getElementById("rad-custom").checked = true;
        document.getElementById("row-custom-colors").style.opacity = "1";
        document.getElementById("row-custom-colors").style.pointerEvents = "auto";
        if (attrs.primary) {
          document.getElementById("inp-primary").value = attrs.primary;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.primary)) document.getElementById("picker-primary").value = attrs.primary;
        }
        if (attrs.accent) {
          document.getElementById("inp-accent").value = attrs.accent;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.accent)) document.getElementById("picker-accent").value = attrs.accent;
        }
        if (attrs.tertiary) {
          document.getElementById("inp-tertiary").value = attrs.tertiary;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.tertiary)) document.getElementById("picker-tertiary").value = attrs.tertiary;
        }
      } else {
        document.getElementById("rad-preset").checked = true;
        document.getElementById("row-custom-colors").style.opacity = "0.4";
        document.getElementById("row-custom-colors").style.pointerEvents = "none";
        onBlockPresetChange();
      }

      // 1. Header
      document.getElementById("inp-title").value = attrs.title || attrs.text || attrs.label || attrs.status || "";
      document.getElementById("inp-subtitle").value = attrs.subtitle || attrs.sub || "";
      document.getElementById("inp-tag").value = attrs.tag || "";
      document.getElementById("inp-spec1").value = attrs.spec1 || "";
      document.getElementById("inp-spec2").value = attrs.spec2 || "";
      document.getElementById("inp-spec3").value = attrs.spec3 || "";
      document.getElementById("inp-tag-url").value = attrs.tag_url || attrs.tag_href || "";
      document.getElementById("inp-close-url").value = attrs.close_url || attrs.close_href || "";
      document.getElementById("chk-compact").checked = (attrs.compact === "true" || attrs.compact === "1");

      // 2. Timeline
      document.getElementById("inp-timeline-milestones").value = blk.body || "";

      // 3. Window
      document.getElementById("inp-window-title").value = attrs.title || "SYSTEM.WINDOW";
      document.getElementById("inp-window-tag").value = attrs.tag || "[SYS_LOG]";
      document.getElementById("inp-window-tag-url").value = attrs.tag_url || "";
      document.getElementById("inp-window-close-url").value = attrs.close_url || "";

      // 4. Terminal
      document.getElementById("inp-terminal-title").value = attrs.title || "HUD.TERMINAL";
      document.getElementById("sel-terminal-state").value = (attrs.state && attrs.state.toLowerCase() === "closed") ? "closed" : "open";

      // 5. Quote
      document.getElementById("inp-quote-title").value = attrs.title || "SPECIFICATION NOTICE";
      document.getElementById("inp-quote-sub").value = attrs.subtitle || "";
      const qBadgeVal = (attrs.badge || "NOTE").toUpperCase();
      document.getElementById("sel-quote-badge").value = qBadgeVal;
      if (attrs.badge_color) {
        document.getElementById("chk-quote-custom-badge").checked = true;
        document.getElementById("quote-badge-color-group").style.display = "block";
        document.getElementById("picker-quote-badge-color").value = attrs.badge_color;
        document.getElementById("inp-quote-badge-color").value = attrs.badge_color;
      } else {
        document.getElementById("chk-quote-custom-badge").checked = false;
        document.getElementById("quote-badge-color-group").style.display = "none";
        const defCol = GITHUB_ALERT_COLORS[qBadgeVal] || "#2f81f7";
        document.getElementById("picker-quote-badge-color").value = defCol;
        document.getElementById("inp-quote-badge-color").value = defCol;
      }

      // 6. Chip
      document.getElementById("inp-chip-text").value = attrs.text || attrs.title || "CHIP";
      if (attrs.type) document.getElementById("sel-chip-type").value = attrs.type;
      if (attrs.decay_dir) document.getElementById("sel-decay-dir").value = attrs.decay_dir;
      if (attrs.github) document.getElementById("sel-chip-gh").value = attrs.github;
      if (attrs.repo) document.getElementById("inp-chip-repo").value = attrs.repo;
      document.getElementById("inp-chip-width").value = attrs.width || "";
      document.getElementById("inp-chip-url").value = attrs.url || attrs.href || "";

      // 7. Metrics
      document.getElementById("inp-metrics-items").value = attrs.items || blk.body || "";
      document.getElementById("inp-metrics-label").value = attrs.label || attrs.title || "";
      document.getElementById("inp-metrics-val").value = attrs.value || attrs.subtitle || "";
      document.getElementById("inp-metrics-delta").value = attrs.delta || attrs.tag || "";
      document.getElementById("inp-metrics-status").value = attrs.status || "";

      // 8. Progress
      const pVal = parseInt(attrs.value || attrs.tag || "75", 10) || 75;
      document.getElementById("rng-progress-val").value = pVal;
      document.getElementById("inp-progress-val").value = pVal;
      document.getElementById("lbl-progress-num").innerText = `${pVal}%`;
      document.getElementById("inp-progress-label").value = attrs.label || attrs.title || "PROGRESS";
      document.getElementById("inp-progress-sub").value = attrs.sub || attrs.subtitle || "";

      // 9. Techstack
      document.getElementById("inp-techstack-items").value = attrs.items || attrs.subtitle || "python,cpp,docker,git";
      document.getElementById("inp-techstack-cols").value = attrs.columns || attrs.tag || "5";

      // 10. Callout
      const cTypeVal = (attrs.type || "note").toLowerCase();
      document.getElementById("sel-callout-type").value = cTypeVal;
      document.getElementById("inp-callout-title").value = attrs.title || "SYSTEM SPECIFICATION";
      document.getElementById("inp-callout-sub").value = attrs.subtitle || "";
      document.getElementById("chk-callout-quote").checked = (attrs.quote === "true" || attrs.quote === "1");
      if (attrs.badge_color) {
        document.getElementById("chk-callout-custom-badge").checked = true;
        document.getElementById("callout-badge-color-group").style.display = "block";
        document.getElementById("picker-callout-badge-color").value = attrs.badge_color;
        document.getElementById("inp-callout-badge-color").value = attrs.badge_color;
      } else {
        document.getElementById("chk-callout-custom-badge").checked = false;
        document.getElementById("callout-badge-color-group").style.display = "none";
        const defCol = GITHUB_ALERT_COLORS[cTypeVal.toUpperCase()] || "#2f81f7";
        document.getElementById("picker-callout-badge-color").value = defCol;
        document.getElementById("inp-callout-badge-color").value = defCol;
      }

      // 11. Frame
      if (attrs.type) document.getElementById("sel-frame-type").value = attrs.type;
      document.getElementById("inp-frame-title").value = attrs.title || "SYSTEM.CORE";
      document.getElementById("inp-frame-tag").value = attrs.tag || "[OPEN_HUD]";
      document.getElementById("inp-frame-tag-url").value = attrs.tag_url || "";
      document.getElementById("inp-frame-close-url").value = attrs.close_url || "";

      // 13. Splitter
      document.getElementById("inp-splitter-label").value = attrs.label || attrs.title || "[SUB_MODULE]";

      // 14. Footer
      document.getElementById("inp-footer-status").value = attrs.status || attrs.title || "SESSION_ACTIVE // STANDBY";
      document.getElementById("inp-footer-nav").value = attrs.nav || attrs.tag || "▲ RETURN TO TOP";
      document.getElementById("inp-footer-sub").value = attrs.sub || attrs.subtitle || "";

      // 15. Social
      document.getElementById("inp-social-title").value = attrs.title || "PIXEL README KIT";
      document.getElementById("inp-social-sub").value = attrs.subtitle || "";
      document.getElementById("inp-social-repo").value = attrs.repo || "Kazinagg/pixel-readme-kit";
      document.getElementById("inp-social-tags").value = attrs.tags || attrs.tag || "PYTHON,SVG";

      // Generic container body
      document.getElementById("inp-body").value = blk.body || "";

      highlightBlockInPreview(blk.id);
      updateContextualVisibility();
      renderCurrentBlock();
    }

    function onTypeChange(resetValues = true) {
      const type = document.getElementById("sel-type").value;

      const sections = {
        header: document.getElementById("section-header"),
        timeline: document.getElementById("section-timeline"),
        window: document.getElementById("section-window"),
        terminal: document.getElementById("section-terminal"),
        quote: document.getElementById("section-quote"),
        chip: document.getElementById("section-chip"),
        metrics: document.getElementById("section-metrics"),
        progress: document.getElementById("section-progress"),
        techstack: document.getElementById("section-techstack"),
        callout: document.getElementById("section-callout"),
        frame: document.getElementById("section-frame"),
        divider: document.getElementById("section-divider"),
        splitter: document.getElementById("section-splitter"),
        footer: document.getElementById("section-footer"),
        social: document.getElementById("section-social"),
        body: document.getElementById("section-body")
      };

      for (let k in sections) {
        if (sections[k]) sections[k].style.display = "none";
      }

      if (sections[type]) {
        sections[type].style.display = "flex";
      }

      // Container markdown body section
      if (type === "window" || type === "terminal" || type === "quote") {
        sections.body.style.display = "flex";
      }

      updateCharCounters();
      updateContextualVisibility();
      renderCurrentBlock();
    }

    function generateDirectiveCode() {
      const btype = document.getElementById("sel-type").value;
      const inheritTheme = document.getElementById("chk-inherit-theme").checked;

      let style = document.getElementById("sel-global-style").value;
      let preset = document.getElementById("sel-global-preset").value;
      let mode = document.getElementById("sel-global-mode").value;
      let isCustomColors = false;
      let prim = "";
      let acc = "";
      let tert = "";

      if (!inheritTheme) {
        style = document.getElementById("sel-style").value;
        preset = document.getElementById("sel-preset").value;
        mode = document.getElementById("sel-mode").value;
        isCustomColors = document.getElementById("rad-custom").checked;
        if (isCustomColors) {
          prim = document.getElementById("inp-primary").value.trim();
          acc = document.getElementById("inp-accent").value.trim();
          tert = document.getElementById("inp-tertiary") ? document.getElementById("inp-tertiary").value.trim() : "";
        }
      }

      const origAttrs = (currentEditingBlockOriginal && currentEditingBlockOriginal.attrs) ? currentEditingBlockOriginal.attrs : {};

      let opening = `<!-- pixel-kit:${btype}`;
      if (!inheritTheme) {
        if (style) opening += ` style="${style}"`;
        if (preset) opening += ` preset="${preset}"`;
        if (mode && mode !== "auto") opening += ` mode="${mode}"`;
        if (isCustomColors && prim) opening += ` primary="${prim}"`;
        if (isCustomColors && acc) opening += ` accent="${acc}"`;
        if (isCustomColors && tert) opening += ` tertiary="${tert}"`;
      }

      let innerBody = "";

      if (btype === "header") {
        const title = document.getElementById("inp-title").value.trim();
        const sub = document.getElementById("inp-subtitle").value.trim();
        const tag = document.getElementById("inp-tag").value.trim();
        const s1 = document.getElementById("inp-spec1").value.trim();
        const s2 = document.getElementById("inp-spec2").value.trim();
        const s3 = document.getElementById("inp-spec3").value.trim();
        const tUrl = document.getElementById("inp-tag-url").value.trim();
        const cUrl = document.getElementById("inp-close-url").value.trim();
        const compact = document.getElementById("chk-compact").checked;

        if (title) opening += ` title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (tag) opening += ` tag="${tag}"`;
        if (!compact && s1) opening += ` spec1="${s1}"`;
        if (!compact && s2) opening += ` spec2="${s2}"`;
        if (!compact && s3) opening += ` spec3="${s3}"`;
        if (tUrl) opening += ` tag_url="${tUrl}"`;
        if (cUrl) opening += ` close_url="${cUrl}"`;
        if (compact) opening += ` compact="true"`;
      } else if (btype === "timeline") {
        innerBody = document.getElementById("inp-timeline-milestones").value.trim();
      } else if (btype === "window") {
        const title = document.getElementById("inp-window-title").value.trim();
        const tag = document.getElementById("inp-window-tag").value.trim();
        const tUrl = document.getElementById("inp-window-tag-url").value.trim();
        const cUrl = document.getElementById("inp-window-close-url").value.trim();
        if (title) opening += ` title="${title}"`;
        if (tag) opening += ` tag="${tag}"`;
        if (tUrl) opening += ` tag_url="${tUrl}"`;
        if (cUrl) opening += ` close_url="${cUrl}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "terminal") {
        const title = document.getElementById("inp-terminal-title").value.trim();
        const state = document.getElementById("sel-terminal-state").value;
        if (title) opening += ` title="${title}"`;
        if (state) opening += ` state="${state}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "quote") {
        const title = document.getElementById("inp-quote-title").value.trim();
        const sub = document.getElementById("inp-quote-sub").value.trim();
        const badge = document.getElementById("sel-quote-badge").value;
        const isCustomBadge = document.getElementById("chk-quote-custom-badge").checked;
        const bCol = document.getElementById("inp-quote-badge-color").value.trim();
        if (title) opening += ` title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (badge) opening += ` badge="${badge}"`;
        if (isCustomBadge && bCol) opening += ` badge_color="${bCol}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "chip") {
        const text = document.getElementById("inp-chip-text").value.trim();
        const ctype = document.getElementById("sel-chip-type").value;
        const decay = document.getElementById("sel-decay-dir").value;
        const gh = document.getElementById("sel-chip-gh").value;
        const repo = document.getElementById("inp-chip-repo").value.trim();
        const w = document.getElementById("inp-chip-width").value.trim();
        const url = document.getElementById("inp-chip-url").value.trim();

        if (text) opening += ` text="${text}"`;
        if (ctype && ctype !== "closed") opening += ` type="${ctype}"`;
        if (ctype === "decay" && decay && decay !== "right") opening += ` decay_dir="${decay}"`;
        if (gh) opening += ` github="${gh}"`;
        if (gh && repo) opening += ` repo="${repo}"`;
        if (w) opening += ` width="${w}"`;
        if (url) opening += ` url="${url}"`;
      } else if (btype === "metrics") {
        const items = document.getElementById("inp-metrics-items").value.trim();
        const lbl = document.getElementById("inp-metrics-label").value.trim();
        const val = document.getElementById("inp-metrics-val").value.trim();
        const delta = document.getElementById("inp-metrics-delta").value.trim();
        const st = document.getElementById("inp-metrics-status").value.trim();

        if (items.includes("\n") || items.startsWith("-")) {
          innerBody = items;
        } else if (items) {
          opening += ` items="${items}"`;
        } else {
          if (lbl) opening += ` label="${lbl}"`;
          if (val) opening += ` value="${val}"`;
          if (delta) opening += ` delta="${delta}"`;
          if (st) opening += ` status="${st}"`;
        }
      } else if (btype === "progress") {
        const val = document.getElementById("inp-progress-val").value;
        const lbl = document.getElementById("inp-progress-label").value.trim();
        const sub = document.getElementById("inp-progress-sub").value.trim();
        opening += ` value="${val}" label="${lbl}"`;
        if (sub) opening += ` sub="${sub}"`;
      } else if (btype === "techstack") {
        const items = document.getElementById("inp-techstack-items").value.trim();
        const cols = document.getElementById("inp-techstack-cols").value.trim();
        opening += ` items="${items}" columns="${cols}"`;
      } else if (btype === "callout") {
        const ctype = document.getElementById("sel-callout-type").value;
        const title = document.getElementById("inp-callout-title").value.trim();
        const sub = document.getElementById("inp-callout-sub").value.trim();
        const quote = document.getElementById("chk-callout-quote").checked;
        const isCustomBadge = document.getElementById("chk-callout-custom-badge").checked;
        const bCol = document.getElementById("inp-callout-badge-color").value.trim();
        opening += ` type="${ctype}" title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (quote) opening += ` quote="true"`;
        if (isCustomBadge && bCol) opening += ` badge_color="${bCol}"`;
      } else if (btype === "frame") {
        const ftype = document.getElementById("sel-frame-type").value;
        const title = document.getElementById("inp-frame-title").value.trim();
        const tag = document.getElementById("inp-frame-tag").value.trim();
        const tUrl = document.getElementById("inp-frame-tag-url").value.trim();
        const cUrl = document.getElementById("inp-frame-close-url").value.trim();
        if (ftype === "bottom") {
          opening += ` type="bottom"`;
          if (cUrl) opening += ` close_url="${cUrl}"`;
        } else {
          opening += ` type="top" title="${title}" tag="${tag}"`;
          if (tUrl) opening += ` tag_url="${tUrl}"`;
          if (cUrl) opening += ` close_url="${cUrl}"`;
        }
      } else if (btype === "splitter") {
        const lbl = document.getElementById("inp-splitter-label").value.trim();
        opening += ` label="${lbl}"`;
      } else if (btype === "footer") {
        const st = document.getElementById("inp-footer-status").value.trim();
        const nav = document.getElementById("inp-footer-nav").value.trim();
        const sub = document.getElementById("inp-footer-sub").value.trim();
        opening += ` status="${st}" nav="${nav}"`;
        if (sub) opening += ` sub="${sub}"`;
      } else if (btype === "social") {
        const title = document.getElementById("inp-social-title").value.trim();
        const sub = document.getElementById("inp-social-sub").value.trim();
        const repo = document.getElementById("inp-social-repo").value.trim();
        const tags = document.getElementById("inp-social-tags").value.trim();
        opening += ` title="${title}" subtitle="${sub}" repo="${repo}" tags="${tags}"`;
      }

      if (origAttrs.out) opening += ` out="${origAttrs.out}"`;
      opening += ` -->`;

      const isContainerType = (btype === "window" || btype === "terminal" || btype === "quote" || btype === "timeline" || (btype === "metrics" && innerBody));
      if (isContainerType) {
        return `${opening}\n${innerBody}\n<!-- /pixel-kit:${btype} -->`;
      }
      return opening;
    }

    function onRawDirectiveManualEdit() {
      if (isParsingRaw) return;
      const raw = document.getElementById("txt-raw-directive").value;
      const m = raw.match(/<!--\s*pixel-kit:([a-zA-Z0-9_\-]+)\b([\s\S]*?)-->/i);
      if (!m) return;

      isParsingRaw = true;
      try {
        const btype = m[1].toLowerCase();
        const attrStr = m[2];
        const selType = document.getElementById("sel-type");
        if (editorMode === "insert" && selType.querySelector(`option[value="${btype}"]`)) {
          selType.value = btype;
          onTypeChange(false);
        }

        const attrRegex = /([\w\-]+)=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g;
        let match;
        const parsed = {};
        while ((match = attrRegex.exec(attrStr)) !== null) {
          const key = match[1].toLowerCase();
          const val = match[2] !== undefined ? match[2] : (match[3] !== undefined ? match[3] : match[4]);
          parsed[key] = val;
        }

        const hasCustom = parsed.style || parsed.preset || parsed.primary || parsed.accent;
        document.getElementById("chk-inherit-theme").checked = !hasCustom;
        onInheritThemeToggle();

        if (parsed.style) document.getElementById("sel-style").value = parsed.style;
        if (parsed.preset) document.getElementById("sel-preset").value = parsed.preset;
        if (parsed.mode) document.getElementById("sel-mode").value = parsed.mode;
        if (parsed.primary || parsed.accent) {
          document.getElementById("rad-custom").checked = true;
          document.getElementById("row-custom-colors").style.opacity = "1";
          document.getElementById("row-custom-colors").style.pointerEvents = "auto";
          if (parsed.primary) {
            document.getElementById("inp-primary").value = parsed.primary;
            if (/^#[0-9A-Fa-f]{6}$/.test(parsed.primary)) document.getElementById("picker-primary").value = parsed.primary;
          }
          if (parsed.accent) {
            document.getElementById("inp-accent").value = parsed.accent;
            if (/^#[0-9A-Fa-f]{6}$/.test(parsed.accent)) document.getElementById("picker-accent").value = parsed.accent;
          }
        }

        if (parsed.title) document.getElementById("inp-title").value = parsed.title;
        if (parsed.subtitle) document.getElementById("inp-subtitle").value = parsed.subtitle;
        if (parsed.tag) document.getElementById("inp-tag").value = parsed.tag;
        if (parsed.spec1) document.getElementById("inp-spec1").value = parsed.spec1;
        if (parsed.spec2) document.getElementById("inp-spec2").value = parsed.spec2;
        if (parsed.spec3) document.getElementById("inp-spec3").value = parsed.spec3;
        if (parsed.compact !== undefined) document.getElementById("chk-compact").checked = (parsed.compact === "true" || parsed.compact === "1");

        updateCharCounters();
        updateContextualVisibility();
        renderCurrentBlock(false);
      } finally {
        isParsingRaw = false;
      }
    }

    function updateCharCounters() {
      const title = document.getElementById("inp-title").value || "";
      const sub = document.getElementById("inp-subtitle").value || "";
      const s1 = document.getElementById("inp-spec1").value || "";
      const s2 = document.getElementById("inp-spec2").value || "";
      const s3 = document.getElementById("inp-spec3").value || "";

      const bTitle = document.getElementById("badge-title-budget");
      const bSub = document.getElementById("badge-sub-budget");
      const bS1 = document.getElementById("badge-spec1-budget");
      const bS2 = document.getElementById("badge-spec2-budget");
      const bS3 = document.getElementById("badge-spec3-budget");

      if (bTitle) {
        const len = title.length;
        bTitle.innerText = `${len} chars`;
        bTitle.className = "char-badge " + (len <= 14 ? "badge-optimal" : (len <= 20 ? "badge-warning" : "badge-danger"));
      }
      if (bSub) {
        const len = sub.length;
        bSub.innerText = `${len} chars`;
        bSub.className = "char-badge " + (len <= 45 ? "badge-optimal" : "badge-warning");
      }
      if (bS1) {
        const len = s1.length;
        bS1.innerText = `${len} chars`;
        bS1.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
      if (bS2) {
        const len = s2.length;
        bS2.innerText = `${len} chars`;
        bS2.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
      if (bS3) {
        const len = s3.length;
        bS3.innerText = `${len} chars`;
        bS3.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
    }

    function debounceRender() {
      updateCharCounters();
      if (!isParsingRaw) {
        const rawCode = generateDirectiveCode();
        document.getElementById("txt-raw-directive").value = rawCode;
      }
      clearTimeout(renderTimer);
      renderTimer = setTimeout(renderCurrentBlock, 60);
    }

    async function renderCurrentBlock(updateRaw = true) {
      const t0 = performance.now();
      const btype = document.getElementById("sel-type").value;
      const inheritTheme = document.getElementById("chk-inherit-theme").checked;

      let style = document.getElementById("sel-global-style").value;
      let preset = document.getElementById("sel-global-preset").value;
      let mode = document.getElementById("sel-global-mode").value;
      let prim = "";
      let acc = "";
      let tert = "";

      if (!inheritTheme) {
        style = document.getElementById("sel-style").value;
        preset = document.getElementById("sel-preset").value;
        mode = document.getElementById("sel-mode").value;
        if (document.getElementById("rad-custom").checked) {
          prim = document.getElementById("inp-primary").value.trim();
          acc = document.getElementById("inp-accent").value.trim();
          tert = document.getElementById("inp-tertiary") ? document.getElementById("inp-tertiary").value.trim() : "";
        }
      }

      // If mode is auto, force the current preview theme mode so the user sees the SVG in chosen theme
      let effectiveRenderMode = mode;
      if (mode === "auto") {
        effectiveRenderMode = activePreviewTheme;
      }

      if (updateRaw && !isParsingRaw) {
        const rawCode = generateDirectiveCode();
        document.getElementById("txt-raw-directive").value = rawCode;
      }

      const params = new URLSearchParams({
        block_type: btype,
        style: style,
        preset: preset,
        mode: effectiveRenderMode
      });
      if (prim) params.set("primary", prim);
      if (acc) params.set("accent", acc);
      if (tert) params.set("tertiary", tert);

      if (btype === "header") {
        params.set("title", document.getElementById("inp-title").value);
        params.set("subtitle", document.getElementById("inp-subtitle").value);
        params.set("tag", document.getElementById("inp-tag").value);
        params.set("spec1", document.getElementById("inp-spec1").value);
        params.set("spec2", document.getElementById("inp-spec2").value);
        params.set("spec3", document.getElementById("inp-spec3").value);
        params.set("tag_url", document.getElementById("inp-tag-url").value);
        params.set("close_url", document.getElementById("inp-close-url").value);
        params.set("compact", document.getElementById("chk-compact").checked ? "true" : "false");
      } else if (btype === "timeline") {
        params.set("body", document.getElementById("inp-timeline-milestones").value);
      } else if (btype === "window") {
        params.set("title", document.getElementById("inp-window-title").value);
        params.set("tag", document.getElementById("inp-window-tag").value);
      } else if (btype === "terminal") {
        params.set("title", document.getElementById("inp-terminal-title").value);
      } else if (btype === "quote") {
        params.set("title", document.getElementById("inp-quote-title").value);
        params.set("subtitle", document.getElementById("inp-quote-sub").value);
        const qBadge = document.getElementById("sel-quote-badge").value;
        params.set("badge", qBadge);
        if (document.getElementById("chk-quote-custom-badge").checked) {
          const bCol = document.getElementById("inp-quote-badge-color").value.trim();
          if (bCol) params.set("badge_color", bCol);
        } else if (GITHUB_ALERT_COLORS[qBadge.toUpperCase()]) {
          params.set("badge_color", GITHUB_ALERT_COLORS[qBadge.toUpperCase()]);
        }
      } else if (btype === "chip") {
        params.set("title", document.getElementById("inp-chip-text").value);
        params.set("type", document.getElementById("sel-chip-type").value);
        params.set("decay_dir", document.getElementById("sel-decay-dir").value);
        params.set("github", document.getElementById("sel-chip-gh").value);
        params.set("repo", document.getElementById("inp-chip-repo").value);
        params.set("width", document.getElementById("inp-chip-width").value);
      } else if (btype === "metrics") {
        params.set("items", document.getElementById("inp-metrics-items").value);
        params.set("title", document.getElementById("inp-metrics-label").value);
        params.set("subtitle", document.getElementById("inp-metrics-val").value);
        params.set("delta", document.getElementById("inp-metrics-delta").value);
        params.set("status", document.getElementById("inp-metrics-status").value);
      } else if (btype === "progress") {
        params.set("value", document.getElementById("inp-progress-val").value);
        params.set("title", document.getElementById("inp-progress-label").value);
        params.set("sub", document.getElementById("inp-progress-sub").value);
      } else if (btype === "techstack") {
        params.set("items", document.getElementById("inp-techstack-items").value);
        params.set("columns", document.getElementById("inp-techstack-cols").value);
      } else if (btype === "callout") {
        const cType = document.getElementById("sel-callout-type").value;
        params.set("type", cType);
        params.set("title", document.getElementById("inp-callout-title").value);
        params.set("subtitle", document.getElementById("inp-callout-sub").value);
        params.set("quote", document.getElementById("chk-callout-quote").checked ? "true" : "false");
        if (document.getElementById("chk-callout-custom-badge").checked) {
          const bCol = document.getElementById("inp-callout-badge-color").value.trim();
          if (bCol) params.set("badge_color", bCol);
        } else if (GITHUB_ALERT_COLORS[cType.toUpperCase()]) {
          params.set("badge_color", GITHUB_ALERT_COLORS[cType.toUpperCase()]);
        }
      } else if (btype === "frame") {
        params.set("type", document.getElementById("sel-frame-type").value);
        params.set("title", document.getElementById("inp-frame-title").value);
        params.set("tag", document.getElementById("inp-frame-tag").value);
        params.set("tag_url", document.getElementById("inp-frame-tag-url").value);
        params.set("close_url", document.getElementById("inp-frame-close-url").value);
      } else if (btype === "splitter") {
        params.set("title", document.getElementById("inp-splitter-label").value);
      } else if (btype === "footer") {
        params.set("status", document.getElementById("inp-footer-status").value);
        params.set("nav", document.getElementById("inp-footer-nav").value);
        params.set("sub", document.getElementById("inp-footer-sub").value);
      } else if (btype === "social") {
        params.set("title", document.getElementById("inp-social-title").value);
        params.set("subtitle", document.getElementById("inp-social-sub").value);
        params.set("repo", document.getElementById("inp-social-repo").value);
        params.set("tags", document.getElementById("inp-social-tags").value);
      }

      try {
        const resp = await fetch(`/api/render?${params.toString()}`);
        if (resp.ok) {
          const svgText = await resp.text();
          const mount = document.getElementById("svg-render-mount");
          // Use Shadow DOM to prevent any <style>:root in SVG from leaking into Studio UI
          if (!mount.shadowRoot) {
            mount.attachShadow({ mode: "open" });
          }
          mount.shadowRoot.innerHTML = svgText;
          const dt = Math.round(performance.now() - t0);
          document.getElementById("render-latency").innerText = `${dt}ms`;
        }
      } catch (err) {
        console.error("Render block error:", err);
      }
    }

    async function saveExistingBlockChanges() {
      if (currentEditingBlockId === null) {
        alert("No block selected to update.");
        return;
      }
      const newRaw = document.getElementById("txt-raw-directive").value.trim() || generateDirectiveCode();
      try {
        const resp = await fetch("/api/template/update_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: currentEditingBlockId,
            directive_raw: newRaw
          })
        });
        if (resp.ok) {
          flashNotification("✓ BLOCK SAVED & RECOMPILED", "var(--studio-green)");
          const keepId = currentEditingBlockId;
          await loadTemplateBlocks(keepId);
          await loadCompiledPreview();
          highlightBlockInPreview(keepId);
        } else {
          const err = await resp.text();
          alert("Failed to update block: " + err);
        }
      } catch (e) {
        alert("Error saving block: " + e);
      }
    }

    async function executeInsertBlock() {
      const newRaw = document.getElementById("txt-raw-directive").value.trim() || generateDirectiveCode();
      try {
        const resp = await fetch("/api/template/insert_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            after_id: targetInsertAfterId,
            directive_raw: newRaw
          })
        });
        if (resp.ok) {
          flashNotification("✓ NEW BLOCK INSERTED", "var(--studio-green)");
          switchEditorMode('edit');
          await loadTemplateBlocks();
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to insert block: " + err);
        }
      } catch (e) {
        alert("Error inserting block: " + e);
      }
    }

    function confirmDeleteBlock(blockId, event) {
      if (event) event.stopPropagation();
      currentEditingBlockId = blockId;
      deleteExistingBlock();
    }

    async function deleteExistingBlock() {
      if (currentEditingBlockId === null) return;
      if (!confirm(`Delete block #${currentEditingBlockId} from template?`)) return;
      try {
        const resp = await fetch("/api/template/delete_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: currentEditingBlockId })
        });
        if (resp.ok) {
          flashNotification("✓ BLOCK REMOVED", "var(--studio-amber)");
          currentEditingBlockId = null;
          currentEditingBlockOriginal = null;
          await loadTemplateBlocks(0);
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to delete block: " + err);
        }
      } catch (e) {
        alert("Error deleting block: " + e);
      }
    }

    function copyDirective() {
      const code = document.getElementById("txt-raw-directive").value;
      navigator.clipboard.writeText(code).then(() => {
        flashNotification("✓ COPIED TO CLIPBOARD", "var(--studio-cyan)");
      });
    }

    function flashNotification(text, color) {
      const s = document.getElementById("sse-status");
      if (s) {
        const oldText = s.innerText;
        const oldColor = s.style.color;
        s.innerText = text;
        s.style.color = color;
        setTimeout(() => {
          s.innerText = oldText;
          s.style.color = oldColor;
        }, 2500);
      }
    }

    async function pushReadmeToGit() {
      const btn = document.getElementById("btn-git-push");
      if (!btn) return;
      const originalText = btn.innerText;
      btn.disabled = true;
      btn.innerText = "[ PUSHING... ]";
      flashNotification("SYNCING README & PUSHING TO GIT...", "var(--studio-amber)");

      try {
        const resp = await fetch("/api/git/push_readme", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();
        if (resp.ok && data.ok) {
          flashNotification(data.committed ? "✓ README PUSHED TO GITHUB" : "✓ ALREADY UP TO DATE IN GIT", "var(--studio-green)");
          await loadCompiledPreview();
        } else {
          flashNotification("✗ PUSH FAILED: " + (data.error || "Unknown error"), "var(--studio-danger)");
          alert("Git Push Error: " + (data.error || "Failed to push to Git"));
        }
      } catch (err) {
        flashNotification("✗ NETWORK ERROR DURING PUSH", "var(--studio-danger)");
        alert("Network / Server error: " + err);
      } finally {
        btn.disabled = false;
        btn.innerText = originalText;
      }
    }

    async function loadCompiledPreview() {
      try {
        const resp = await fetch(`/api/preview?theme=${activePreviewTheme}&t=${Date.now()}`, { cache: "no-store" });
        if (resp.ok) {
          const data = await resp.json();
          const bustTimestamp = Date.now();
          const applyTheme = (htmlStr) => (htmlStr || "").replace(
            /(<img\b[^>]*?\bsrc=")([^"]+)(\")/gi,
            function(match, p1, p2, p3) {
              const cleanUrl = p2.split("?")[0];
              return `${p1}${cleanUrl}?theme=${activePreviewTheme}&t=${bustTimestamp}${p3}`;
            }
          );
          cachedEditHtml = applyTheme(data.html || "");
          cachedViewHtml = applyTheme(data.view_html || data.html || "");

          const previewArea = document.getElementById("readme-preview-content");
          if (previewArea) {
            if (currentStudioMode === "view") {
              previewArea.innerHTML = cachedViewHtml;
            } else {
              previewArea.innerHTML = cachedEditHtml;
            }
          }
          document.getElementById("template-filename").innerText = data.filename || "README.template.md";
          if (data.lines) document.getElementById("gh-stats-lines").innerText = `${data.lines} lines`;
          if (data.bytes) {
            const kb = (data.bytes / 1024).toFixed(1);
            document.getElementById("gh-stats-bytes").innerText = `${kb} KB`;
          }
          if (currentStudioMode !== "view" && currentEditingBlockId !== null) {
            highlightBlockInPreview(currentEditingBlockId);
          }
        }
      } catch (e) {
        console.error("Load preview error:", e);
      }
    }

    function attachPreviewClickInterceptor() {
      const container = document.getElementById("readme-preview-content");
      if (!container) return;
      container.addEventListener("click", function(e) {
        if (currentStudioMode === "view") return;
        const link = e.target.closest("a");
        if (link && !e.target.closest(".pk-block-hud-bar")) {
          e.preventDefault();
          e.stopPropagation();
        }
        const wrapper = e.target.closest(".pk-block-wrapper");
        if (wrapper && !e.target.closest(".pk-hud-actions")) {
          const blkId = parseInt(wrapper.getAttribute("data-pk-id"), 10);
          if (!isNaN(blkId)) {
            selectBlockFromPreview(blkId, e);
          }
        }
      });
    }

    function initSSE() {
      if (sseSource) sseSource.close();
      sseSource = new EventSource("/events");
      sseSource.addEventListener("reload", () => {
        loadTemplateBlocks(currentEditingBlockId);
        loadCompiledPreview();
      });
      sseSource.onopen = () => {
        const el = document.getElementById("sse-status");
        if (el) { el.innerText = "HUD STUDIO SYNC: ONLINE"; el.style.color = "var(--studio-green)"; }
      };
      sseSource.onerror = () => {
        const el = document.getElementById("sse-status");
        if (el) { el.innerText = "HUD STUDIO SYNC: RECONNECTING..."; el.style.color = "var(--studio-amber)"; }
      };
    }

    // Global Keyboard Shortcuts
    document.addEventListener("keydown", function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        if (editorMode === "edit") {
          saveExistingBlockChanges();
        } else {
          executeInsertBlock();
        }
      }
    });

    window.addEventListener("DOMContentLoaded", () => {
      try {
        const savedMode = localStorage.getItem("pk_studio_mode");
        if (savedMode === "view") {
          setStudioMode("view");
        }
        const savedTheme = localStorage.getItem("pk_preview_theme");
        if (savedTheme === "light") {
          switchPreviewTheme("light");
        }
      } catch (_) {}
      onGlobalPresetChange();
      onBlockPresetChange();
      loadTemplateBlocks();
      loadCompiledPreview();
      attachPreviewClickInterceptor();
      initSSE();
    });
  </script>
</body>
</html>
"""

# ==============================================================================
# HTTP REQUEST HANDLER
# ==============================================================================

class StudioRequestHandler(SimpleHTTPRequestHandler):
    """Handles HUD Studio API and static asset requests."""

    template_file = "README.template.md"
    output_file = "README.md"
    assets_dir = "assets/generated"
    subscribers = set()
    subscribers_lock = threading.Lock()

    def end_headers(self):
        """Ensure no browser or proxy caching for any studio assets or endpoints."""
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        # 1. Main Studio UI
        if path == "/" or path == "/studio":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
            self.end_headers()
            self.wfile.write(STUDIO_HTML.encode("utf-8"))
            return

        # 2. Server-Sent Events (SSE) Live Reload channel
        if path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            with self.subscribers_lock:
                self.subscribers.add(self)

            try:
                self.wfile.write(b"data: {\"status\": \"connected\"}\n\n")
                self.wfile.flush()
                while True:
                    time.sleep(1.0)
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
            except (ConnectionError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                pass
            finally:
                with self.subscribers_lock:
                    self.subscribers.discard(self)
            return

        # 3. Dynamic SVG Render API (/api/render)
        if path == "/api/render":
            btype = query.get("block_type", ["header"])[0].lower()
            style = query.get("style", ["cyberpunk"])[0]
            mode = query.get("mode", ["auto"])[0]
            preset = query.get("preset", [None])[0] or None
            primary = query.get("primary", [None])[0] or None
            accent = query.get("accent", [None])[0] or None
            tertiary = query.get("tertiary", [None])[0] or None

            title = query.get("title", [None])[0]
            subtitle = query.get("subtitle", [None])[0]
            tag = query.get("tag", [None])[0]
            compact = query.get("compact", ["false"])[0].lower() in ("true", "1", "yes")

            spec1 = query.get("spec1", [None])[0] or None
            spec2 = query.get("spec2", [None])[0] or None
            spec3 = query.get("spec3", [None])[0] or None
            specs = query.get("specs", [None])[0] or None
            tag_url = query.get("tag_url", [None])[0] or None
            close_url = query.get("close_url", [None])[0] or None

            chip_type = query.get("chip_type", [None])[0] or query.get("type", ["closed"])[0]
            decay_dir = query.get("decay_dir", [None])[0] or query.get("direction", ["right"])[0]
            gh_stat = query.get("github", [None])[0] or query.get("gh", [None])[0]
            repo = query.get("repo", [None])[0]
            width_str = query.get("width", [None])[0]
            width_val = int(width_str) if width_str and width_str.isdigit() else None

            items = query.get("items", [None])[0]
            body = query.get("body", [None])[0]
            delta = query.get("delta", [None])[0]
            status = query.get("status", [None])[0]
            trend = query.get("trend", [None])[0]

            value_str = query.get("value", [None])[0] or tag
            cols_str = query.get("columns", [None])[0]
            cols_val = int(cols_str) if cols_str and cols_str.isdigit() else (int(tag) if tag and tag.isdigit() else 5)

            callout_type = query.get("callout_type", [None])[0] or query.get("type", ["note"])[0]
            badge_color = query.get("badge_color", [None])[0] or None
            is_quote = query.get("quote", ["false"])[0].lower() in ("true", "1", "yes")
            frame_type = query.get("frame_type", [None])[0] or query.get("type", ["top"])[0]
            badge = query.get("badge", ["NOTE"])[0]
            label = query.get("label", [None])[0] or title or "[SUB_MODULE]"
            sub_text = query.get("sub", [None])[0] or subtitle
            nav_text = query.get("nav", [None])[0] or tag or "RETURN TO TOP"
            tags_str = query.get("tags", [None])[0] or tag or "PYTHON,SVG"

            try:
                if btype == "header":
                    svg = generate_header(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent, tertiary=tertiary,
                        title=title or "PIXEL-KIT", subtitle=subtitle or "TRANSLUCENT HUD SYSTEM",
                        tag=tag or "SYSTEM_ACTIVE", spec1=spec1, spec2=spec2, spec3=spec3, specs=specs,
                        tag_url=tag_url, close_url=close_url, compact=compact
                    )
                elif btype == "footer":
                    svg = generate_footer(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent, tertiary=tertiary,
                        status=status or title or "SESSION_ACTIVE // STANDBY",
                        nav_text=nav_text, sub_text=sub_text
                    )
                elif btype in ("callout", "quote"):
                    q_badge = badge if btype == "quote" else callout_type
                    svg = generate_callout(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        callout_type=q_badge, title=title or "SYSTEM NOTICE",
                        subtitle=subtitle or "", is_quote=(btype == "quote" or is_quote),
                        badge_color=badge_color
                    )
                elif btype in ("frame", "window", "terminal"):
                    f_title = title or ("HUD.TERMINAL" if btype == "terminal" else "SYSTEM.CORE")
                    if btype == "terminal":
                        f_title = f"╔═ {f_title} // RUNTIME.SYS"
                    svg = generate_frame(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent, tertiary=tertiary,
                        frame_type=frame_type, title=f_title,
                        tag=tag or "[OPEN_HUD]", tag_url=tag_url, close_url=close_url
                    )
                elif btype == "chip":
                    text_val = title or "CHIP"
                    if gh_stat:
                        repo_name = repo or "Kazinagg/pixel-readme-kit"
                        stat_text, _ = fetch_github_stat(repo_name, gh_stat)
                        text_val = stat_text
                    svg = generate_chip(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        chip_type=chip_type, text=text_val, width=width_val, decay_dir=decay_dir
                    )
                elif btype == "divider":
                    svg = generate_divider(style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "splitter":
                    svg = generate_splitter(style=style, mode=mode, preset=preset, primary=primary, accent=accent, label=label)
                elif btype == "metrics":
                    cards = []
                    raw_items = items or body
                    if raw_items:
                        for line in raw_items.splitlines() if "\n" in raw_items else raw_items.split("|"):
                            item = line.strip()
                            if not item:
                                continue
                            if item.startswith("-"): item = item[1:].strip()
                            if item.startswith("milestone") or item.startswith("card"):
                                item = item.split(" ", 1)[-1].strip()
                            # Check if key="val" format
                            if '="' in item or "='" in item:
                                parsed = parse_directive_attrs(item)
                                cards.append({
                                    "label": parsed.get("label", "METRIC"),
                                    "value": parsed.get("value", "100"),
                                    "delta": parsed.get("delta"),
                                    "status": parsed.get("status")
                                })
                            else:
                                c_label, c_val = item, ""
                                c_delta, c_status = None, None
                                if ":" in item:
                                    parts = item.split(":", 1)
                                    c_label = parts[0].strip()
                                    rest = parts[1].strip()
                                    m_st = re.search(r'\[(.*?)\]', rest)
                                    if m_st:
                                        c_status = m_st.group(1).strip()
                                        rest = (rest[:m_st.start()] + rest[m_st.end():]).strip()
                                    m_dt = re.search(r'\((.*?)\)', rest)
                                    if m_dt:
                                        c_delta = m_dt.group(1).strip()
                                        rest = (rest[:m_dt.start()] + rest[m_dt.end():]).strip()
                                    c_val = rest
                                cards.append({"label": c_label, "value": c_val, "delta": c_delta, "status": c_status})
                    if not cards:
                        cards = [{"label": title or "BENCHMARK", "value": subtitle or "1,200+", "delta": delta or tag, "status": status, "trend": trend}]
                    svg = generate_metrics(cards=cards, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "progress":
                    val = int(value_str) if value_str and value_str.isdigit() else 75
                    svg = generate_progress(value=val, label=title or "PROGRESS", sub=sub_text, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "techstack":
                    item_list = [x.strip() for x in (items or subtitle or "python,cpp,docker,git").split(",") if x.strip()]
                    svg = generate_techstack(items=item_list, columns=cols_val, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "timeline":
                    timeline_items = []
                    raw_lines = (body or items or "").splitlines()
                    for line in raw_lines:
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("-"): line = line[1:].strip()
                        for prefix in ("milestone", "stage", "item"):
                            if line.lower().startswith(prefix):
                                line = line[len(prefix):].strip()
                                break
                        item_attrs = parse_directive_attrs(line)
                        if item_attrs:
                            timeline_items.append(item_attrs)
                    svg = generate_timeline(items=timeline_items if timeline_items else None, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "social":
                    tag_list = [x.strip() for x in tags_str.split(",") if x.strip()]
                    svg = generate_social(title=title or "PIXEL README KIT", subtitle=subtitle or "HUD SYSTEM", repo=repo or "Kazinagg/pixel-readme-kit", tags=tag_list, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                else:
                    self.send_error(400, f"Unsupported block type: {btype}")
                    return

                validate_svg(svg)
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
                self.end_headers()
                self.wfile.write(svg.encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Render error: {e}")
                return

        # 4. Preview Compiled Content (/api/preview)
        if path == "/api/preview":
            req_theme = query.get("theme", ["dark"])[0]
            edit_html = self.render_template_to_preview_html(preview_theme=req_theme, view_mode=False)
            view_html = self.render_template_to_preview_html(preview_theme=req_theme, view_mode=True)
            line_count = 0
            byte_size = 0
            if os.path.exists(self.template_file):
                try:
                    with open(self.template_file, "r", encoding="utf-8") as f:
                        f_data = f.read()
                        line_count = len(f_data.splitlines())
                        byte_size = len(f_data.encode("utf-8"))
                except Exception:
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
            self.end_headers()
            resp = {
                "status": "success",
                "filename": self.template_file,
                "lines": line_count,
                "bytes": byte_size,
                "html": edit_html,
                "view_html": view_html
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 5. List Presets and Icons (/api/presets)
        if path == "/api/presets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            presets_dir = os.path.join(PROJECT_ROOT, "presets")
            preset_names = []
            if os.path.exists(presets_dir):
                preset_names = [f.replace(".json", "") for f in os.listdir(presets_dir) if f.endswith(".json")]
            if not preset_names:
                preset_names = ["cyberpunk", "amber", "matrix", "tokyo"]
            data = {
                "presets": sorted(preset_names),
                "icons": list_available_icons()
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # 6. Extract Blocks from Template (/api/template/blocks)
        if path == "/api/template/blocks":
            if not os.path.exists(self.template_file):
                self.send_error(404, "Template file not found")
                return
            with open(self.template_file, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = extract_template_blocks(content)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            resp = {
                "status": "success",
                "filename": self.template_file,
                "count": len(blocks),
                "blocks": blocks
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 7. Static SVG File Serving with Theme Adaptability
        if path.lower().endswith(".svg"):
            local_path = path.lstrip("/")
            if not os.path.exists(local_path) and hasattr(self, "assets_dir") and self.assets_dir:
                candidate = os.path.join(self.assets_dir, os.path.basename(path))
                if os.path.exists(candidate):
                    local_path = candidate

            if os.path.exists(local_path):
                try:
                    with open(local_path, "r", encoding="utf-8", errors="replace") as f:
                        svg_data = f.read()
                    req_theme = query.get("theme", [None])[0]
                    if req_theme == "light":
                        # Strip dark @media block so SVG unconditionally renders light :root
                        svg_data = re.sub(r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{[\s\S]*?\}\s*\}', '', svg_data)
                    elif req_theme == "dark":
                        # If dark requested, find dark :root and replace light :root
                        m_dark = re.search(r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{\s*:root\s*\{([\s\S]*?)\}\s*\}', svg_data)
                        if m_dark:
                            dark_vars = m_dark.group(1)
                            svg_data = re.sub(r':root\s*\{[\s\S]*?\}', f':root {{{dark_vars}}}', svg_data, count=1)
                            svg_data = re.sub(r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{[\s\S]*?\}\s*\}', '', svg_data)

                    self.send_response(200)
                    self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
                    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
                    self.end_headers()
                    self.wfile.write(svg_data.encode("utf-8"))
                    return
                except Exception:
                    pass

        # 8. Fallback to standard file serving
        return super().do_GET()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        if path == "/api/recompile":
            self.trigger_compile()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b"{\"status\": \"recompiled\"}")
            return

        # 9. Batch Apply Global Theme to All Blocks (/api/template/apply_global_theme)
        if path == "/api/template/apply_global_theme":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req = json.loads(body)
                g_style = req.get("style", "cyberpunk")
                g_preset = req.get("preset", "cyberpunk")
                g_mode = req.get("mode", "auto")
                g_prim = req.get("primary", "")
                g_acc = req.get("accent", "")
                g_tert = req.get("tertiary", "")
                is_force = bool(req.get("force", False))

                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Regex to update each directive's style and preset
                def update_dir(m):
                    tag_content = m.group(0)
                    tag_type = m.group(1).lower()
                    if tag_type.startswith("/"):
                        return tag_content

                    # 1. Update style
                    if re.search(r'\bstyle="[^"]*"', tag_content):
                        tag_content = re.sub(r'\bstyle="[^"]*"', f'style="{g_style}"', tag_content)
                    else:
                        tag_content = tag_content.replace(f"<!-- pixel-kit:{m.group(1)}", f'<!-- pixel-kit:{m.group(1)} style="{g_style}"')

                    # 2. Preset and Colors
                    if g_preset == "custom":
                        # Remove preset attribute
                        tag_content = re.sub(r'\s*\bpreset="[^"]*"', '', tag_content)
                        # Set primary
                        if g_prim:
                            if re.search(r'\bprimary="[^"]*"', tag_content):
                                tag_content = re.sub(r'\bprimary="[^"]*"', f'primary="{g_prim}"', tag_content)
                            else:
                                tag_content = re.sub(r'(style="[^"]*")', rf'\1 primary="{g_prim}"', tag_content)
                        # Handle accent and badge_color
                        if is_force:
                            if g_acc:
                                if re.search(r'\baccent="[^"]*"', tag_content):
                                    tag_content = re.sub(r'\baccent="[^"]*"', f'accent="{g_acc}"', tag_content)
                                else:
                                    tag_content = re.sub(r'(style="[^"]*")', rf'\1 accent="{g_acc}"', tag_content)
                            else:
                                tag_content = re.sub(r'\s*\baccent="[^"]*"', '', tag_content)
                            tag_content = re.sub(r'\s*\bbadge_color="[^"]*"', '', tag_content)
                        else:
                            # Soft Apply: keep existing accent if present, otherwise set g_acc
                            if not re.search(r'\baccent="[^"]*"', tag_content) and g_acc:
                                tag_content = re.sub(r'(style="[^"]*")', rf'\1 accent="{g_acc}"', tag_content)

                        # Handle tertiary
                        if is_force:
                            if g_tert:
                                if re.search(r'\btertiary="[^"]*"', tag_content):
                                    tag_content = re.sub(r'\btertiary="[^"]*"', f'tertiary="{g_tert}"', tag_content)
                                else:
                                    tag_content = re.sub(r'(style="[^"]*")', rf'\1 tertiary="{g_tert}"', tag_content)
                            else:
                                tag_content = re.sub(r'\s*\btertiary="[^"]*"', '', tag_content)
                        else:
                            # Soft Apply: keep existing tertiary if present, otherwise set g_tert
                            if not re.search(r'\btertiary="[^"]*"', tag_content) and g_tert:
                                tag_content = re.sub(r'(style="[^"]*")', rf'\1 tertiary="{g_tert}"', tag_content)
                    else:
                        # Named preset
                        if re.search(r'\bpreset="[^"]*"', tag_content):
                            tag_content = re.sub(r'\bpreset="[^"]*"', f'preset="{g_preset}"', tag_content)
                        else:
                            tag_content = re.sub(r'(style="[^"]*")', rf'\1 preset="{g_preset}"', tag_content)

                        # Primary is inherited from preset, so remove block-level primary
                        tag_content = re.sub(r'\s*\bprimary="[^"]*"', '', tag_content)

                        if is_force:
                            # Force: remove custom accent, tertiary and badge_color
                            tag_content = re.sub(r'\s*\baccent="[^"]*"', '', tag_content)
                            tag_content = re.sub(r'\s*\btertiary="[^"]*"', '', tag_content)
                            tag_content = re.sub(r'\s*\bbadge_color="[^"]*"', '', tag_content)
                        # Soft apply: preserve block's accent and badge_color!

                    # 3. Update mode if not auto
                    if g_mode and g_mode != "auto":
                        if re.search(r'\bmode="[^"]*"', tag_content):
                            tag_content = re.sub(r'\bmode="[^"]*"', f'mode="{g_mode}"', tag_content)
                        else:
                            tag_content = re.sub(r'(style="[^"]*")', rf'\1 mode="{g_mode}"', tag_content)
                    else:
                        # Remove explicit mode so it inherits auto
                        tag_content = re.sub(r'\s*\bmode="[^"]*"', '', tag_content)

                    return tag_content

                updated_content = re.sub(
                    r'<!--\s*pixel-kit:([a-zA-Z0-9_\-]+)\b[\s\S]*?-->',
                    update_dir,
                    content
                )

                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)

                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b"{\"status\": \"applied\"}")
                return
            except Exception as e:
                self.send_error(500, f"Apply global theme error: {e}")
                return

        if path == "/api/insert":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req = json.loads(body)
                directive = req.get("directive", "")
                if os.path.exists(self.template_file):
                    with open(self.template_file, "a", encoding="utf-8") as f:
                        f.write(f"\n{directive}\n")
                    self.trigger_compile()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b"{\"status\": \"inserted\"}")
                    return
                else:
                    self.send_error(404, "Template file not found")
                    return
            except Exception as e:
                self.send_error(500, f"Insert error: {e}")
                return

        if path == "/api/template/update_block":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req = json.loads(body)
                blk_id = int(req.get("id", -1))
                new_raw = req.get("directive_raw", "")
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks = extract_template_blocks(content)
                if blk_id < 0 or blk_id >= len(blocks):
                    self.send_error(400, f"Invalid block index: {blk_id}")
                    return
                target = blocks[blk_id]
                new_content = content[:target["start"]] + new_raw + content[target["end"]:]
                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "updated", "id": blk_id}).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Update block error: {e}")
                return

        if path == "/api/template/delete_block":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req = json.loads(body)
                blk_id = int(req.get("id", -1))
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks = extract_template_blocks(content)
                if blk_id < 0 or blk_id >= len(blocks):
                    self.send_error(400, f"Invalid block index: {blk_id}")
                    return
                target = blocks[blk_id]
                start = target["start"]
                end = target["end"]
                if start > 0 and content[start-1] == '\n':
                    start -= 1
                new_content = content[:start] + content[end:]
                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "deleted"}).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Delete block error: {e}")
                return

        if path == "/api/template/insert_block":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req = json.loads(body)
                after_id = int(req.get("after_id", -1))
                directive_raw = req.get("directive_raw", "").strip()
                if not directive_raw:
                    self.send_error(400, "Empty directive_raw")
                    return
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()

                blocks = extract_template_blocks(content)
                if after_id == -1 or not blocks:
                    new_content = f"{directive_raw}\n\n" + content
                elif 0 <= after_id < len(blocks):
                    target = blocks[after_id]
                    ins_pos = target["end"]
                    new_content = content[:ins_pos] + f"\n\n{directive_raw}\n" + content[ins_pos:]
                else:
                    new_content = content.rstrip() + f"\n\n{directive_raw}\n"

                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "inserted"}).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Insert block error: {e}")
                return

        if path == "/api/git/push_readme":
            try:
                # 1. Recompile fresh README and assets
                self.trigger_compile()

                # 2. Check if git repository exists
                work_dir = os.path.dirname(os.path.abspath(self.template_file)) if self.template_file else os.getcwd()
                res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=work_dir, capture_output=True, text=True)
                if res.returncode != 0:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": False, "error": "Not a Git repository"}).encode("utf-8"))
                    return

                # 3. Carefully stage ONLY README.md, README.template.md, and assets_dir
                # STRICT ISOLATION: Never run `git add .` or stage unrelated code files
                files_to_add = []
                if self.output_file and os.path.exists(self.output_file):
                    files_to_add.append(os.path.relpath(self.output_file, work_dir))
                if self.template_file and os.path.exists(self.template_file):
                    files_to_add.append(os.path.relpath(self.template_file, work_dir))
                if self.assets_dir and os.path.exists(self.assets_dir):
                    files_to_add.append(os.path.relpath(self.assets_dir, work_dir))

                if not files_to_add:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": False, "error": "No README or assets found to stage"}).encode("utf-8"))
                    return

                for target in files_to_add:
                    subprocess.run(["git", "add", target], cwd=work_dir, check=True)

                # 4. Check if there are staged changes
                diff_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=work_dir)
                has_staged_changes = (diff_res.returncode != 0)

                committed = False
                if has_staged_changes:
                    commit_msg = "docs: update README via Pixel-Kit Studio"
                    c_res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=work_dir, capture_output=True, text=True)
                    if c_res.returncode != 0:
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"ok": False, "error": f"Git commit failed: {c_res.stderr.strip()}"}).encode("utf-8"))
                        return
                    committed = True

                # 5. Push to remote
                p_res = subprocess.run(["git", "push"], cwd=work_dir, capture_output=True, text=True)
                if p_res.returncode != 0:
                    self.send_response(500)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "ok": False,
                        "error": f"Git push failed: {p_res.stderr.strip() or p_res.stdout.strip()}",
                        "committed": committed
                    }).encode("utf-8"))
                    return

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": True,
                    "committed": committed,
                    "files": files_to_add,
                    "message": "README and assets pushed to GitHub successfully!" if committed else "Already up to date. Pushed latest commits to GitHub."
                }).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Git push error: {e}")
                return

        self.send_error(404, "Endpoint not found")

    def render_template_to_preview_html(self, preview_theme: str = "auto", view_mode: bool = False) -> str:
        """Compiles template and formats markdown into HTML for browser preview.
        When view_mode=True, compiles pure GitHub markdown without interactive wrappers or synthetic line breaks.
        When view_mode=False, injects interactive block wrappers and insert dividers for Edit mode.
        """
        if not os.path.exists(self.template_file):
            return f"<div style='padding:20px;color:#f85149;'>Template file not found: <code>{self.template_file}</code></div>"

        try:
            with open(self.template_file, "r", encoding="utf-8") as f:
                raw_template = f.read()

            blocks = extract_template_blocks(raw_template)
            if not blocks or view_mode:
                # 100% authentic GitHub render directly from raw template
                compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False, bust_cache=True)
                compiled_md = compiler.compile_string(raw_template)
                html = self.markdown_to_html(compiled_md)
                if preview_theme in ("light", "dark"):
                    html = re.sub(
                        r'(<img\b[^>]*?\bsrc=")([^"]+)(\")',
                        lambda m: f'{m.group(1)}{m.group(2).split("?")[0]}?theme={preview_theme}&t={int(time.time()*1000)}{m.group(3)}',
                        html
                    )
                return html

            # Inject delimiters around each block in reverse order to preserve string offsets
            wrapped_template = raw_template
            for b in reversed(blocks):
                b_id = b["id"]
                b_type = b["type"]
                start = b["start"]
                end = b["end"]
                wrapped_template = (
                    wrapped_template[:start]
                    + f"<!-- PK_BLOCK_START:{b_id}:{b_type} -->\n"
                    + wrapped_template[start:end]
                    + f"\n<!-- PK_BLOCK_END:{b_id}:{b_type} -->"
                    + wrapped_template[end:]
                )

            compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=False, bust_cache=True)
            compiled_md = compiler.compile_string(wrapped_template)

            # Convert markdown elements into GitHub-style HTML
            html = self.markdown_to_html(compiled_md)

            def start_repl(m):
                blk_id = int(m.group(1))
                blk_type = m.group(2).upper()
                top_divider = ""
                if blk_id == 0:
                    top_divider = '<div class="pk-insert-divider" data-after-id="-1"><button class="pk-insert-btn" onclick="openInsertAt(-1, event)">+ Add block at top</button></div>'
                return f"""{top_divider}
<div class="pk-block-wrapper" id="pk-block-{blk_id}" data-pk-id="{blk_id}" data-pk-type="{blk_type.lower()}" onclick="selectBlockFromPreview({blk_id}, event)">
  <div class="pk-block-hud-bar">
    <div class="pk-hud-badge"><span class="pk-hud-dot">●</span> {blk_type} <span class="pk-hud-num">#{blk_id}</span></div>
    <div class="pk-hud-actions">
      <button class="pk-hud-btn edit-btn" onclick="selectBlockFromPreview({blk_id}, event)">EDIT</button>
      <button class="pk-hud-btn del-btn" onclick="confirmDeleteBlock({blk_id}, event)">DEL</button>
    </div>
  </div>
  <div class="pk-block-content">"""

            def end_repl(m):
                blk_id = int(m.group(1))
                return f"""  </div>
</div>
<div class="pk-insert-divider" data-after-id="{blk_id}"><button class="pk-insert-btn" onclick="openInsertAt({blk_id}, event)">+ Add block here</button></div>"""

            html = re.sub(r'<!--\s*PK_BLOCK_START:(\d+):(\w+)\s*-->', start_repl, html)
            html = re.sub(r'<!--\s*PK_BLOCK_END:(\d+):(\w+)\s*-->', end_repl, html)

            if preview_theme in ("light", "dark"):
                html = re.sub(
                    r'(<img\b[^>]*?\bsrc=")([^"]+)(\")',
                    lambda m: f'{m.group(1)}{m.group(2).split("?")[0]}?theme={preview_theme}&t={int(time.time()*1000)}{m.group(3)}',
                    html
                )

            return html
        except Exception as e:
            return f"<div style='padding:20px;color:#f85149;'>Compilation Error: {e}</div>"

    @classmethod
    def markdown_to_html(cls, *args, **kwargs) -> str:
        """
        Lightweight yet complete GitHub Flavored Markdown converter for README preview.
        Uses MarkdownIt with GFM tables and strikethroughs enabled when available,
        with task list checkboxes, GitHub alert callouts, and robust zero-dependency fallbacks.
        Supports both cls.markdown_to_html(md) and handler.markdown_to_html(handler, md).
        """
        if len(args) == 1:
            md = args[0]
        elif len(args) >= 2:
            md = args[1]
        else:
            md = kwargs.get("md", "")

        try:
            from markdown_it import MarkdownIt
            md_parser = MarkdownIt().enable('table').enable('strikethrough')
            html = md_parser.render(md)

            # 1. GFM Task List Checkboxes
            html = re.sub(r'<li>\s*\[ \]\s+', r'<li class="task-list-item"><input type="checkbox" disabled class="task-list-item-checkbox"> ', html)
            html = re.sub(r'<li>\s*\[[xX]\]\s+', r'<li class="task-list-item"><input type="checkbox" checked disabled class="task-list-item-checkbox"> ', html)

            # 2. GitHub Alert Callouts (> [!NOTE], > [!TIP], etc.)
            def alert_repl(m):
                alert_type = m.group(1).upper()
                body = m.group(2).strip()
                icons = {
                    "NOTE": '<svg class="octicon octicon-info" viewBox="0 0 16 16" width="16" height="16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>',
                    "TIP": '<svg class="octicon octicon-light-bulb" viewBox="0 0 16 16" width="16" height="16"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.666 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.416-.701 2.5-1.328 3.25-.095.115-.184.22-.268.319-.18.213-.362.43-.542.68-.207.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6.25 15h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1 0-1.5Z"></path></svg>',
                    "IMPORTANT": '<svg class="octicon octicon-report" viewBox="0 0 16 16" width="16" height="16"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
                    "WARNING": '<svg class="octicon octicon-alert" viewBox="0 0 16 16" width="16" height="16"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
                    "CAUTION": '<svg class="octicon octicon-stop" viewBox="0 0 16 16" width="16" height="16"><path d="M4.47.047A1.75 1.75 0 0 1 5.707 0h4.586c.464 0 .909.184 1.237.513l3.957 3.957c.328.328.513.773.513 1.237v4.586c0 .464-.185.909-.513 1.237l-3.957 3.957c-.328.328-.773.513-1.237.513H5.707c-.464 0-.91-.185-1.238-.513L.512 11.53A1.75 1.75 0 0 1 0 10.293V5.707c0-.464.184-.91.513-1.238ZM1.5 5.707v4.586c0 .066.026.13.073.177l3.957 3.957c.047.047.111.073.177.073h4.586c.066 0 .13-.026.177-.073l3.957-3.957c.047-.047.073-.111.073-.177V5.707a.25.25 0 0 0-.073-.177L10.464 1.573a.25.25 0 0 0-.177-.073H5.707a.25.25 0 0 0-.177.073L1.573 5.53a.25.25 0 0 0-.073.177Zm7.25 4.543v1.5a.75.75 0 0 1-1.5 0v-1.5a.75.75 0 0 1 1.5 0ZM8 3.5a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 3.5Z"></path></svg>',
                }
                icon_svg = icons.get(alert_type, icons["NOTE"])
                title_text = alert_type.capitalize()
                return f"""<div class="markdown-alert markdown-alert-{alert_type.lower()}">
  <p class="markdown-alert-title">{icon_svg} {title_text}</p>
  <div>{body}</div>
</div>"""

            html = re.sub(
                r'<blockquote>\s*<p>\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\s*<br\s*/?>)?\s*([\s\S]*?)</p>\s*</blockquote>',
                alert_repl,
                html,
                flags=re.IGNORECASE
            )
            return html
        except Exception:
            return cls._fallback_markdown_to_html(md)

    @classmethod
    def _fallback_markdown_to_html(cls, md: str) -> str:
        """
        Pure Python fallback GFM-compatible markdown converter when markdown-it is unavailable.
        Supports tables, task lists, code blocks, alerts, and inline styling.
        """
        lines = md.split("\n")
        out = []
        in_code_block = False
        in_list = False
        in_blockquote = False
        in_table = False
        table_headers = []
        table_rows = []

        def flush_table():
            nonlocal in_table, table_headers, table_rows
            if not in_table:
                return
            t_html = ["<table>"]
            if table_headers:
                t_html.append("<thead><tr>")
                for h in table_headers:
                    t_html.append(f"<th>{cls._format_inline_md(h.strip())}</th>")
                t_html.append("</tr></thead>")
            if table_rows:
                t_html.append("<tbody>")
                for r in table_rows:
                    t_html.append("<tr>")
                    for c in r:
                        t_html.append(f"<td>{cls._format_inline_md(c.strip())}</td>")
                    t_html.append("</tr>")
                t_html.append("</tbody>")
            t_html.append("</table>")
            out.append("".join(t_html))
            in_table = False
            table_headers = []
            table_rows = []

        i = 0
        while i < len(lines):
            line = lines[i]
            trimmed = line.strip()

            # 1. GFM Table Detection
            if trimmed.startswith("|") and trimmed.endswith("|"):
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if in_blockquote:
                    out.append("</blockquote>")
                    in_blockquote = False

                cells = [c for c in trimmed.split("|")[1:-1]]
                if not in_table:
                    # Check if next line is table delimiter (| :--- | :--- |)
                    if i + 1 < len(lines) and re.match(r'^\s*\|(?:\s*:?-+:?\s*\|)+\s*$', lines[i+1].strip()):
                        in_table = True
                        table_headers = cells
                        table_rows = []
                        i += 2  # skip header and delimiter
                        continue
                    else:
                        out.append(f"<p>{cls._format_inline_md(line)}</p>")
                        i += 1
                        continue
                else:
                    table_rows.append(cells)
                    i += 1
                    continue
            else:
                if in_table:
                    flush_table()

            # 2. Code blocks
            if trimmed.startswith("```"):
                if not in_code_block:
                    if in_list:
                        out.append("</ul>")
                        in_list = False
                    if in_blockquote:
                        out.append("</blockquote>")
                        in_blockquote = False
                    in_code_block = True
                    lang = trimmed[3:].strip()
                    out.append(f"<pre class='gh-code-block' data-lang='{lang}'><code>")
                else:
                    in_code_block = False
                    out.append("</code></pre>")
                i += 1
                continue

            if in_code_block:
                escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                out.append(escaped)
                i += 1
                continue

            # 3. Raw HTML preserved
            if trimmed.startswith("<") or trimmed.startswith("<!--") or trimmed.endswith(">"):
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if in_blockquote:
                    out.append("</blockquote>")
                    in_blockquote = False
                out.append(line)
                i += 1
                continue

            if not trimmed:
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if in_blockquote:
                    out.append("</blockquote>")
                    in_blockquote = False
                out.append("")
                i += 1
                continue

            # 4. Headings
            m_h = re.match(r'^(#{1,6})\s+(.*)$', line)
            if m_h:
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if in_blockquote:
                    out.append("</blockquote>")
                    in_blockquote = False
                level = len(m_h.group(1))
                h_text = m_h.group(2)
                out.append(f"<h{level} class='gh-h{level}'>{h_text}</h{level}>")
                i += 1
                continue

            # 5. Horizontal rules
            if trimmed in ("---", "***", "___"):
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if in_blockquote:
                    out.append("</blockquote>")
                    in_blockquote = False
                out.append("<hr class='gh-hr'>")
                i += 1
                continue

            # 6. GitHub Alert Callouts (> [!NOTE], etc.)
            m_alert = re.match(r'^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$', line, re.IGNORECASE)
            if m_alert:
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if in_blockquote:
                    out.append("</blockquote>")
                    in_blockquote = False
                alert_type = m_alert.group(1).upper()
                alert_body_lines = []
                i += 1
                while i < len(lines) and lines[i].startswith(">"):
                    alert_body_lines.append(lines[i].lstrip("> ").strip())
                    i += 1
                body = "<br>".join(cls._format_inline_md(b) for b in alert_body_lines if b)
                title = alert_type.capitalize()
                out.append(f"""<div class="markdown-alert markdown-alert-{alert_type.lower()}">
  <p class="markdown-alert-title">{title}</p>
  <div>{body}</div>
</div>""")
                continue

            # 7. Blockquotes
            if line.startswith("> "):
                if in_list:
                    out.append("</ul>")
                    in_list = False
                if not in_blockquote:
                    out.append("<blockquote>")
                    in_blockquote = True
                bq_content = cls._format_inline_md(line[2:])
                out.append(f"<p>{bq_content}</p>")
                i += 1
                continue
            elif in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False

            # 8. GFM Task List items
            m_task_checked = re.match(r'^[-*]\s+\[[xX]\]\s+(.*)$', line)
            m_task_open = re.match(r'^[-*]\s+\[ \]\s+(.*)$', line)
            if m_task_checked:
                if not in_list:
                    out.append("<ul>")
                    in_list = True
                item_content = cls._format_inline_md(m_task_checked.group(1))
                out.append(f'<li class="task-list-item"><input type="checkbox" checked disabled class="task-list-item-checkbox"> {item_content}</li>')
                i += 1
                continue
            elif m_task_open:
                if not in_list:
                    out.append("<ul>")
                    in_list = True
                item_content = cls._format_inline_md(m_task_open.group(1))
                out.append(f'<li class="task-list-item"><input type="checkbox" disabled class="task-list-item-checkbox"> {item_content}</li>')
                i += 1
                continue

            # 9. Standard unordered lists
            if line.startswith("- ") or line.startswith("* "):
                if not in_list:
                    out.append("<ul>")
                    in_list = True
                item_content = cls._format_inline_md(line[2:])
                out.append(f"<li>{item_content}</li>")
                i += 1
                continue
            elif in_list:
                out.append("</ul>")
                in_list = False

            # 10. Paragraphs
            p_content = cls._format_inline_md(line)
            out.append(f"<p>{p_content}</p>")
            i += 1

        if in_table:
            flush_table()
        if in_code_block:
            out.append("</code></pre>")
        if in_list:
            out.append("</ul>")
        if in_blockquote:
            out.append("</blockquote>")

        return "\n".join(out)

    @classmethod
    def _format_inline_md(cls, text: str) -> str:
        """Formats inline markdown elements like bold, italic, code, links, images, strikethrough."""
        text = re.sub(r'`([^`]+)`', r'<code class="gh-inline-code">\1</code>', text)
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="gh-img" />', text)
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="gh-link">\1</a>', text)
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        return text

    @classmethod
    def trigger_compile(cls):
        """Forces compilation and notifies all SSE clients."""
        if os.path.exists(cls.template_file):
            compiler = MarkdownCompiler(assets_dir=cls.assets_dir, use_cache=False, bust_cache=True)
            compiler.compile_file(cls.template_file, cls.output_file)

        with cls.subscribers_lock:
            dead = set()
            for s in cls.subscribers:
                try:
                    s.wfile.write(b"event: reload\ndata: {\"reloaded\": true}\n\n")
                    s.wfile.flush()
                except Exception:
                    dead.add(s)
            cls.subscribers.difference_update(dead)


# ==============================================================================
# SERVER RUNNER & WATCHER
# ==============================================================================

class ThreadedStudioServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        """Suppress noisy tracebacks for normal browser disconnects / tab reloads."""
        exc_type, exc_val, _ = sys.exc_info()
        if exc_type and issubclass(exc_type, (ConnectionError, ConnectionResetError, ConnectionAbortedError, BrokenPipeError)):
            return
        if exc_type and issubclass(exc_type, OSError) and getattr(exc_val, "winerror", None) in (10053, 10054):
            return
        super().handle_error(request, client_address)

def start_file_watcher(template_path: str, handler_class, poll_interval: float = 0.3):
    """Background thread watching template file mtime to trigger auto-reloads."""
    def watcher_loop():
        last_mtime = 0
        if os.path.exists(template_path):
            last_mtime = os.path.getmtime(template_path)

        while True:
            time.sleep(poll_interval)
            if os.path.exists(template_path):
                try:
                    mtime = os.path.getmtime(template_path)
                    if mtime > last_mtime:
                        last_mtime = mtime
                        handler_class.trigger_compile()
                except OSError:
                    pass

    t = threading.Thread(target=watcher_loop, daemon=True)
    t.start()
    return t

def run_studio_server(template_path="README.template.md", output_path="README.md",
                      assets_dir="assets/generated", port=3000, open_browser=False):
    """Starts the HUD Studio server and watches the template."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    StudioRequestHandler.template_file = template_path
    StudioRequestHandler.output_file = output_path
    StudioRequestHandler.assets_dir = assets_dir

    # Initial compilation
    if os.path.exists(template_path):
        compiler = MarkdownCompiler(assets_dir=assets_dir, use_cache=True)
        compiler.compile_file(template_path, output_path)

    # Start watcher
    start_file_watcher(template_path, StudioRequestHandler)

    server = ThreadedStudioServer(("127.0.0.1", port), StudioRequestHandler)
    url = f"http://localhost:{port}/"
    print(f"[*] ╔═══════════════════════════════════════════════════════════╗")
    print(f"[*] ║      PIXEL README KIT // HUD STUDIO LIVE PREVIEW v4.1     ║")
    print(f"[*] ╚═══════════════════════════════════════════════════════════╝")
    print(f"[*] ▶ Studio Web UI:     {url}")
    print(f"[*] ▶ Active Template:   {template_path}")
    print(f"[*] ▶ Output Target:     {output_path}")
    print(f"[*] ▶ Live Reload:       ENABLED (300ms SSE sync)")
    print(f"[*] Press Ctrl+C to terminate.")

    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down HUD Studio server...")
    finally:
        server.server_close()

if __name__ == "__main__":
    run_studio_server()
