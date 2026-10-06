"""
Central Theme Registry and Palette Resolver for Pixel Readme Kit.
Acts as Single Source of Truth for base themes, presets, and mode resolution.
"""

import os
import json
from typing import Dict, Any, Optional, Tuple, List
from generator.themes.color_utils import darken_hex, is_light_color
from generator.themes.models import ThemeDefinition


# Built-in handcrafted base themes (guarantees pixel-perfect backward compatibility)
BASE_THEME_PALETTES: Dict[str, Dict[str, Dict[str, str]]] = {
    "cyberpunk": {
        "dark": {
            "bg": "rgba(10, 14, 23, 0.85)",
            "panel": "rgba(15, 23, 38, 0.82)",
            "border": "rgba(30, 41, 59, 0.85)",
            "primary": "#00C8D7",
            "accent": "#A855F7",
            "tertiary": "#FF0055",
            "title_front": "#00C8D7",
            "title_mid": "#006B74",
            "title_dark": "#002B2F",
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#00D26A",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F6F8FA",
            "panel": "#EAEFF5",
            "border": "#D0D7DE",
            "primary": "#0969DA",
            "accent": "#8250DF",
            "tertiary": "#CF222E",
            "title_front": "#0969DA",
            "title_mid": "#0550AE",
            "title_dark": "#033D8B",
            "text_main": "#1F2328",
            "text_dim": "#57606A",
            "success": "#1A7F37",
            "warning": "#9A6700",
            "grid_op": "0.10"
        }
    },
    "tactical": {
        "dark": {
            "bg": "rgba(20, 14, 6, 0.88)",
            "panel": "rgba(30, 22, 10, 0.82)",
            "border": "rgba(50, 36, 16, 0.85)",
            "primary": "#F59E0B",
            "accent": "#EA580C",
            "tertiary": "#EF4444",
            "title_front": "#F59E0B",
            "title_mid": "#92400E",
            "title_dark": "#451A03",
            "text_main": "#FFFBEB",
            "text_dim": "#D97706",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#FFFBEB",
            "panel": "#FEF3C7",
            "border": "#FDE68A",
            "primary": "#B45309",
            "accent": "#C2410C",
            "tertiary": "#B91C1C",
            "title_front": "#B45309",
            "title_mid": "#78350F",
            "title_dark": "#451A03",
            "text_main": "#1F2937",
            "text_dim": "#6B7280",
            "success": "#15803D",
            "warning": "#B45309",
            "grid_op": "0.10"
        }
    },
    "minimal": {
        "dark": {
            "bg": "rgba(15, 18, 30, 0.85)",
            "panel": "rgba(22, 27, 46, 0.80)",
            "border": "rgba(41, 46, 66, 0.85)",
            "primary": "#4F8BFF",
            "accent": "#A855F7",
            "tertiary": "#06B6D4",
            "title_front": "#4F8BFF",
            "title_mid": "#2563EB",
            "title_dark": "#1E3A8A",
            "text_main": "#F1F5F9",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#1D4ED8",
            "accent": "#6D28D9",
            "tertiary": "#0891B2",
            "title_front": "#1D4ED8",
            "title_mid": "#1E40AF",
            "title_dark": "#0F172A",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.10"
        }
    },
    "clean-mono": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.85)",
            "panel": "rgba(30, 41, 59, 0.80)",
            "border": "rgba(51, 65, 85, 0.85)",
            "primary": "#E2E8F0",
            "accent": "#94A3B8",
            "tertiary": "#CBD5E1",
            "title_front": "#F8FAFC",
            "title_mid": "#CBD5E1",
            "title_dark": "#64748B",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FFFFFF",
            "panel": "#F1F5F9",
            "border": "#CBD5E1",
            "primary": "#0F172A",
            "accent": "#475569",
            "tertiary": "#64748B",
            "title_front": "#0F172A",
            "title_mid": "#334155",
            "title_dark": "#64748B",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "corporate-blue": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.88)",
            "panel": "rgba(30, 41, 59, 0.82)",
            "border": "rgba(30, 58, 138, 0.85)",
            "primary": "#38BDF8",
            "accent": "#818CF8",
            "tertiary": "#0284C7",
            "title_front": "#38BDF8",
            "title_mid": "#0284C7",
            "title_dark": "#0369A1",
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#22C55E",
            "warning": "#EAB308",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F0F9FF",
            "panel": "#E0F2FE",
            "border": "#BAE6FD",
            "primary": "#0284C7",
            "accent": "#4F46E5",
            "tertiary": "#0369A1",
            "title_front": "#0369A1",
            "title_mid": "#075985",
            "title_dark": "#0C4A6E",
            "text_main": "#0C4A6E",
            "text_dim": "#0369A1",
            "success": "#16A34A",
            "warning": "#CA8A04",
            "grid_op": "0.08"
        }
    },
    "academic-paper": {
        "dark": {
            "bg": "rgba(24, 24, 27, 0.88)",
            "panel": "rgba(39, 39, 42, 0.82)",
            "border": "rgba(63, 63, 70, 0.85)",
            "primary": "#60A5FA",
            "accent": "#F59E0B",
            "tertiary": "#38BDF8",
            "title_front": "#93C5FD",
            "title_mid": "#3B82F6",
            "title_dark": "#1D4ED8",
            "text_main": "#F4F4F5",
            "text_dim": "#A1A1AA",
            "success": "#10B981",
            "warning": "#D97706",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FAFAF9",
            "panel": "#F5F5F4",
            "border": "#E7E5E4",
            "primary": "#1C1917",
            "accent": "#B45309",
            "tertiary": "#2563EB",
            "title_front": "#1C1917",
            "title_mid": "#44403C",
            "title_dark": "#78716C",
            "text_main": "#1C1917",
            "text_dim": "#78716C",
            "success": "#15803D",
            "warning": "#B45309",
            "grid_op": "0.06"
        }
    },
    "modern-slate": {
        "dark": {
            "bg": "rgba(15, 23, 30, 0.88)",
            "panel": "rgba(22, 33, 46, 0.82)",
            "border": "rgba(30, 41, 59, 0.85)",
            "primary": "#2DD4BF",
            "accent": "#A78BFA",
            "tertiary": "#F43F5E",
            "title_front": "#2DD4BF",
            "title_mid": "#0D9488",
            "title_dark": "#115E59",
            "text_main": "#F1F5F9",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#0F766E",
            "accent": "#6D28D9",
            "tertiary": "#BE123C",
            "title_front": "#0F766E",
            "title_mid": "#115E59",
            "title_dark": "#134E4A",
            "text_main": "#0F172A",
            "text_dim": "#475569",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    }
}

# Standard style and name aliases
THEME_ALIASES: Dict[str, str] = {
    "clean_mono": "clean-mono",
    "corporate_blue": "corporate-blue",
    "academic_paper": "academic-paper",
    "modern_slate": "modern-slate",
    "amber": "tactical",
    "amber_crt": "tactical",
    "matrix": "cyberpunk",
    "tokyo": "minimal",
    "tokyo_night": "minimal",
}


def load_preset(preset_name_or_path: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Loads custom color palette from a JSON file or named preset in presets/.
    Preserves exact backward compatibility with engine.load_preset.
    """
    if not preset_name_or_path:
        return None
    path = str(preset_name_or_path).strip()
    if os.path.isfile(path):
        target_path = path
    else:
        # Search relative to repo root / presets
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cand1 = os.path.join(base_dir, "..", "..", "presets", f"{path}.json")
        cand2 = os.path.join(base_dir, "..", "..", "presets", path)
        cand3 = os.path.join("presets", f"{path}.json")
        cand4 = os.path.join("presets", path)
        if os.path.isfile(cand1):
            target_path = cand1
        elif os.path.isfile(cand2):
            target_path = cand2
        elif os.path.isfile(cand3):
            target_path = cand3
        elif os.path.isfile(cand4):
            target_path = cand4
        elif os.path.isfile(f"{path}.json"):
            target_path = f"{path}.json"
        else:
            return None
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


class ThemeRegistry:
    """Singleton Theme Registry managing all available themes, palettes, and presets."""

    def __init__(self, presets_dir: Optional[str] = None):
        if presets_dir:
            self.presets_dir = presets_dir
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.presets_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "presets"))

        self._palettes: Dict[str, Dict[str, Dict[str, str]]] = {
            k: {m: dict(v[m]) for m in v} for k, v in BASE_THEME_PALETTES.items()
        }
        for alias, target in THEME_ALIASES.items():
            if target in self._palettes:
                self._palettes[alias] = self._palettes[target]

    @property
    def theme_palettes(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Provides direct dictionary access for backward compatibility."""
        return self._palettes

    def list_presets(self) -> List[str]:
        """Returns sorted list of available JSON preset names."""
        if not os.path.isdir(self.presets_dir):
            return sorted(list(BASE_THEME_PALETTES.keys()))
        names = []
        for f in os.listdir(self.presets_dir):
            if f.endswith(".json"):
                names.append(f[:-5])
        return sorted(names) if names else sorted(list(BASE_THEME_PALETTES.keys()))

    def resolve_theme(
        self,
        style: Optional[str] = "cyberpunk",
        mode: str = "auto",
        primary: Optional[str] = None,
        accent: Optional[str] = None,
        preset: Optional[str] = None,
        tertiary: Optional[str] = None,
    ) -> Tuple[Dict[str, str], str]:
        """
        Resolves final theme color dictionary and CSS variables for SVG rendering.
        Fully backward compatible with engine.resolve_theme.
        """
        st = style.lower() if style else "cyberpunk"
        canonical = THEME_ALIASES.get(st, st)
        pal = self._palettes.get(canonical, self._palettes["cyberpunk"])
        dark_vals = dict(pal["dark"])
        light_vals = dict(pal["light"])

        if preset:
            preset_data = load_preset(preset)
            if preset_data:
                p_prim = preset_data.get("primary")
                p_acc = preset_data.get("accent") or preset_data.get("secondary")
                p_tert = preset_data.get("tertiary") or (
                    preset_data.get("accent") if preset_data.get("secondary") else None
                )
                p_succ = preset_data.get("success")
                p_warn = preset_data.get("warning")
                p_bg = preset_data.get("bg_glass") or preset_data.get("bg")
                p_panel = preset_data.get("bg_panel") or preset_data.get("panel")
                p_border = (
                    preset_data.get("border_subtle")
                    or preset_data.get("border_slate")
                    or preset_data.get("border")
                )

                if p_prim and not primary:
                    primary = p_prim
                if p_acc and not accent:
                    accent = p_acc
                if p_tert and not tertiary:
                    tertiary = p_tert
                if p_succ:
                    dark_vals["success"] = p_succ
                    light_vals["success"] = darken_hex(p_succ, 0.7) if is_light_color(p_succ) else p_succ
                if p_warn:
                    dark_vals["warning"] = p_warn
                    light_vals["warning"] = darken_hex(p_warn, 0.7) if is_light_color(p_warn) else p_warn
                if p_bg:
                    dark_vals["bg"] = p_bg
                if p_panel:
                    dark_vals["panel"] = p_panel
                if p_border:
                    dark_vals["border"] = p_border

        if primary:
            dark_vals["primary"] = primary
            dark_vals["title_front"] = primary
            dark_vals["title_mid"] = darken_hex(primary, 0.45)
            dark_vals["title_dark"] = darken_hex(primary, 0.15)
            light_vals["primary"] = darken_hex(primary, 0.7) if is_light_color(primary) else primary
            light_vals["title_front"] = light_vals["primary"]
            light_vals["title_mid"] = darken_hex(light_vals["primary"], 0.6)
            light_vals["title_dark"] = darken_hex(light_vals["primary"], 0.3)

        if accent:
            dark_vals["accent"] = accent
            light_vals["accent"] = darken_hex(accent, 0.7) if is_light_color(accent) else accent

        if tertiary:
            dark_vals["tertiary"] = tertiary
            light_vals["tertiary"] = darken_hex(tertiary, 0.7) if is_light_color(tertiary) else tertiary

        m = mode.lower() if mode else "auto"
        if m == "dark":
            return dark_vals, ""
        elif m == "light":
            return light_vals, ""
        elif m == "transparent":
            res = dict(dark_vals)
            res["bg"] = "none"
            res["panel"] = "none"
            return res, ""
        else:  # "auto" (default: CSS variables + @media)
            colors = {
                "bg": "var(--bg-glass)",
                "panel": "var(--bg-panel)",
                "border": "var(--border-chassis)",
                "primary": "var(--primary)",
                "accent": "var(--accent)",
                "tertiary": "var(--tertiary)",
                "title_front": "var(--title-front)",
                "title_mid": "var(--title-mid)",
                "title_dark": "var(--title-dark)",
                "text_main": "var(--text-main)",
                "text_dim": "var(--text-dim)",
                "success": "var(--status)",
                "warning": "var(--warning)",
                "grid_op": "var(--grid-op)"
            }
            css_vars = f"""
      :root {{
        --bg-glass: {light_vals['bg']};
        --bg-panel: {light_vals['panel']};
        --border-chassis: {light_vals['border']};
        --primary: {light_vals['primary']};
        --accent: {light_vals['accent']};
        --tertiary: {light_vals['tertiary']};
        --title-front: {light_vals['title_front']};
        --title-mid: {light_vals['title_mid']};
        --title-dark: {light_vals['title_dark']};
        --text-main: {light_vals['text_main']};
        --text-dim: {light_vals['text_dim']};
        --status: {light_vals['success']};
        --warning: {light_vals['warning']};
        --grid-op: {light_vals['grid_op']};
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          --bg-glass: {dark_vals['bg']};
          --bg-panel: {dark_vals['panel']};
          --border-chassis: {dark_vals['border']};
          --primary: {dark_vals['primary']};
          --accent: {dark_vals['accent']};
          --tertiary: {dark_vals['tertiary']};
          --title-front: {dark_vals['title_front']};
          --title-mid: {dark_vals['title_mid']};
          --title-dark: {dark_vals['title_dark']};
          --text-main: {dark_vals['text_main']};
          --text-dim: {dark_vals['text_dim']};
          --status: {dark_vals['success']};
          --warning: {dark_vals['warning']};
          --grid-op: {dark_vals['grid_op']};
        }}
      }}
      @media (hover: hover) {{
        .btn-hover:hover, a:hover polygon, a:hover rect {{
          filter: drop-shadow(0 0 6px var(--primary, {dark_vals['primary']}));
          cursor: pointer;
          transition: filter 0.2s ease;
        }}
      }}
"""
            return colors, css_vars

    def resolve_colors(self, style, primary=None, accent=None, mode="auto", preset=None, tertiary=None):
        c, _ = self.resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
        return c["primary"], c["accent"], c.get("tertiary", c["accent"])


# Default singleton instance
theme_registry = ThemeRegistry()
THEME_PALETTES = theme_registry.theme_palettes
STYLE_PALETTES = {k: v["dark"] for k, v in THEME_PALETTES.items()}
resolve_theme = theme_registry.resolve_theme

def resolve_colors(style, primary=None, accent=None, mode="auto", preset=None, tertiary=None):
    c, _ = resolve_theme(style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    return c["primary"], c["accent"], c["bg"]
