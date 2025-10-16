from data_reader import read_z_values, read_text
from text_processor import assign_boldness
from random_boldness import assign_boldness_random
from vertical_invert_boldness import assign_boldness_vertical_inverted
from vertical_invert_chaotic import assign_boldness_vertical_chaotic
from image_generator import generate_image

def choose_generator():
    print('генератор:')
    print('1) детерминуемый (по значениям пульсара)')
    print('2) случайный (каждой букве назначается случайная жирность)')
    print('3) вертикальная инверсия (волна по колонкам)')
    print('4) вертикальная инверсия + хаос (как 3, но с шумом)')
    choice = input('1..4 (по умолчанию 1): ').strip()
    return choice


def main():
    z_values = read_z_values()
    text = read_text()

    choice = choose_generator()
    if choice == '2':
        seed_input = input('целое seed для случайного генератора: ').strip()
        seed = int(seed_input) if seed_input.isdigit() else None
        groups = assign_boldness_random(text, seed=seed)
    elif choice == '3':
        groups = assign_boldness_vertical_inverted(text, z_values)
    elif choice == '4':
        seed_input = input('целое seed для детерминированности (или Enter): ').strip()
        seed = int(seed_input) if seed_input.isdigit() else None
        chaos_input = input('интенсивность хаоса 0.0-2.0 (по умолчанию 0.5): ').strip()
        try:
            chaos = float(chaos_input) if chaos_input else 0.5
        except Exception:
            chaos = 0.5
        groups = assign_boldness_vertical_chaotic(text, z_values, seed=seed, chaos=chaos)
    else:
        groups = assign_boldness(text, z_values)

    font_dir = 'data/11zon_zip'
    image = generate_image(groups, font_dir)
    image.save('output.png')


if __name__ == '__main__':
    main()