"""
HUD Studio HTTP Server for Pixel Readme Kit.
Handles live browser preview, template editing API, theme creation, and asset compilation.
"""

import os
import sys
import json
import time
import re
import threading
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from generator.compiler import MarkdownCompiler
from generator.studio.handlers import (
    handle_render_request,
    extract_template_blocks,
    apply_global_theme_to_content,
    render_preview_html,
    markdown_to_html,
    handle_presets_list,
    handle_themes_list,
    handle_theme_generate,
    handle_theme_save,
    handle_git_push,
)

STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(STUDIO_DIR, "..", ".."))
STATIC_DIR = os.path.join(STUDIO_DIR, "static")

# Load STUDIO_HTML from static/index.html (inlining CSS and JS for 100% standalone reliability)
def _load_studio_html() -> str:
    html_path = os.path.join(STATIC_DIR, "index.html")
    css_path = os.path.join(STATIC_DIR, "css", "studio.css")
    js_path = os.path.join(STATIC_DIR, "js", "app.js")
    ts_js_path = os.path.join(STATIC_DIR, "js", "theme_studio.js")

    if os.path.isfile(html_path) and os.path.isfile(css_path) and os.path.isfile(js_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        with open(js_path, "r", encoding="utf-8") as f:
            js = f.read()
        ts_js = ""
        if os.path.isfile(ts_js_path):
            with open(ts_js_path, "r", encoding="utf-8") as f:
                ts_js = f.read()

        # Inline stylesheet and script so the studio HTML is completely self-contained
        html = html.replace('<link rel="stylesheet" href="/static/css/studio.css">', f"<style>\n{css}\n</style>")
        html = html.replace('<script src="/static/js/app.js"></script>', f"<script>\n{js}\n</script>")
        if ts_js:
            html = html.replace('<script src="/static/js/theme_studio.js"></script>', f"<script>\n{ts_js}\n</script>")
        return html
    return "<html><body>HUD Studio static assets not found</body></html>"

STUDIO_HTML = _load_studio_html()


class StudioRequestHandler(SimpleHTTPRequestHandler):
    """Handles HUD Studio API, static asset requests, and interactive editing."""

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

        # 2. Static Assets Serving (/static/*)
        if path.startswith("/static/"):
            rel_path = path[len("/static/"):].lstrip("/")
            file_path = os.path.join(STATIC_DIR, rel_path)
            if os.path.isfile(file_path):
                content_type = "text/plain"
                if file_path.endswith(".css"):
                    content_type = "text/css; charset=utf-8"
                elif file_path.endswith(".js"):
                    content_type = "application/javascript; charset=utf-8"
                elif file_path.endswith(".html"):
                    content_type = "text/html; charset=utf-8"
                with open(file_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(data)
                return

        # 3. Server-Sent Events (SSE) Live Reload channel
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

        # 4. Dynamic SVG Render API (/api/render)
        if path == "/api/render":
            handle_render_request(self, query)
            return

        # 5. Preview Compiled Content (/api/preview)
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

        # 6. List Presets and Icons (/api/presets)
        if path == "/api/presets":
            handle_presets_list(self)
            return

        # 7. List Detailed Themes (/api/themes)
        if path == "/api/themes":
            handle_themes_list(self)
            return

        # 8. Extract Blocks from Template (/api/template/blocks)
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

        # 9. Static SVG File Serving with Theme Adaptability
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
                        svg_data = re.sub(r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{[\s\S]*?\}\s*\}', '', svg_data)
                    elif req_theme == "dark":
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

        # 10. Fallback to standard file serving
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

        if path == "/api/template/apply_global_theme":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req = json.loads(body)
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()

                updated_content = apply_global_theme_to_content(content, req)
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

        # New Theme API routes
        if path == "/api/themes/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length).decode("utf-8")) if content_length > 0 else {}
            handle_theme_generate(self, body)
            return

        if path == "/api/themes/save":
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length).decode("utf-8")) if content_length > 0 else {}
            handle_theme_save(self, body)
            return

        if path == "/api/git/push_readme":
            handle_git_push(self)
            return

        self.send_error(404, "Endpoint not found")

    def render_template_to_preview_html(self, preview_theme: str = "auto", view_mode: bool = False) -> str:
        """Compiles template and formats markdown into HTML for browser preview."""
        return render_preview_html(self.template_file, self.assets_dir, preview_theme, view_mode)

    @classmethod
    def markdown_to_html(cls, *args, **kwargs) -> str:
        """Converts Markdown text to HTML using GFM renderer."""
        return markdown_to_html(*args, **kwargs)

    @classmethod
    def _fallback_markdown_to_html(cls, md: str) -> str:
        from generator.studio.handlers.template_handler import _fallback_markdown_to_html
        return _fallback_markdown_to_html(md)

    @classmethod
    def _format_inline_md(cls, text: str) -> str:
        from generator.studio.handlers.template_handler import _format_inline_md
        return _format_inline_md(text)

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

    if os.path.exists(template_path):
        compiler = MarkdownCompiler(assets_dir=assets_dir, use_cache=True)
        compiler.compile_file(template_path, output_path)

    start_file_watcher(template_path, StudioRequestHandler)

    server = ThreadedStudioServer(("127.0.0.1", port), StudioRequestHandler)
    url = f"http://localhost:{port}/"
    print(f"[*] ╔═══════════════════════════════════════════════════════════╗")
    print(f"[*] ║      PIXEL README KIT // HUD STUDIO LIVE PREVIEW v5.0     ║")
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
