"""
Color themes and translucent palette tokens for Pixel Readme Kit
"""

THEMES = {
    "cyberpunk": {
        "name": "Kazinagg Cyberpunk Core",
        "bg_glass": "rgba(10, 14, 23, 0.72)",
        "bg_panel": "rgba(15, 23, 38, 0.65)",
        "bg_chip": "rgba(0, 240, 255, 0.08)",
        "border_slate": "rgba(30, 41, 59, 0.85)",
        "primary": "#00F0FF",      # Neon Cyan
        "primary_glow": "rgba(0, 240, 255, 0.35)",
        "secondary": "#BD93F9",    # Neon Purple
        "secondary_glow": "rgba(189, 147, 249, 0.35)",
        "success": "#39FF14",      # Matrix Green
        "success_glow": "rgba(57, 255, 20, 0.35)",
        "warning": "#FFE600",      # Cyber Amber
        "warning_glow": "rgba(255, 230, 0, 0.35)",
        "accent": "#FF0055",       # Signal Magenta / Red
        "text_main": "#F8F8F2",
        "text_dim": "#8892B0",
        "shadow_dark": "#050B14",
        "shadow_mid": "#005577",
    },
    "matrix": {
        "name": "Emerald Matrix Terminal",
        "bg_glass": "rgba(8, 18, 12, 0.75)",
        "bg_panel": "rgba(13, 28, 18, 0.65)",
        "bg_chip": "rgba(57, 255, 20, 0.08)",
        "border_slate": "rgba(20, 45, 25, 0.85)",
        "primary": "#39FF14",
        "primary_glow": "rgba(57, 255, 20, 0.35)",
        "secondary": "#00FF88",
        "secondary_glow": "rgba(0, 255, 136, 0.35)",
        "success": "#39FF14",
        "success_glow": "rgba(57, 255, 20, 0.35)",
        "warning": "#B8FF00",
        "warning_glow": "rgba(184, 255, 0, 0.35)",
        "accent": "#FF3366",
        "text_main": "#E8FFE8",
        "text_dim": "#5C8C65",
        "shadow_dark": "#020A04",
        "shadow_mid": "#0A3D18",
    },
    "amber_crt": {
        "name": "Retro Amber Industrial CRT",
        "bg_glass": "rgba(18, 14, 6, 0.75)",
        "bg_panel": "rgba(28, 20, 8, 0.65)",
        "bg_chip": "rgba(255, 176, 0, 0.08)",
        "border_slate": "rgba(45, 34, 15, 0.85)",
        "primary": "#FFB000",
        "primary_glow": "rgba(255, 176, 0, 0.35)",
        "secondary": "#FFA040",
        "secondary_glow": "rgba(255, 160, 64, 0.35)",
        "success": "#FFD000",
        "success_glow": "rgba(255, 208, 0, 0.35)",
        "warning": "#FF7700",
        "warning_glow": "rgba(255, 119, 0, 0.35)",
        "accent": "#FF3300",
        "text_main": "#FFF0D0",
        "text_dim": "#8C7350",
        "shadow_dark": "#0A0702",
        "shadow_mid": "#4A3305",
    },
    "tokyo_night": {
        "name": "Tokyo Night Vaporwave",
        "bg_glass": "rgba(15, 18, 30, 0.72)",
        "bg_panel": "rgba(22, 27, 46, 0.65)",
        "bg_chip": "rgba(122, 162, 247, 0.08)",
        "border_slate": "rgba(41, 46, 66, 0.85)",
        "primary": "#7AA2F7",
        "primary_glow": "rgba(122, 162, 247, 0.35)",
        "secondary": "#BB9AF7",
        "secondary_glow": "rgba(187, 154, 247, 0.35)",
        "success": "#9ECE6A",
        "success_glow": "rgba(158, 206, 106, 0.35)",
        "warning": "#E0AF68",
        "warning_glow": "rgba(224, 175, 104, 0.35)",
        "accent": "#F7768E",
        "text_main": "#C0CAF5",
        "text_dim": "#565F89",
        "shadow_dark": "#0A0C14",
        "shadow_mid": "#1A2440",
    }
}

def get_theme(theme_name="cyberpunk"):
    return THEMES.get(theme_name, THEMES["cyberpunk"])
