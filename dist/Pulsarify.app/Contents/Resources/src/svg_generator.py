from typing import List, Tuple
import os
import base64
from PIL import Image, ImageDraw, ImageFont

FONT_SIZE = 30
MARGIN = 20
TEXT_COLOR = 'black'
BG_COLOR = 'white'


def _load_fonts(font_dir: str):
    names = ['Thin', 'Light', 'Medium', 'Bold', 'Fat', 'Black']
    fonts = {}
    font_files = {}
    for style in names:
        key = style.lower()
        path = os.path.join(font_dir, f'OOTheranTrial-{style}.otf')
        fonts[key] = ImageFont.truetype(path, FONT_SIZE)
        with open(path, 'rb') as f:
            font_files[key] = f.read()
    return fonts, font_files


def _embed_font_css(font_files: dict) -> str:
    css_parts = []
    for key, data in font_files.items():
        family = f"OOTheran-{key}"
        b64 = base64.b64encode(data).decode('ascii')
        css = (
            f"@font-face {{ font-family: '{family}'; src: url('data:font/otf;base64,{b64}') format('opentype'); }}"
        )
        css_parts.append(css)
    return '\n'.join(css_parts)


def generate_svg(groups: List[Tuple[str, float]], font_dir: str, out_path: str):
    fonts, font_files = _load_fonts(font_dir)

    temp_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_img)

    try:
        max_ascent = max(f.getmetrics()[0] for f in fonts.values())
        max_descent = max(f.getmetrics()[1] for f in fonts.values())
        line_height = max_ascent + max_descent + 8
    except Exception:
        line_height = FONT_SIZE + 12

    x = MARGIN
    y = MARGIN
    max_x = 0
    max_y = 0
    for ch, z in groups:
        if ch == '\n':
            x = MARGIN
            y += line_height
            continue
        font = fonts['thin'] if z < -1 else (
            fonts['light'] if z < 0 else (
                fonts['medium'] if z < 1 else (
                    fonts['bold'] if z < 2 else (
                        fonts['fat'] if z < 3 else fonts['black']))))
        bbox = draw.textbbox((0, 0), ch, font=font)
        cw = bbox[2] - bbox[0]
        max_x = max(max_x, x + cw)
        max_y = max(max_y, y + line_height)
        x += cw

    content_width = int(max_x - MARGIN)
    if content_width < 50:
        content_width = 800
    wrap_width = content_width

    x = MARGIN
    y = MARGIN
    positions = []
    max_x = 0
    max_y = 0
    for ch, z in groups:
        if ch == '\n':
            x = MARGIN
            y += line_height
            positions.append((ch, None, None, None))
            continue
        font_key = 'thin' if z < -1 else (
            'light' if z < 0 else (
                'medium' if z < 1 else (
                    'bold' if z < 2 else (
                        'fat' if z < 3 else 'black'))))
        font = fonts[font_key]
        bbox = draw.textbbox((0, 0), ch, font=font)
        cw = bbox[2] - bbox[0]
        if x + cw > MARGIN + wrap_width:
            x = MARGIN
            y += line_height
        positions.append((ch, x, y, font_key))
        max_x = max(max_x, x + cw)
        max_y = max(max_y, y + line_height)
        x += cw

    width = int(max_x + MARGIN)
    height = int(max_y + 2 * MARGIN)
    final_width = max(width, int(wrap_width + 2 * MARGIN))

    css = _embed_font_css(font_files)
    svg_parts = []
    svg_parts.append(f"<style><![CDATA[{css}]]></style>")
    svg_parts.append(f"<rect width='{final_width}' height='{height}' fill='{BG_COLOR}' />")

    for item in positions:
        ch, px, py, fkey = item
        if ch == '\n':
            continue
        family = f"OOTheran-{fkey}"
        esc = ch.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg_parts.append(
            f"<text x='{px}' y='{py + (line_height - (FONT_SIZE // 4))}' fill='{TEXT_COLOR}' font-family='{family}' font-size='{FONT_SIZE}'>{esc}</text>"
        )

    svg_content = f"<svg xmlns='http://www.w3.org/2000/svg' width='{final_width}' height='{height}'>" + ''.join(svg_parts) + "</svg>"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)