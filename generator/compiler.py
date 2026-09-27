"""
Markdown Compiler / Transpiler for Pixel Readme Kit v3.0
Parses markdown files containing pixel-kit directives:
  <!-- pixel-kit:header ... -->
  <!-- pixel-kit:window ... --> ... <!-- /pixel-kit:window -->
  <!-- pixel-kit:terminal ... --> ... <!-- /pixel-kit:terminal -->
  <!-- pixel-kit:quote ... --> ... <!-- /pixel-kit:quote -->
  <!-- pixel-kit:footer ... -->
  <!-- pixel-kit:callout ... -->
  <!-- pixel-kit:divider ... -->
  <!-- pixel-kit:splitter ... -->
  <!-- pixel-kit:chip ... -->

Supports multi-mode theming:
  mode="auto"        (Default: Single adaptive SVG with CSS @media (prefers-color-scheme: dark))
  mode="dark"        (Always dark palette)
  mode="light"       (Always light palette)
  mode="transparent" (Dark palette with transparent background)
  mode="gh"          (GitHub syntax: generates -dark and -light files, #gh-*-mode-only markup)
  mode="picture"     (HTML5 <picture> tag: generates -dark and -light files)

Automatically generates all requested SVGs into --assets-dir, creates proper
100% full-width table wrappers, quote formats, and details/summary blocks,
and outputs the compiled README markdown.
"""

import os
import re
import json
import urllib.request
from generator.engine import (
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    validate_svg,
    escape_xml
)

_GITHUB_CACHE = {}

def fetch_github_stat(repo, stat_type):
    """
    Fetches real-time repository stats from GitHub REST API:
    - stars -> ('★ 42', 'https://github.com/{repo}/stargazers')
    - forks -> ('🍴 12', 'https://github.com/{repo}/network/members')
    - issues -> ('● ISSUES: 5', 'https://github.com/{repo}/issues')
    - license -> ('⚖ MIT', 'https://github.com/{repo}')
    - watchers -> ('👁 20', 'https://github.com/{repo}/watchers')
    - version / release -> ('v1.0.0', 'https://github.com/{repo}/releases')
    """
    clean_repo = repo.strip().strip("/")
    cache_key = f"{clean_repo}:{stat_type.lower()}"
    if cache_key in _GITHUB_CACHE:
        return _GITHUB_CACHE[cache_key]

    default_links = {
        "stars": f"https://github.com/{clean_repo}/stargazers",
        "forks": f"https://github.com/{clean_repo}/network/members",
        "issues": f"https://github.com/{clean_repo}/issues",
        "watchers": f"https://github.com/{clean_repo}/watchers",
        "license": f"https://github.com/{clean_repo}",
        "version": f"https://github.com/{clean_repo}/releases",
        "release": f"https://github.com/{clean_repo}/releases",
    }
    def_link = default_links.get(stat_type.lower(), f"https://github.com/{clean_repo}")

    def format_count(n):
        if n is None:
            return "--"
        n = int(n)
        if n >= 1000000:
            return f"{n/1000000:.1f}M"
        if n >= 1000:
            return f"{n/1000:.1f}k"
        return str(n)

    st = stat_type.lower()
    try:
        if st in ("version", "release"):
            url = f"https://api.github.com/repos/{clean_repo}/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "Pixel-Readme-Kit/3.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                tag = data.get("tag_name") or data.get("name") or "v1.0"
                res = (str(tag), def_link)
                _GITHUB_CACHE[cache_key] = res
                return res
        else:
            url = f"https://api.github.com/repos/{clean_repo}"
            req = urllib.request.Request(url, headers={"User-Agent": "Pixel-Readme-Kit/3.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())

            if st == "stars":
                count = format_count(data.get("stargazers_count", 0))
                res = (f"★ {count}", def_link)
            elif st == "forks":
                count = format_count(data.get("forks_count", 0))
                res = (f"🍴 {count}", def_link)
            elif st == "issues":
                count = format_count(data.get("open_issues_count", 0))
                res = (f"● ISSUES: {count}", def_link)
            elif st == "watchers":
                count = format_count(data.get("subscribers_count", 0))
                res = (f"👁 {count}", def_link)
            elif st == "license":
                lic = (data.get("license") or {}).get("spdx_id") or "MIT"
                res = (f"⚖ {lic}", def_link)
            else:
                res = (f"{st.upper()}", def_link)

            _GITHUB_CACHE[cache_key] = res
            return res
    except Exception:
        fallback_text = {
            "stars": "★ STARS",
            "forks": "🍴 FORKS",
            "issues": "● ISSUES",
            "license": "⚖ LICENSE",
            "version": "v1.0.0",
            "release": "v1.0.0",
        }.get(st, st.upper())
        res = (fallback_text, def_link)
        _GITHUB_CACHE[cache_key] = res
        return res

def parse_directive_attrs(attr_string):
    """Parses key="value" or key=value attributes from a directive string."""
    attrs = {}
    pattern = re.compile(r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))')
    for m in pattern.finditer(attr_string):
        key = m.group(1).lower()
        val = m.group(2) if m.group(2) is not None else (m.group(3) if m.group(3) is not None else m.group(4))
        attrs[key] = val
    return attrs

class MarkdownCompiler:
    def __init__(self, assets_dir="assets/generated", base_url=""):
        self.assets_dir = assets_dir
        self.base_url = base_url
        self.counters = {}

    def _next_file(self, prefix, ext="svg"):
        count = self.counters.get(prefix, 0) + 1
        self.counters[prefix] = count
        filename = f"{prefix}-{count}.{ext}"
        filepath = os.path.join(self.assets_dir, filename)
        rel_url = os.path.relpath(filepath, ".").replace("\\", "/")
        return filepath, rel_url

    def _save_svg(self, svg_content, custom_out, default_prefix):
        if custom_out:
            filepath = custom_out
            rel_url = custom_out.replace("\\", "/")
        else:
            filepath, rel_url = self._next_file(default_prefix)

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        validate_svg(svg_content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return rel_url

    def _render_asset_markup(self, generator_fn, kwargs, attrs, default_prefix, alt="", is_full_width=True, link=None):
        mode = attrs.get("mode", "auto").lower()
        custom_out = attrs.get("out")

        width_attr = ' width="100%"' if is_full_width else ""
        alt_attr = f' alt="{escape_xml(alt)}"' if alt else ""

        if mode in ("gh", "github"):
            kwargs_dark = dict(kwargs, mode="dark")
            kwargs_light = dict(kwargs, mode="light")
            dark_svg = generator_fn(**kwargs_dark)
            light_svg = generator_fn(**kwargs_light)

            if custom_out:
                base, ext = os.path.splitext(custom_out)
                out_dark = f"{base}-dark{ext}"
                out_light = f"{base}-light{ext}"
            else:
                out_dark = None
                out_light = None

            url_dark = self._save_svg(dark_svg, out_dark, f"{default_prefix}-dark")
            url_light = self._save_svg(light_svg, out_light, f"{default_prefix}-light")

            img_dark = f'<img src="{url_dark}#gh-dark-mode-only"{width_attr}{alt_attr} />'
            img_light = f'<img src="{url_light}#gh-light-mode-only"{width_attr}{alt_attr} />'

            if link:
                img_dark = f'<a href="{link}">{img_dark}</a>'
                img_light = f'<a href="{link}">{img_light}</a>'

            return f"{img_dark}\n{img_light}"

        elif mode == "picture":
            kwargs_dark = dict(kwargs, mode="dark")
            kwargs_light = dict(kwargs, mode="light")
            dark_svg = generator_fn(**kwargs_dark)
            light_svg = generator_fn(**kwargs_light)

            if custom_out:
                base, ext = os.path.splitext(custom_out)
                out_dark = f"{base}-dark{ext}"
                out_light = f"{base}-light{ext}"
            else:
                out_dark = None
                out_light = None

            url_dark = self._save_svg(dark_svg, out_dark, f"{default_prefix}-dark")
            url_light = self._save_svg(light_svg, out_light, f"{default_prefix}-light")

            pic = f"""<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{url_dark}">
  <source media="(prefers-color-scheme: light)" srcset="{url_light}">
  <img src="{url_dark}"{width_attr}{alt_attr} />
</picture>"""
            if link:
                pic = f'<a href="{link}">\n{pic}\n</a>'
            return pic

        else:
            # "auto" (default adaptive), "dark", "light", "transparent"
            kwargs_single = dict(kwargs, mode=mode)
            svg = generator_fn(**kwargs_single)
            url = self._save_svg(svg, custom_out, default_prefix)
            img = f'<img src="{url}"{width_attr}{alt_attr} />'
            if link:
                img = f'<a href="{link}">{img}</a>'
            return img

    def compile_text(self, markdown_text):
        """Compiles template markdown string into full GitHub markdown with SVGs."""
        os.makedirs(self.assets_dir, exist_ok=True)
        text = markdown_text

        # ---------------------------------------------------------------
        # 1. CONTAINERS: WINDOW
        # <!-- pixel-kit:window style="..." title="..." [tag="..."] [primary="..."] [accent="..."] [mode="..."] [out_top="..."] [out_bottom="..."] -->
        # ...
        # <!-- /pixel-kit:window -->
        # ---------------------------------------------------------------
        window_regex = re.compile(
            r'<!--\s*pixel-kit:window\s+(.*?)\s*-->([\s\S]*?)<!--\s*/pixel-kit:window\s*-->',
            re.IGNORECASE
        )

        def repl_window(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style = attrs.get("style", "cyberpunk")
            title = attrs.get("title", "╔═ SYSTEM.CORE // WINDOW.SYS")
            tag = attrs.get("tag", "[OPEN_HUD]")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            attrs_top = dict(attrs)
            if "out_top" in attrs:
                attrs_top["out"] = attrs["out_top"]
            elif "out" in attrs:
                del attrs_top["out"]

            attrs_bot = dict(attrs)
            if "out_bottom" in attrs:
                attrs_bot["out"] = attrs["out_bottom"]
            elif "out" in attrs:
                del attrs_bot["out"]

            rendered_top = self._render_asset_markup(
                generate_frame,
                {"style": style, "primary": prim, "accent": acc, "frame_type": "top", "title": title, "tag": tag, "preset": preset},
                attrs_top,
                f"frame-top-{style}",
                is_full_width=True
            )
            rendered_bot = self._render_asset_markup(
                generate_frame,
                {"style": style, "primary": prim, "accent": acc, "frame_type": "bottom", "title": title, "tag": tag, "preset": preset},
                attrs_bot,
                f"frame-bottom-{style}",
                is_full_width=True
            )

            if style.lower() == "minimal":
                # Integrated 3-row single table monolith
                return f"""<table width="100%">
<tr>
<td width="100%" align="center">
{rendered_top}
</td>
</tr>
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
<tr>
<td width="100%" align="center">
{rendered_bot}
</td>
</tr>
</table>"""
            else:
                # Direct capping 1-cell table
                return f"""{rendered_top}

<table width="100%">
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
</table>

{rendered_bot}"""

        text = window_regex.sub(repl_window, text)

        # ---------------------------------------------------------------
        # 2. CONTAINERS: TERMINAL (Details/Summary)
        # <!-- pixel-kit:terminal style="..." title="..." [state="open|closed"] [primary="..."] [accent="..."] [preset="..."] [mode="..."] -->
        # ...
        # <!-- /pixel-kit:terminal -->
        # ---------------------------------------------------------------
        terminal_regex = re.compile(
            r'<!--\s*pixel-kit:terminal\s+(.*?)\s*-->([\s\S]*?)<!--\s*/pixel-kit:terminal\s*-->',
            re.IGNORECASE
        )

        def repl_terminal(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style = attrs.get("style", "cyberpunk")
            title = attrs.get("title", "HUD.TERMINAL")
            state = attrs.get("state", "open").lower()
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            attrs_top = dict(attrs)
            if "out_top" in attrs:
                attrs_top["out"] = attrs["out_top"]
            elif "out" in attrs:
                del attrs_top["out"]

            attrs_bot = dict(attrs)
            if "out_bottom" in attrs:
                attrs_bot["out"] = attrs["out_bottom"]
            elif "out" in attrs:
                del attrs_bot["out"]

            rendered_top = self._render_asset_markup(
                generate_frame,
                {"style": style, "primary": prim, "accent": acc, "frame_type": "top", "title": f"╔═ {title} // RUNTIME.SYS", "preset": preset},
                attrs_top,
                f"terminal-top-{style}",
                is_full_width=True
            )
            rendered_bot = self._render_asset_markup(
                generate_frame,
                {"style": style, "primary": prim, "accent": acc, "frame_type": "bottom", "preset": preset},
                attrs_bot,
                f"terminal-bottom-{style}",
                is_full_width=True
            )

            open_attr = "open" if state == "open" else ""
            status_text = "STATE: EXPANDED" if state == "open" else "CLICK TO EXPAND"

            return f"""<details {open_attr}>
<summary><kbd>▶ {title}</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[{status_text}]</code></summary>

<br/>

{rendered_top}

<table width="100%">
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
</table>

{rendered_bot}

</details>"""

        text = terminal_regex.sub(repl_terminal, text)

        # ---------------------------------------------------------------
        # 3. CONTAINERS: QUOTE CALLOUT
        # <!-- pixel-kit:quote style="..." title="..." [subtitle="..."] [badge="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] -->
        # ...
        # <!-- /pixel-kit:quote -->
        # ---------------------------------------------------------------
        quote_regex = re.compile(
            r'<!--\s*pixel-kit:quote\s+(.*?)\s*-->([\s\S]*?)<!--\s*/pixel-kit:quote\s*-->',
            re.IGNORECASE
        )

        def repl_quote(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style = attrs.get("style", "cyberpunk")
            title = attrs.get("title", "SPECIFICATION NOTICE")
            sub = attrs.get("subtitle", "Content flows into live blockquote text")
            badge = attrs.get("badge", "NOTE")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            rendered_q = self._render_asset_markup(
                generate_callout,
                {"style": style, "primary": prim, "accent": acc, "callout_type": badge, "title": title, "subtitle": sub, "is_quote": True, "preset": preset},
                attrs,
                f"callout-quote-{style}",
                alt=title,
                is_full_width=True
            )

            quote_header_lines = "\n".join([f"> {line}" for line in rendered_q.splitlines()])
            prefixed_lines = "\n".join([f"> {line}" if line.strip() else ">" for line in inner_content.splitlines()])

            return f"""{quote_header_lines}
>
{prefixed_lines}"""

        text = quote_regex.sub(repl_quote, text)

        # ---------------------------------------------------------------
        # 4. STANDALONE: HEADER
        # <!-- pixel-kit:header style="..." title="..." subtitle="..." [tag="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        header_regex = re.compile(r'<!--\s*pixel-kit:header\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_header(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            title = attrs.get("title", "PIXEL-KIT")
            sub = attrs.get("subtitle", "TRANSLUCENT HUD DESIGN SYSTEM")
            tag = attrs.get("tag", "SYSTEM_ACTIVE")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            spec1 = attrs.get("spec1", None)
            spec2 = attrs.get("spec2", None)
            spec3 = attrs.get("spec3", None)
            specs = attrs.get("specs", None)

            return self._render_asset_markup(
                generate_header,
                {
                    "style": style, "primary": prim, "accent": acc, "title": title,
                    "subtitle": sub, "tag": tag, "spec1": spec1, "spec2": spec2,
                    "spec3": spec3, "specs": specs, "preset": preset
                },
                attrs,
                f"header-{style}",
                alt=title,
                is_full_width=True
            )

        text = header_regex.sub(repl_header, text)

        # ---------------------------------------------------------------
        # 5. STANDALONE: FOOTER
        # <!-- pixel-kit:footer style="..." status="..." [nav="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        footer_regex = re.compile(r'<!--\s*pixel-kit:footer\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_footer(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            status = attrs.get("status", "SYSTEM_ACTIVE // STANDBY")
            nav = attrs.get("nav", "RETURN TO TOP")
            sub = attrs.get("sub") or attrs.get("sub_text") or None
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_footer,
                {"style": style, "primary": prim, "accent": acc, "status": status, "nav_text": nav, "sub_text": sub, "preset": preset},
                attrs,
                f"footer-{style}",
                alt=nav,
                is_full_width=True,
                link="#top"
            )

        text = footer_regex.sub(repl_footer, text)

        # ---------------------------------------------------------------
        # 6. STANDALONE: CALLOUT (Autonomous)
        # <!-- pixel-kit:callout style="..." type="..." title="..." [subtitle="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        callout_regex = re.compile(r'<!--\s*pixel-kit:callout\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_callout(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            ctype = attrs.get("type", "note")
            title = attrs.get("title", "SYSTEM SPECIFICATION")
            sub = attrs.get("subtitle", "")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_callout,
                {"style": style, "primary": prim, "accent": acc, "callout_type": ctype, "title": title, "subtitle": sub, "is_quote": False, "preset": preset},
                attrs,
                f"callout-{style}-{ctype}",
                alt=title,
                is_full_width=True
            )

        text = callout_regex.sub(repl_callout, text)

        # ---------------------------------------------------------------
        # 7. STANDALONE: DIVIDER
        # <!-- pixel-kit:divider style="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        divider_regex = re.compile(r'<!--\s*pixel-kit:divider\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_divider(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_divider,
                {"style": style, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"divider-{style}",
                alt=f"Divider {style}",
                is_full_width=True
            )

        text = divider_regex.sub(repl_divider, text)

        # ---------------------------------------------------------------
        # 8. STANDALONE: SPLITTER
        # <!-- pixel-kit:splitter style="..." label="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        splitter_regex = re.compile(r'<!--\s*pixel-kit:splitter\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_splitter(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            label = attrs.get("label", "[MODULE: SUB_SYSTEM]")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_splitter,
                {"style": style, "primary": prim, "accent": acc, "label": label, "preset": preset},
                attrs,
                f"splitter-{style}",
                alt=label,
                is_full_width=True
            )

        text = splitter_regex.sub(repl_splitter, text)

        # ---------------------------------------------------------------
        # 9. STANDALONE: CHIP
        # <!-- pixel-kit:chip style="..." [type="closed|decay|pulse"] [text="..."] [github="stars|forks|issues|license|watchers|version|release"] [repo="owner/repo"] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        chip_regex = re.compile(r'<!--\s*pixel-kit:chip\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_chip(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            ctype = attrs.get("type", "closed")
            text_val = attrs.get("text", "CHIP")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            w_val = int(attrs["width"]) if "width" in attrs and attrs["width"].isdigit() else None
            link_url = attrs.get("url") or attrs.get("href") or attrs.get("link")

            gh_stat = attrs.get("github") or attrs.get("gh")
            if not gh_stat and "repo" in attrs and text_val.lower() in ("stars", "forks", "issues", "watchers", "license", "version", "release"):
                gh_stat = text_val.lower()

            if gh_stat:
                repo_name = attrs.get("repo", "Kazinagg/pixel-readme-kit")
                stat_text, stat_link = fetch_github_stat(repo_name, gh_stat)
                text_val = stat_text
                if not link_url:
                    link_url = stat_link

            return self._render_asset_markup(
                generate_chip,
                {"style": style, "primary": prim, "accent": acc, "chip_type": ctype, "text": text_val, "width": w_val, "preset": preset},
                attrs,
                f"chip-{style}-{ctype}",
                alt=text_val,
                is_full_width=False,
                link=link_url
            )

        text = chip_regex.sub(repl_chip, text)

        return text

    def compile_file(self, input_filepath, output_filepath):
        """Reads input file, compiles all directives, and writes output file."""
        with open(input_filepath, "r", encoding="utf-8") as f:
            template_content = f.read()

        compiled_content = self.compile_text(template_content)

        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(compiled_content)

        return output_filepath
