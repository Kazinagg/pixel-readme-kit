"""
Pixel Readme Kit v4.0 - Live Preview & HUD Studio Server.
Zero-dependency HTTP server with Server-Sent Events (SSE) live reload,
real-time SVG rendering API, and interactive HUD Studio Web UI.
"""

import os
import sys
import json
import time
import urllib.parse
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

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
from generator.compiler import MarkdownCompiler

# ==============================================================================
# EMBEDDED HUD STUDIO HTML/CSS/JS INTERFACE
# ==============================================================================

STUDIO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIXEL README KIT // HUD STUDIO v4.0</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Orbitron:wght@600;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #07090e;
      --panel-bg: rgba(13, 19, 33, 0.88);
      --panel-border: rgba(0, 200, 215, 0.28);
      --primary: #00c8d7;
      --accent: #a855f7;
      --amber: #f59e0b;
      --green: #00d26a;
      --text: #f1f5f9;
      --text-dim: #94a3b8;
      --font-mono: 'JetBrains Mono', monospace;
      --font-hud: 'Orbitron', var(--font-mono);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-mono);
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

    /* Scanline Overlay */
    .scanlines {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
      background-size: 100% 4px;
      z-index: 999;
      opacity: 0.6;
    }

    /* Top HUD Navbar */
    header.hud-nav {
      height: 54px;
      background: rgba(10, 14, 23, 0.95);
      border-bottom: 1px solid var(--panel-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 100;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-hud);
      font-weight: 900;
      font-size: 16px;
      color: var(--primary);
      letter-spacing: 2px;
      text-shadow: 0 0 12px rgba(0, 200, 215, 0.6);
    }
    .brand-badge {
      font-size: 9px;
      padding: 2px 6px;
      background: rgba(168, 85, 247, 0.2);
      border: 1px solid var(--accent);
      color: var(--accent);
      border-radius: 2px;
    }

    .nav-status {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .status-indicator {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--green);
      font-size: 11px;
    }
    .pulse-dot {
      width: 8px; height: 8px;
      background: var(--green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--green);
      animation: pulse 1.8s infinite;
    }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

    .nav-btn {
      background: rgba(0, 200, 215, 0.1);
      border: 1px solid var(--primary);
      color: var(--primary);
      padding: 6px 14px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .nav-btn:hover {
      background: var(--primary);
      color: #000;
      box-shadow: 0 0 14px rgba(0, 200, 215, 0.6);
    }

    /* Main Workspace Split Layout */
    .workspace {
      flex: 1;
      display: grid;
      grid-template-columns: 460px 1fr;
      overflow: hidden;
    }

    /* Left Sidebar: Component Builder */
    .builder-pane {
      background: var(--panel-bg);
      border-right: 1px solid var(--panel-border);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 20px;
      gap: 18px;
    }

    .pane-title {
      font-family: var(--font-hud);
      font-size: 12px;
      color: var(--primary);
      letter-spacing: 1.5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px dashed rgba(0, 200, 215, 0.3);
      padding-bottom: 6px;
    }

    .control-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .control-group label {
      font-size: 10.5px;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .control-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    select, input[type="text"], input[type="number"] {
      background: rgba(10, 14, 23, 0.85);
      border: 1px solid rgba(0, 200, 215, 0.3);
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 8px 10px;
      outline: none;
      transition: border-color 0.2s;
    }
    select:focus, input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 8px rgba(0, 200, 215, 0.3);
    }

    .checkbox-row {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      font-size: 11.5px;
      color: var(--text);
    }
    .checkbox-row input {
      accent-color: var(--primary);
    }

    /* Live Component Preview Card */
    .live-card {
      border: 1px solid rgba(0, 200, 215, 0.4);
      background: rgba(6, 9, 15, 0.95);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }
    .live-preview-box {
      width: 100%;
      min-height: 120px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0d1117;
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 10px;
      overflow: hidden;
      position: relative;
    }
    .live-preview-box svg {
      max-width: 100%;
      height: auto;
    }

    /* HUD Debug Mode Overlay */
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

    .char-badge {
      font-size: 9.5px;
      padding: 1px 5px;
      border-radius: 2px;
      margin-left: 6px;
      font-weight: 600;
      text-transform: none;
    }
    .badge-optimal { background: rgba(0, 210, 106, 0.2); color: #00d26a; border: 1px solid #00d26a; }
    .badge-warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }
    .badge-danger  { background: rgba(239, 68, 68, 0.25); color: #ef4444; border: 1px solid #ef4444; }

    .directive-code {
      background: #05070a;
      border: 1px solid rgba(168, 85, 247, 0.3);
      padding: 8px 10px;
      color: #38bdf8;
      font-size: 11px;
      font-family: var(--font-mono);
      white-space: pre-wrap;
      word-break: break-all;
      user-select: all;
    }

    .action-btn-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .btn-secondary {
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid var(--accent);
      color: var(--accent);
      padding: 8px;
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }
    .btn-secondary:hover {
      background: var(--accent);
      color: #fff;
      box-shadow: 0 0 12px rgba(168, 85, 247, 0.6);
    }

    /* Right Pane: Full README Live Preview */
    .preview-pane {
      display: flex;
      flex-direction: column;
      background: #0d1117;
      overflow: hidden;
    }
    .preview-toolbar {
      height: 44px;
      background: rgba(13, 17, 23, 0.98);
      border-bottom: 1px solid rgba(48, 54, 61, 0.8);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }
    .preview-toolbar-title {
      color: #8b949e;
      font-size: 11.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .theme-switch-group {
      display: flex;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 4px;
      overflow: hidden;
    }
    .theme-tab {
      padding: 4px 12px;
      font-size: 11px;
      cursor: pointer;
      color: #8b949e;
      border: none;
      background: transparent;
    }
    .theme-tab.active {
      background: #21262d;
      color: #f0f6fc;
      font-weight: 600;
    }

    .preview-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 40px 24px;
      display: flex;
      justify-content: center;
      transition: background 0.2s;
    }
    .preview-content {
      width: 100%;
      max-width: 890px;
      color: #c9d1d9;
    }
    .preview-content table {
      width: 100% !important;
      border-collapse: collapse !important;
      margin-bottom: 16px;
    }
    .preview-content td {
      padding: 0 !important;
      border: none !important;
    }
    .preview-content img {
      max-width: 100%;
      height: auto;
      display: block;
    }

    /* Light Mode Preview Simulation */
    .preview-scroll.light-theme {
      background: #ffffff;
    }
    .preview-scroll.light-theme .preview-content {
      color: #24292f;
    }
  </style>
</head>
<body>
  <div class="scanlines"></div>

  <!-- TOP HUD NAVBAR -->
  <header class="hud-nav">
    <div class="brand">
      <span>▶ PIXEL README KIT</span>
      <span class="brand-badge">HUD STUDIO v4.0</span>
    </div>

    <div class="nav-status">
      <div class="status-indicator">
        <span class="pulse-dot"></span>
        <span id="sse-status">LIVE SYNC ACTIVE</span>
      </div>
      <button class="nav-btn" id="btn-debug" onclick="toggleDebugMode()">[ HUD DEBUG ]</button>
      <button class="nav-btn" onclick="triggerRecompile()">⚡ COMPILE NOW</button>
      <a href="https://github.com/Kazinagg/pixel-readme-kit" target="_blank" style="text-decoration:none;">
        <button class="nav-btn">★ GITHUB</button>
      </a>
    </div>
  </header>

  <!-- WORKSPACE -->
  <div class="workspace">
    <!-- LEFT: COMPONENT BUILDER -->
    <aside class="builder-pane">
      <div class="pane-title">
        <span>■ INTERACTIVE BLOCK GENERATOR</span>
        <span id="render-latency" style="color:var(--text-dim);font-size:10px;">0ms</span>
      </div>

      <div class="control-group">
        <label>Block Type</label>
        <select id="sel-type" onchange="onTypeChange()">
          <option value="header">Header Banner</option>
          <option value="metrics">Metrics KPI Card</option>
          <option value="progress">Progress HUD Bar</option>
          <option value="techstack">Tech Stack Matrix</option>
          <option value="timeline">PCB Timeline</option>
          <option value="social">OpenGraph Social Card (1280x640)</option>
          <option value="callout">Callout Alert / Quote</option>
          <option value="frame">Window Frame Cap</option>
          <option value="chip">Holographic Chip</option>
          <option value="divider">Chapter Divider</option>
          <option value="splitter">Sub-Module Splitter</option>
          <option value="footer">Closing Footer Plate</option>
        </select>
      </div>

      <div class="control-row">
        <div class="control-group">
          <label>Style</label>
          <select id="sel-style" onchange="renderCurrentBlock()">
            <option value="cyberpunk">Cyberpunk</option>
            <option value="tactical">Tactical</option>
            <option value="minimal">Minimal Glass</option>
          </select>
        </div>
        <div class="control-group">
          <label>Palette Preset</label>
          <select id="sel-preset" onchange="renderCurrentBlock()">
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
          <select id="sel-mode" onchange="renderCurrentBlock()">
            <option value="auto">Auto (Dark + Light)</option>
            <option value="dark">Dark Only</option>
            <option value="light">Light Only</option>
            <option value="transparent">Transparent</option>
          </select>
        </div>
        <div class="control-group" id="group-compact">
          <label>Layout Mode</label>
          <label class="checkbox-row" style="margin-top:6px;">
            <input type="checkbox" id="chk-compact" onchange="renderCurrentBlock()">
            <span>Compact (Mobile ~84px)</span>
          </label>
        </div>
      </div>

      <!-- DYNAMIC INPUT FIELDS -->
      <div class="control-group" id="group-title">
        <label id="lbl-title">Title <span id="badge-title-budget" class="char-badge badge-optimal">0 chars</span></label>
        <input type="text" id="inp-title" value="PIXEL README KIT" oninput="debounceRender()">
      </div>

      <div class="control-group" id="group-subtitle">
        <label id="lbl-subtitle">Subtitle <span id="badge-sub-budget" class="char-badge badge-optimal">0 chars</span></label>
        <input type="text" id="inp-subtitle" value="RETRO-FUTURISTIC HUD & SCI-FI INFOGRAPHICS" oninput="debounceRender()">
      </div>

      <div class="control-group" id="group-tag">
        <label id="lbl-tag">Tag / Badge</label>
        <input type="text" id="inp-tag" value="SYSTEM_ONLINE" oninput="debounceRender()">
      </div>

      <!-- LIVE PREVIEW & DIRECTIVE -->
      <div class="live-card">
        <div class="pane-title" style="font-size:10.5px; border-bottom:none;">
          <span>LIVE SVG PREVIEW</span>
          <span style="color:var(--amber);">REALTIME</span>
        </div>
        <div class="live-preview-box" id="live-svg-box">
          <div class="debug-grid-overlay" id="hud-debug-grid"></div>
          <div id="svg-render-mount" style="width:100%;display:flex;align-items:center;justify-content:center;"></div>
        </div>

        <div class="pane-title" style="font-size:10.5px; border-bottom:none; margin-top:4px;">
          <span>MARKDOWN DIRECTIVE</span>
        </div>
        <div class="directive-code" id="live-directive"></div>

        <div class="action-btn-row">
          <button class="nav-btn" onclick="copyDirective()">📋 COPY CODE</button>
          <button class="btn-secondary" onclick="insertDirective()">⚡ INSERT TO README</button>
        </div>
      </div>
    </aside>

    <!-- RIGHT: LIVE README PREVIEW -->
    <main class="preview-pane">
      <div class="preview-toolbar">
        <div class="preview-toolbar-title">
          <span>📄 ACTIVE TEMPLATE:</span>
          <strong id="template-filename" style="color:#58a6ff;">README.template.md</strong>
        </div>

        <div class="theme-switch-group">
          <button class="theme-tab active" id="tab-dark" onclick="switchPreviewTheme('dark')">GitHub Dark</button>
          <button class="theme-tab" id="tab-light" onclick="switchPreviewTheme('light')">GitHub Light</button>
        </div>
      </div>

      <div class="preview-scroll" id="preview-scroll-area">
        <div class="preview-content" id="readme-preview-content">
          <!-- Compiled Readme HTML Injected Here -->
        </div>
      </div>
    </main>
  </div>

  <script>
    let renderTimer = null;
    let sseSource = null;
    let debugMode = false;

    function toggleDebugMode() {
      debugMode = !debugMode;
      const box = document.getElementById("live-svg-box");
      const btn = document.getElementById("btn-debug");
      if (debugMode) {
        box.classList.add("debug-active");
        btn.style.background = "var(--amber)";
        btn.style.color = "#000";
        btn.style.borderColor = "var(--amber)";
      } else {
        box.classList.remove("debug-active");
        btn.style.background = "";
        btn.style.color = "";
        btn.style.borderColor = "";
      }
    }

    function updateCharCounters() {
      const title = document.getElementById("inp-title").value || "";
      const sub = document.getElementById("inp-subtitle").value || "";
      const bTitle = document.getElementById("badge-title-budget");
      const bSub = document.getElementById("badge-sub-budget");

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
    }

    function debounceRender() {
      updateCharCounters();
      clearTimeout(renderTimer);
      renderTimer = setTimeout(renderCurrentBlock, 60);
    }

    function onTypeChange() {
      const type = document.getElementById("sel-type").value;
      const grpCompact = document.getElementById("group-compact");
      const lblTitle = document.getElementById("lbl-title");
      const lblSubtitle = document.getElementById("lbl-subtitle");
      const lblTag = document.getElementById("lbl-tag");

      grpCompact.style.display = (type === "header") ? "flex" : "none";

      if (type === "progress") {
        lblTitle.innerText = "Title Label";
        lblSubtitle.innerText = "Subtext Diagnostic";
        lblTag.innerText = "Progress Percentage (0-100)";
        document.getElementById("inp-tag").value = "85";
      } else if (type === "techstack") {
        lblTitle.innerText = "Ignored (Matrix)";
        lblSubtitle.innerText = "Tech items (comma-separated)";
        lblTag.innerText = "Columns count (e.g. 5)";
        document.getElementById("inp-subtitle").value = "python,cpp,rust,docker,git";
        document.getElementById("inp-tag").value = "5";
      } else if (type === "social") {
        lblTitle.innerText = "Main Project Title";
        lblSubtitle.innerText = "Repository Description";
        lblTag.innerText = "Tech Tags (comma-separated)";
        document.getElementById("inp-tag").value = "PYTHON,SVG,CYBERPUNK";
      } else {
        lblTitle.innerText = "Title";
        lblSubtitle.innerText = "Subtitle";
        lblTag.innerText = "Tag / Badge";
      }

      updateCharCounters();
      renderCurrentBlock();
    }

    async function renderCurrentBlock() {
      const t0 = performance.now();
      const btype = document.getElementById("sel-type").value;
      const style = document.getElementById("sel-style").value;
      const preset = document.getElementById("sel-preset").value;
      const mode = document.getElementById("sel-mode").value;
      const compact = document.getElementById("chk-compact").checked;
      const title = document.getElementById("inp-title").value;
      const subtitle = document.getElementById("inp-subtitle").value;
      const tag = document.getElementById("inp-tag").value;

      updateCharCounters();

      // Update markdown directive text
      let directive = `<!-- pixel-kit:${btype} style="${style}" preset="${preset}" mode="${mode}"`;
      if (btype === "header" && compact) directive += ` compact="true"`;
      if (btype === "progress") {
        directive += ` value="${tag}" label="${title}" sub="${subtitle}"`;
      } else if (btype === "techstack") {
        directive += ` items="${subtitle}" columns="${tag}"`;
      } else if (btype === "social") {
        directive += ` title="${title}" subtitle="${subtitle}" tags="${tag}"`;
      } else {
        if (title) directive += ` title="${title}"`;
        if (subtitle) directive += ` subtitle="${subtitle}"`;
        if (tag) directive += ` tag="${tag}"`;
      }
      directive += ` -->`;
      document.getElementById("live-directive").innerText = directive;

      // Fetch rendered SVG from API
      try {
        const params = new URLSearchParams({
          block_type: btype,
          style: style,
          preset: preset,
          mode: mode,
          compact: compact ? "true" : "false",
          title: title,
          subtitle: subtitle,
          tag: tag
        });
        const resp = await fetch(`/api/render?${params.toString()}`);
        if (resp.ok) {
          const svgText = await resp.text();
          document.getElementById("svg-render-mount").innerHTML = svgText;
          const dt = Math.round(performance.now() - t0);
          document.getElementById("render-latency").innerText = `${dt}ms`;
        }
      } catch (err) {
        console.error("Render block error:", err);
      }
    }

    function copyDirective() {
      const code = document.getElementById("live-directive").innerText;
      navigator.clipboard.writeText(code).then(() => {
        alert("Directive copied to clipboard!");
      });
    }

    async function insertDirective() {
      const code = document.getElementById("live-directive").innerText;
      try {
        const resp = await fetch("/api/insert", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ directive: code })
        });
        if (resp.ok) {
          alert("Directive inserted into template and recompiled!");
          loadCompiledPreview();
        }
      } catch (e) {
        alert("Failed to insert directive: " + e);
      }
    }

    function switchPreviewTheme(theme) {
      const scrollArea = document.getElementById("preview-scroll-area");
      const tabDark = document.getElementById("tab-dark");
      const tabLight = document.getElementById("tab-light");

      if (theme === "light") {
        scrollArea.classList.add("light-theme");
        tabLight.classList.add("active");
        tabDark.classList.remove("active");
      } else {
        scrollArea.classList.remove("light-theme");
        tabDark.classList.add("active");
        tabLight.classList.remove("active");
      }
    }

    async function loadCompiledPreview() {
      try {
        const resp = await fetch("/api/preview");
        if (resp.ok) {
          const data = await resp.json();
          document.getElementById("readme-preview-content").innerHTML = data.html;
          document.getElementById("template-filename").innerText = data.filename || "README.template.md";
        }
      } catch (e) {
        console.error("Load preview error:", e);
      }
    }

    async function triggerRecompile() {
      const resp = await fetch("/api/recompile", { method: "POST" });
      if (resp.ok) {
        loadCompiledPreview();
      }
    }

    function initSSE() {
      sseSource = new EventSource("/events");
      sseSource.onopen = () => {
        document.getElementById("sse-status").innerText = "LIVE SYNC ACTIVE";
        document.getElementById("sse-status").style.color = "var(--green)";
      };
      sseSource.onerror = () => {
        document.getElementById("sse-status").innerText = "RECONNECTING...";
        document.getElementById("sse-status").style.color = "var(--amber)";
      };
      sseSource.addEventListener("reload", (e) => {
        console.log("[SSE] File changed, reloading preview...");
        loadCompiledPreview();
      });
    }

    // Init on page load
    window.addEventListener("DOMContentLoaded", () => {
      onTypeChange();
      loadCompiledPreview();
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

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        # 1. Main Studio UI
        if path == "/" or path == "/studio":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
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

            q = threading.Event()
            with self.subscribers_lock:
                self.subscribers.add(self)

            try:
                self.wfile.write(b"data: {\"status\": \"connected\"}\n\n")
                self.wfile.flush()
                while True:
                    time.sleep(1.0)
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
            except (ConnectionResetError, BrokenPipeError):
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
            preset = query.get("preset", [None])[0]
            primary = query.get("primary", [None])[0]
            accent = query.get("accent", [None])[0]
            title = query.get("title", [None])[0]
            subtitle = query.get("subtitle", [None])[0]
            tag = query.get("tag", [None])[0]
            compact = query.get("compact", ["false"])[0].lower() in ("true", "1", "yes")

            try:
                if btype == "header":
                    svg = generate_header(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        title=title or "PIXEL-KIT", subtitle=subtitle or "TRANSLUCENT HUD SYSTEM",
                        tag=tag or "SYSTEM_ACTIVE", compact=compact
                    )
                elif btype == "footer":
                    svg = generate_footer(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        status=title or "SESSION_ACTIVE // STANDBY",
                        nav_text=tag or "RETURN TO TOP", sub_text=subtitle
                    )
                elif btype == "callout":
                    svg = generate_callout(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        title=title or "SYSTEM NOTICE", subtitle=subtitle or ""
                    )
                elif btype == "frame":
                    svg = generate_frame(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        title=title or "SYSTEM.CORE", tag=tag or "[OPEN_HUD]"
                    )
                elif btype == "chip":
                    svg = generate_chip(
                        style=style, mode=mode, preset=preset, primary=primary, accent=accent,
                        text=title or "CHIP"
                    )
                elif btype == "divider":
                    svg = generate_divider(style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "splitter":
                    svg = generate_splitter(style=style, mode=mode, preset=preset, primary=primary, accent=accent, label=title or "[SUB_MODULE]")
                elif btype == "metrics":
                    cards = [{"label": title or "BENCHMARK", "value": subtitle or "1,200+", "delta": tag}]
                    svg = generate_metrics(cards=cards, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "progress":
                    val = int(tag) if tag and tag.isdigit() else 75
                    svg = generate_progress(value=val, label=title or "PROGRESS", sub=subtitle, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "techstack":
                    items = [x.strip() for x in (subtitle or "python,cpp,docker,git").split(",") if x.strip()]
                    cols = int(tag) if tag and tag.isdigit() else 5
                    svg = generate_techstack(items=items, columns=cols, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "timeline":
                    svg = generate_timeline(style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                elif btype == "social":
                    tags = [x.strip() for x in (tag or "PYTHON,SVG").split(",") if x.strip()]
                    svg = generate_social(title=title or "PIXEL README KIT", subtitle=subtitle or "HUD SYSTEM", repo="Kazinagg/pixel-readme-kit", tags=tags, style=style, mode=mode, preset=preset, primary=primary, accent=accent)
                else:
                    self.send_error(400, f"Unsupported block type: {btype}")
                    return

                validate_svg(svg)
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store")
                self.end_headers()
                self.wfile.write(svg.encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Render error: {e}")
                return

        # 4. Preview Compiled Content (/api/preview)
        if path == "/api/preview":
            html_content = self.render_template_to_preview_html()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            resp = {
                "status": "success",
                "filename": self.template_file,
                "html": html_content
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

        # 6. Fallback to standard file serving (assets, svgs, etc.)
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

        self.send_error(404, "Endpoint not found")

    def render_template_to_preview_html(self) -> str:
        """Compiles template and formats markdown into HTML for browser preview."""
        if not os.path.exists(self.template_file):
            return f"<div style='padding:20px;color:#f85149;'>Template file not found: <code>{self.template_file}</code></div>"

        compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=True)
        try:
            with open(self.template_file, "r", encoding="utf-8") as f:
                raw_template = f.read()
            compiled_md = compiler.compile_string(raw_template)

            # Convert markdown elements into browser-friendly HTML
            html = self.markdown_to_html(compiled_md)
            return html
        except Exception as e:
            return f"<div style='padding:20px;color:#f85149;'>Compilation Error: {e}</div>"

    def markdown_to_html(self, md: str) -> str:
        """Lightweight converter for compiled README with 100% full-width table wrappers."""
        import re
        lines = md.split("\n")
        out = []
        in_code_block = False

        for line in lines:
            # Code blocks
            if line.strip().startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    out.append("<pre style='background:#161b22;padding:12px;border-radius:6px;overflow-x:auto;'><code>")
                else:
                    in_code_block = False
                    out.append("</code></pre>")
                continue
            if in_code_block:
                out.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
                continue

            # Preserved HTML (tables, wrappers, divs, images)
            if line.strip().startswith("<"):
                out.append(line)
                continue

            # Headings
            if line.startswith("# "):
                out.append(f"<h1 style='border-bottom:1px solid #30363d;padding-bottom:6px;margin:24px 0 12px 0;'>{line[2:]}</h1>")
            elif line.startswith("## "):
                out.append(f"<h2 style='border-bottom:1px solid #30363d;padding-bottom:4px;margin:20px 0 10px 0;'>{line[3:]}</h2>")
            elif line.startswith("### "):
                out.append(f"<h3 style='margin:16px 0 8px 0;'>{line[4:]}</h3>")
            elif line.strip() == "":
                out.append("<br>")
            else:
                # Markdown links and images
                line_html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" style="max-width:100%;">', line)
                line_html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color:#58a6ff;text-decoration:none;">\1</a>', line_html)
                out.append(f"<p style='margin:6px 0;'>{line_html}</p>")

        return "\n".join(out)

    @classmethod
    def trigger_compile(cls):
        """Forces compilation and notifies all SSE clients."""
        if os.path.exists(cls.template_file):
            compiler = MarkdownCompiler(assets_dir=cls.assets_dir, use_cache=False)
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
                        # File changed, notify studio handler
                        handler_class.trigger_compile()
                except OSError:
                    pass

    t = threading.Thread(target=watcher_loop, daemon=True)
    t.start()
    return t

def run_studio_server(template_path="README.template.md", output_path="README.md",
                      assets_dir="assets/generated", port=3000, open_browser=False):
    """Starts the HUD Studio server and watches the template."""
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
    print(f"[*] ║      PIXEL README KIT // HUD STUDIO LIVE PREVIEW v4.0     ║")
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
