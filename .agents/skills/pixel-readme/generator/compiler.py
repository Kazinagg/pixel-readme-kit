"""
Markdown Compiler / Transpiler for Pixel Readme Kit
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

Automatically generates all requested SVGs into --assets-dir, creates proper
100% full-width table wrappers, quote formats, and details/summary blocks,
and outputs the compiled README markdown.
"""

import os
import re
import shlex
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
        # Markdown relative URL
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

    def compile_text(self, markdown_text):
        """Compiles template markdown string into full GitHub markdown with SVGs."""
        os.makedirs(self.assets_dir, exist_ok=True)
        text = markdown_text

        # ---------------------------------------------------------------
        # 1. CONTAINERS: WINDOW
        # <!-- pixel-kit:window style="..." title="..." [tag="..."] [primary="..."] [accent="..."] [out_top="..."] [out_bottom="..."] -->
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

            top_svg = generate_frame(style=style, primary=prim, accent=acc, frame_type="top", title=title, tag=tag)
            bot_svg = generate_frame(style=style, primary=prim, accent=acc, frame_type="bottom", title=title, tag=tag)

            url_top = self._save_svg(top_svg, attrs.get("out_top"), f"frame-top-{style}")
            url_bot = self._save_svg(bot_svg, attrs.get("out_bottom"), f"frame-bottom-{style}")

            if style.lower() == "minimal":
                # Integrated 3-row single table monolith
                return f"""<table width="100%">
<tr>
<td width="100%" align="center">
<img src="{url_top}" width="100%" />
</td>
</tr>
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
<tr>
<td width="100%" align="center">
<img src="{url_bot}" width="100%" />
</td>
</tr>
</table>"""
            else:
                # Direct capping 1-cell table
                return f"""<img src="{url_top}" width="100%" />

<table width="100%">
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
</table>

<img src="{url_bot}" width="100%" />"""

        text = window_regex.sub(repl_window, text)

        # ---------------------------------------------------------------
        # 2. CONTAINERS: TERMINAL (Details/Summary)
        # <!-- pixel-kit:terminal style="..." title="..." [state="open|closed"] [primary="..."] [accent="..."] -->
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

            top_svg = generate_frame(style=style, primary=prim, accent=acc, frame_type="top", title=f"╔═ {title} // RUNTIME.SYS")
            bot_svg = generate_frame(style=style, primary=prim, accent=acc, frame_type="bottom")

            url_top = self._save_svg(top_svg, attrs.get("out_top"), f"terminal-top-{style}")
            url_bot = self._save_svg(bot_svg, attrs.get("out_bottom"), f"terminal-bottom-{style}")

            open_attr = "open" if state == "open" else ""
            status_text = "STATE: EXPANDED" if state == "open" else "CLICK TO EXPAND"

            return f"""<details {open_attr}>
<summary><kbd>▶ {title}</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[{status_text}]</code></summary>

<br/>

<img src="{url_top}" width="100%" />

<table width="100%">
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
</table>

<img src="{url_bot}" width="100%" />

</details>"""

        text = terminal_regex.sub(repl_terminal, text)

        # ---------------------------------------------------------------
        # 3. CONTAINERS: QUOTE CALLOUT
        # <!-- pixel-kit:quote style="..." title="..." [subtitle="..."] [badge="..."] [primary="..."] [accent="..."] -->
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

            q_svg = generate_callout(style=style, primary=prim, accent=acc, callout_type=badge, title=title, subtitle=sub, is_quote=True)
            url_q = self._save_svg(q_svg, attrs.get("out"), f"callout-quote-{style}")

            # Format inner lines with > markdown prefix
            prefixed_lines = "\n".join([f"> {line}" if line.strip() else ">" for line in inner_content.splitlines()])

            return f"""> <img src="{url_q}" width="100%" />
>
{prefixed_lines}"""

        text = quote_regex.sub(repl_quote, text)

        # ---------------------------------------------------------------
        # 4. STANDALONE: HEADER
        # <!-- pixel-kit:header style="..." title="..." subtitle="..." [tag="..."] [primary="..."] [accent="..."] [out="..."] -->
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

            spec1 = attrs.get("spec1", None)
            spec2 = attrs.get("spec2", None)
            spec3 = attrs.get("spec3", None)
            specs = attrs.get("specs", None)

            h_svg = generate_header(
                style=style,
                primary=prim,
                accent=acc,
                title=title,
                subtitle=sub,
                tag=tag,
                spec1=spec1,
                spec2=spec2,
                spec3=spec3,
                specs=specs
            )
            url_h = self._save_svg(h_svg, attrs.get("out"), f"header-{style}")
            return f'<img src="{url_h}" width="100%" alt="{escape_xml(title)}" />'

        text = header_regex.sub(repl_header, text)

        # ---------------------------------------------------------------
        # 5. STANDALONE: FOOTER
        # <!-- pixel-kit:footer style="..." status="..." [nav="..."] [primary="..."] [accent="..."] [out="..."] -->
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

            f_svg = generate_footer(style=style, primary=prim, accent=acc, status=status, nav_text=nav, sub_text=sub)
            url_f = self._save_svg(f_svg, attrs.get("out"), f"footer-{style}")
            return f'<a href="#top"><img src="{url_f}" width="100%" alt="{escape_xml(nav)}" /></a>'

        text = footer_regex.sub(repl_footer, text)

        # ---------------------------------------------------------------
        # 6. STANDALONE: CALLOUT (Autonomous)
        # <!-- pixel-kit:callout style="..." type="..." title="..." [subtitle="..."] [primary="..."] [accent="..."] [out="..."] -->
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

            c_svg = generate_callout(style=style, primary=prim, accent=acc, callout_type=ctype, title=title, subtitle=sub, is_quote=False)
            url_c = self._save_svg(c_svg, attrs.get("out"), f"callout-{style}-{ctype}")
            return f'<img src="{url_c}" width="100%" />'

        text = callout_regex.sub(repl_callout, text)

        # ---------------------------------------------------------------
        # 7. STANDALONE: DIVIDER
        # <!-- pixel-kit:divider style="..." [primary="..."] [accent="..."] [out="..."] -->
        # ---------------------------------------------------------------
        divider_regex = re.compile(r'<!--\s*pixel-kit:divider\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_divider(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)

            d_svg = generate_divider(style=style, primary=prim, accent=acc)
            url_d = self._save_svg(d_svg, attrs.get("out"), f"divider-{style}")
            return f'<img src="{url_d}" width="100%" alt="Divider {style}" />'

        text = divider_regex.sub(repl_divider, text)

        # ---------------------------------------------------------------
        # 8. STANDALONE: SPLITTER
        # <!-- pixel-kit:splitter style="..." label="..." [primary="..."] [accent="..."] [out="..."] -->
        # ---------------------------------------------------------------
        splitter_regex = re.compile(r'<!--\s*pixel-kit:splitter\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_splitter(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            label = attrs.get("label", "[MODULE: SUB_SYSTEM]")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)

            s_svg = generate_splitter(style=style, primary=prim, accent=acc, label=label)
            url_s = self._save_svg(s_svg, attrs.get("out"), f"splitter-{style}")
            return f'<img src="{url_s}" width="100%" />'

        text = splitter_regex.sub(repl_splitter, text)

        # ---------------------------------------------------------------
        # 9. STANDALONE: CHIP
        # <!-- pixel-kit:chip style="..." [type="closed|decay|pulse"] text="..." [primary="..."] [accent="..."] [out="..."] -->
        # ---------------------------------------------------------------
        chip_regex = re.compile(r'<!--\s*pixel-kit:chip\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_chip(m):
            attrs = parse_directive_attrs(m.group(1))
            style = attrs.get("style", "cyberpunk")
            ctype = attrs.get("type", "closed")
            text_val = attrs.get("text", "CHIP")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)

            w_val = int(attrs["width"]) if "width" in attrs and attrs["width"].isdigit() else None
            link_url = attrs.get("url") or attrs.get("href") or attrs.get("link")

            ch_svg = generate_chip(style=style, primary=prim, accent=acc, chip_type=ctype, text=text_val, width=w_val)
            url_ch = self._save_svg(ch_svg, attrs.get("out"), f"chip-{style}-{ctype}")
            img_tag = f'<img src="{url_ch}" alt="{escape_xml(text_val)}" />'
            if link_url:
                return f'<a href="{link_url}">{img_tag}</a>'
            return img_tag

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
