STEP = 3

def assign_boldness(text, z_values):
    result = []
    for i, char in enumerate(text):
        z_index = i // STEP
        if z_index < len(z_values):
            z = z_values[z_index]
        else:
            z = 0
        result.append((char, z))
    return result