from PIL import Image, ImageDraw, ImageFont
import os

FONT_SIZE = 30
MARGIN = 20

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
    
    # First pass: calculate required size
    x, y = MARGIN, MARGIN
    line_height = FONT_SIZE + 10
    max_x, max_y = 0, 0
    for char, z in groups:
        font = get_font(z)
        if char == '\n':
            x = MARGIN
            y += line_height
            continue
        char_width = font.getbbox(char)[2]
        max_x = max(max_x, x + char_width)
        max_y = max(max_y, y + line_height)
        x += char_width
    width = int(max_x + MARGIN)
    height = int(max_y + 2 * MARGIN)
    
    # Second pass: draw
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    x, y = MARGIN, MARGIN
    for char, z in groups:
        font = get_font(z)
        if char == '\n':
            x = MARGIN
            y += line_height
            continue
        bbox = draw.textbbox((x, y), char, font=font)
        if x + (bbox[2] - bbox[0]) > width - MARGIN:
            x = MARGIN
            y += line_height
        draw.text((x, y), char, fill='black', font=font)
        x += bbox[2] - bbox[0]
    return image