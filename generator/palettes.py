"""
Color themes and translucent palette tokens for Pixel Readme Kit
"""

THEMES = {
    "cyberpunk": {
        "name": "Kazinagg Cyberpunk Core",
        "bg_glass": "rgba(10, 14, 23, 0.82)",
        "bg_panel": "rgba(15, 23, 38, 0.78)",
        "bg_chip": "rgba(0, 200, 215, 0.12)",
        "border_slate": "rgba(30, 41, 59, 0.85)",
        "primary": "#00C8D7",      # Electric Cyan (High contrast on white & dark)
        "primary_glow": "rgba(0, 200, 215, 0.35)",
        "secondary": "#A855F7",    # Neon Cyber Purple
        "secondary_glow": "rgba(168, 85, 247, 0.35)",
        "success": "#00D26A",      # Emerald Green
        "success_glow": "rgba(0, 210, 106, 0.35)",
        "warning": "#F59E0B",      # Cyber Amber Gold
        "warning_glow": "rgba(245, 158, 11, 0.35)",
        "accent": "#FF0055",       # Laser Magenta / Red
        "text_main": "#F8F8F2",
        "text_dim": "#94A3B8",
        "shadow_dark": "#050B14",
        "shadow_mid": "#005577",
    },
    "matrix": {
        "name": "Emerald Matrix Terminal",
        "bg_glass": "rgba(6, 18, 12, 0.82)",
        "bg_panel": "rgba(12, 28, 18, 0.78)",
        "bg_chip": "rgba(0, 210, 106, 0.12)",
        "border_slate": "rgba(20, 45, 25, 0.85)",
        "primary": "#00D26A",      # Matrix Emerald
        "primary_glow": "rgba(0, 210, 106, 0.35)",
        "secondary": "#00E5FF",    # Bright Teal Cyan
        "secondary_glow": "rgba(0, 229, 255, 0.35)",
        "success": "#00D26A",
        "success_glow": "rgba(0, 210, 106, 0.35)",
        "warning": "#EAB308",      # Cyber Yellow
        "warning_glow": "rgba(234, 179, 8, 0.35)",
        "accent": "#FF0055",
        "text_main": "#E8FFE8",
        "text_dim": "#6EE7B7",
        "shadow_dark": "#020A04",
        "shadow_mid": "#0A3D18",
    },
    "amber": {
        "name": "Retro Amber Industrial CRT",
        "bg_glass": "rgba(20, 14, 6, 0.82)",
        "bg_panel": "rgba(30, 22, 10, 0.78)",
        "bg_chip": "rgba(245, 158, 11, 0.12)",
        "border_slate": "rgba(50, 36, 16, 0.85)",
        "primary": "#F59E0B",      # Phosphor Amber
        "primary_glow": "rgba(245, 158, 11, 0.35)",
        "secondary": "#EA580C",    # Phosphor Orange
        "secondary_glow": "rgba(234, 88, 12, 0.35)",
        "success": "#10B981",      # Retro Mint
        "success_glow": "rgba(16, 185, 129, 0.35)",
        "warning": "#D97706",
        "warning_glow": "rgba(217, 119, 6, 0.35)",
        "accent": "#EF4444",       # Signal Red
        "text_main": "#FFFBEB",
        "text_dim": "#FCD34D",
        "shadow_dark": "#0A0702",
        "shadow_mid": "#4A3305",
    },
    "tokyo": {
        "name": "Tokyo Night Vaporwave",
        "bg_glass": "rgba(15, 18, 30, 0.82)",
        "bg_panel": "rgba(22, 27, 46, 0.78)",
        "bg_chip": "rgba(79, 139, 255, 0.12)",
        "border_slate": "rgba(41, 46, 66, 0.85)",
        "primary": "#4F8BFF",      # Tokyo Neon Blue
        "primary_glow": "rgba(79, 139, 255, 0.35)",
        "secondary": "#A855F7",    # Tokyo Neon Purple
        "secondary_glow": "rgba(168, 85, 247, 0.35)",
        "success": "#10B981",
        "success_glow": "rgba(16, 185, 129, 0.35)",
        "warning": "#F59E0B",
        "warning_glow": "rgba(245, 158, 11, 0.35)",
        "accent": "#06B6D4",       # Cyan Accent
        "text_main": "#F1F5F9",
        "text_dim": "#94A3B8",
        "shadow_dark": "#0A0C14",
        "shadow_mid": "#1A2440",
    }
}

# Aliases
THEMES["amber_crt"] = THEMES["amber"]
THEMES["tokyo_night"] = THEMES["tokyo"]

def get_theme(theme_name="cyberpunk"):
    return THEMES.get(theme_name, THEMES["cyberpunk"])
