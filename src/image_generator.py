from PIL import Image, ImageDraw, ImageFont
import os

FONT_SIZE = 30
MARGIN = 20
TEXT_COLOR = 'gold'
BG_COLOR = 'black'

def generate_image(groups, font_dir):
    fonts = {
        'thin': ImageFont.truetype(os.path.join(font_dir, 'OOTheranTrial-Thin.otf'), FONT_SIZE),
        'light': ImageFont.truetype(os.path.join(font_dir, 'OOTheranTrial-Light.otf'), FONT_SIZE),
        'medium': ImageFont.truetype(os.path.join(font_dir, 'OOTheranTrial-Medium.otf'), FONT_SIZE),
        'bold': ImageFont.truetype(os.path.join(font_dir, 'OOTheranTrial-Bold.otf'), FONT_SIZE),
        'fat': ImageFont.truetype(os.path.join(font_dir, 'OOTheranTrial-Fat.otf'), FONT_SIZE),
        'black': ImageFont.truetype(os.path.join(font_dir, 'OOTheranTrial-Black.otf'), FONT_SIZE),
    }
    
    def get_font(z):
        if z < -1:
            return fonts['thin']
        elif z < 0:
            return fonts['light']
        elif z < 1:
            return fonts['medium']
        elif z < 2:
            return fonts['bold']
        elif z < 3:
            return fonts['fat']
        else:
            return fonts['black']
    

    line_height = FONT_SIZE + 10

    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    x = MARGIN
    y = MARGIN
    max_x = 0
    max_y = 0
    for char, z in groups:
        font = get_font(z)
        if char == '\n':
            x = MARGIN
            y += line_height
            continue
        bbox = temp_draw.textbbox((0, 0), char, font=font)
        cw = bbox[2] - bbox[0]
        max_x = max(max_x, x + cw)
        max_y = max(max_y, y + line_height)
        x += cw

    width = int(max_x + MARGIN)
    height = int(max_y + 2 * MARGIN)

    tokens = []
    curr = []
    for char, z in groups:
        if char == '\n':
            if curr:
                tokens.append(curr)
                curr = []
            tokens.append('\n')
        elif char == ' ':
            curr.append((char, z))
            tokens.append(curr)
            curr = []
        else:
            curr.append((char, z))
    if curr:
        tokens.append(curr)

    image = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(image)
    x = MARGIN
    y = MARGIN

    for token in tokens:
        if token == '\n':
            x = MARGIN
            y += line_height
            continue

        token_width = 0
        for ch, z in token:
            font = get_font(z)
            bbox = draw.textbbox((0, 0), ch, font=font)
            token_width += bbox[2] - bbox[0]

      
        if x + token_width > width - MARGIN:
            if token_width > (width - 2 * MARGIN):
                for ch, z in token:
                    font = get_font(z)
                    bbox = draw.textbbox((0, 0), ch, font=font)
                    cw = bbox[2] - bbox[0]
                    if x + cw > width - MARGIN:
                        x = MARGIN
                        y += line_height
                    draw.text((x, y), ch, fill=TEXT_COLOR, font=font)
                    x += cw
            else:
                x = MARGIN
                y += line_height
                for ch, z in token:
                    font = get_font(z)
                    bbox = draw.textbbox((0, 0), ch, font=font)
                    cw = bbox[2] - bbox[0]
                    draw.text((x, y), ch, fill=TEXT_COLOR, font=font)
                    x += cw
        else:
            for ch, z in token:
                font = get_font(z)
                bbox = draw.textbbox((0, 0), ch, font=font)
                cw = bbox[2] - bbox[0]
                draw.text((x, y), ch, fill=TEXT_COLOR, font=font)
                x += cw

    return image