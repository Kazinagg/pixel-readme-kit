"""
3D Chunky Pixel Font Engine for Pixel Readme Kit
Supports Cyrillic, Latin, Digits and Symbols.
Renders razor-sharp pixel typography with 3D drop-shadows.
"""

GLYPHS = {
    # Latin
    'A': [".XXXX.", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'B': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'C': [".XXXXX", "XX...X", "XX....", "XX....", "XX....", "XX....", "XX....", "XX...X", ".XXXXX"],
    'D': ["XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'E': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XXXXXX"],
    'F': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XX...."],
    'G': [".XXXXX", "XX...X", "XX....", "XX.XXX", "XX.XXX", "XX..XX", "XX..XX", "XXXXXX", ".XXXX."],
    'H': ["XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'I': ["XXXXXX", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "XXXXXX"],
    'J': ["...XXX", "....XX", "....XX", "....XX", "....XX", "....XX", "XX..XX", "XX..XX", ".XXXX."],
    'K': ["XX...X", "XX..XX", "XX.XX.", "XXXX..", "XXXX..", "XX.XX.", "XX..XX", "XX...X", "XX...X"],
    'L': ["XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XXXXXX"],
    'M': ["XX...XX", "XXX.XXX", "XXXXXXX", "XX.X.XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX"],
    'N': ["XX..XX", "XXX.XX", "XXXXXX", "XX.XXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'O': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    'P': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XX...."],
    'Q': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX.XXX", ".XXXX.", "....XX"],
    'R': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX.XX.", "XX..XX", "XX..XX", "XX...X"],
    'S': [".XXXXX", "XX...X", "XX....", ".XXXX.", ".XXXX.", "....XX", "X...XX", "XX..XX", ".XXXX."],
    'T': ["XXXXXXX", "XXXXXXX", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX.."],
    'U': ["XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    'V': ["XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX.", ".XXXX.", "..XX..", "..XX.."],
    'W': ["XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX.X.XX", "XXXXXXX", "XXX.XXX", "XX...XX", "XX...XX"],
    'X': ["XX..XX", "XX..XX", ".XXXX.", "..XX..", "..XX..", ".XXXX.", "XX..XX", "XX..XX", "XX..XX"],
    'Y': ["XX..XX", "XX..XX", ".XXXX.", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX.."],
    'Z': ["XXXXXX", "XXXXXX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XXXXXX", "XXXXXX"],

    # Cyrillic
    'А': [".XXXX.", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'Б': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'В': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'Г': ["XXXXXX", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX...."],
    'Д': ["..XXXX.", "..XX.XX", "..XX.XX", "..XX.XX", "..XX.XX", "..XX.XX", "XXXXXXXX", "XX....XX", "XX....XX"],
    'Е': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XXXXXX"],
    'Ё': ["..XX..", "XXXXXX", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XXXXXX"],
    'Ж': ["XX.X.XX", "XX.X.XX", ".XXXXX.", "..XXX..", "..XXX..", ".XXXXX.", "XX.X.XX", "XX.X.XX", "XX.X.XX"],
    'З': ["XXXXXX", "....XX", "....XX", "..XXXX", "....XX", "....XX", "....XX", "X...XX", ".XXXX."],
    'И': ["XX..XX", "XX..XX", "XX..XX", "XX.XXX", "XXXXXX", "XXX.XX", "XX..XX", "XX..XX", "XX..XX"],
    'Й': [".XXXX.", "XX..XX", "XX..XX", "XX.XXX", "XXXXXX", "XXX.XX", "XX..XX", "XX..XX", "XX..XX"],
    'К': ["XX...X", "XX..XX", "XX.XX.", "XXXX..", "XXXX..", "XX.XX.", "XX..XX", "XX...X", "XX...X"],
    'Л': ["..XXXX", ".XX.XX", ".XX.XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'М': ["XX...XX", "XXX.XXX", "XXXXXXX", "XX.X.XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX"],
    'Н': ["XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'О': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    'П': ["XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'Р': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XX...."],
    'С': [".XXXXX", "XX...X", "XX....", "XX....", "XX....", "XX....", "XX....", "XX...X", ".XXXXX"],
    'Т': ["XXXXXXX", "XXXXXXX", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX.."],
    'У': ["XX..XX", "XX..XX", "XX..XX", ".XXXXX", "....XX", "....XX", "...XX.", "..XX..", ".XX..."],
    'Ф': ["..XXX..", ".XX.XX.", "XXXXXXX", "XX.X.XX", "XXXXXXX", ".XX.XX.", "..XXX..", "..XXX..", "..XXX.."],
    'Х': ["XX..XX", "XX..XX", ".XXXX.", "..XX..", "..XX..", ".XXXX.", "XX..XX", "XX..XX", "XX..XX"],
    'Ц': ["XX..XX.", "XX..XX.", "XX..XX.", "XX..XX.", "XX..XX.", "XX..XX.", "XXXXXXX", "....XXX", ".....XX"],
    'Ч': ["XX..XX", "XX..XX", "XX..XX", ".XXXXX", "....XX", "....XX", "....XX", "....XX", "....XX"],
    'Ш': ["XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XXXXXXX", "XXXXXXX"],
    'Щ': ["XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XXXXXXXX", "....XXXX", "......XX"],
    'Ъ': ["XXXX...", "..XX...", "..XX...", "..XXXX.", "..XX.XX", "..XX.XX", "..XX.XX", "..XX.XX", "..XXXX."],
    'Ы': ["XX...XX", "XX...XX", "XX...XX", "XXXX.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XXXX.XX"],
    'Ь': ["XX....", "XX....", "XX....", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'Э': [".XXXX.", "XX...X", "....XX", "....XX", "..XXXX", "....XX", "....XX", "XX...X", ".XXXX."],
    'Ю': ["XX.XXXX", "XX.X..X", "XX.X..X", "XXXX..X", "XXXX..X", "XX.X..X", "XX.X..X", "XX.X..X", "XX.XXXX"],
    'Я': [".XXXXX", "XX..XX", "XX..XX", ".XXXXX", ".XXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],

    # Digits
    '0': [".XXXX.", "XX..XX", "XX.XXX", "XX.XXX", "XX..XX", "XXX.XX", "XXX.XX", "XX..XX", ".XXXX."],
    '1': ["..XX..", ".XXX..", "XXXX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "XXXXXX"],
    '2': [".XXXX.", "XX..XX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XXXXXX", "XXXXXX"],
    '3': ["XXXXXX", "....XX", "...XX.", "..XXX.", "...XX.", "....XX", "....XX", "XX..XX", ".XXXX."],
    '4': ["XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "....XX", "....XX", "....XX", "....XX"],
    '5': ["XXXXXX", "XX....", "XX....", "XXXXX.", "....XX", "....XX", "....XX", "XX..XX", ".XXXX."],
    '6': [".XXXX.", "XX..XX", "XX....", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    '7': ["XXXXXX", "XXXXXX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XX....", "XX...."],
    '8': [".XXXX.", "XX..XX", "XX..XX", ".XXXX.", ".XXXX.", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    '9': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", ".XXXXX", "....XX", "....XX", "XX..XX", ".XXXX."],

    # Symbols
    ' ': ["......", "......", "......", "......", "......", "......", "......", "......", "......"],
    '-': ["......", "......", "......", "XXXXXX", "XXXXXX", "......", "......", "......", "......"],
    '_': ["......", "......", "......", "......", "......", "......", "......", "XXXXXX", "XXXXXX"],
    '/': ["....XX", "...XX.", "...XX.", "..XX..", "..XX..", ".XX...", ".XX...", "XX....", "XX...."],
    ':': ["......", "..XX..", "..XX..", "......", "......", "..XX..", "..XX..", "......", "......"],
    '.': ["......", "......", "......", "......", "......", "......", "..XX..", "..XX..", "......"],
}

def matrix_to_rects(matrix, char_symbol, color, px_size, offset_x, offset_y):
    rects = []
    for row_idx, row in enumerate(matrix):
        col_idx = 0
        while col_idx < len(row):
            if row[col_idx] == char_symbol:
                start_col = col_idx
                while col_idx < len(row) and row[col_idx] == char_symbol:
                    col_idx += 1
                run = col_idx - start_col
                x = offset_x + start_col * px_size
                y = offset_y + row_idx * px_size
                w = run * px_size
                h = px_size
                rects.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
            else:
                col_idx += 1
    return "".join(rects)

def render_3d_text(text, x, y, px_size, front_color, mid_shadow, dark_shadow, spacing=2):
    shadow_dark_rects = []
    shadow_mid_rects = []
    front_rects = []

    curr_x = x
    for char in text.upper():
        glyph = GLYPHS.get(char, GLYPHS[' '])
        w = len(glyph[0])
        shadow_dark_rects.append(matrix_to_rects(glyph, 'X', dark_shadow, px_size, curr_x + int(px_size * 1.2), y + int(px_size * 1.2)))
        shadow_mid_rects.append(matrix_to_rects(glyph, 'X', mid_shadow, px_size, curr_x + int(px_size * 0.6), y + int(px_size * 0.6)))
        front_rects.append(matrix_to_rects(glyph, 'X', front_color, px_size, curr_x, y))
        curr_x += (w + spacing) * px_size

    total_width = curr_x - x
    total_height = 9 * px_size + int(px_size * 1.2)

    svg_markup = f"""<g class="pixel-text-3d">
  <!-- Shadow Dark -->
  {''.join(shadow_dark_rects)}
  <!-- Shadow Mid -->
  {''.join(shadow_mid_rects)}
  <!-- Front Face -->
  {''.join(front_rects)}
</g>"""
    return svg_markup, total_width, total_height
