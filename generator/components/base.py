"""
Base utilities for SVG component generation in Pixel Readme Kit.
"""

import html
import xml.etree.ElementTree as ET
from typing import Any


def escape_xml(s: Any) -> str:
    """Escapes strings for safe inclusion in SVG attributes and text nodes."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def validate_svg(svg_content: str) -> bool:
    """Validates that SVG content parses cleanly as XML without errors."""
    try:
        ET.fromstring(svg_content)
        return True
    except ET.ParseError as e:
        raise ValueError(f"Generated SVG has invalid XML syntax: {e}\nSVG Content:\n{svg_content}")
