"""
Themes domain module for Pixel Readme Kit.
Provides theme models, registry, color utilities, and theme creation tools.
"""

from generator.themes.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    hex_to_hsl,
    hsl_to_hex,
    is_light_color,
    darken_hex,
    lighten_hex,
    relative_luminance,
    contrast_ratio,
    get_shadow_colors,
)
from generator.themes.models import ModePalette, ThemeDefinition
from generator.themes.registry import (
    ThemeRegistry,
    theme_registry,
    BASE_THEME_PALETTES,
    THEME_PALETTES,
    STYLE_PALETTES,
    THEME_ALIASES,
    VALID_STYLES,
    STYLE_THEMES,
    load_preset,
    resolve_theme,
    resolve_colors,
    normalize_style_and_theme,
    get_themes_for_style,
)
from generator.themes.creator import ThemeCreator, theme_creator, slugify

__all__ = [
    "hex_to_rgb",
    "rgb_to_hex",
    "hex_to_hsl",
    "hsl_to_hex",
    "is_light_color",
    "darken_hex",
    "lighten_hex",
    "relative_luminance",
    "contrast_ratio",
    "get_shadow_colors",
    "ModePalette",
    "ThemeDefinition",
    "ThemeRegistry",
    "theme_registry",
    "BASE_THEME_PALETTES",
    "THEME_PALETTES",
    "STYLE_PALETTES",
    "THEME_ALIASES",
    "VALID_STYLES",
    "STYLE_THEMES",
    "load_preset",
    "resolve_theme",
    "resolve_colors",
    "normalize_style_and_theme",
    "get_themes_for_style",
    "ThemeCreator",
    "theme_creator",
    "slugify",
]
