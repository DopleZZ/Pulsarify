from data_reader import read_z_values, read_text
from text_processor import assign_boldness
from random_boldness import assign_boldness_random
from image_generator import generate_image
import os


def choose_generator():
    print('Выберите генератор:')
    print('1) Детерминуемый (по значениям пульсара)')
    print('2) Случайный (каждой букве назначается случайная жирность)')
    choice = input('Введите 1 или 2 (по умолчанию 1): ').strip()
    return choice


def main():
    z_values = read_z_values()
    text = read_text()

    choice = choose_generator()
    if choice == '2':
        seed_input = input('Ввести целое seed для случайного генератора: ').strip()
        seed = int(seed_input) if seed_input.isdigit() else None
        groups = assign_boldness_random(text, seed=seed)
    else:
        groups = assign_boldness(text, z_values)

    font_dir = 'data/11zon_zip'
    image = generate_image(groups, font_dir)
    image.save('output.png')


if __name__ == '__main__':
    main()