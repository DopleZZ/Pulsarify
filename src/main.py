from data_reader import read_z_values, read_text
from text_processor import assign_boldness
from image_generator import generate_image
import os

def main():
    z_values = read_z_values()
    text = read_text()
    groups = assign_boldness(text, z_values)
    font_dir = 'data/11zon_zip'
    image = generate_image(groups, font_dir)
    image.save('output.png')

if __name__ == '__main__':
    main()