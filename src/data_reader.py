import csv

def read_z_values():
    z_values = []
    with open('data/cp1919.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            z_values.append(float(row['z']))
    return z_values

def read_text():
    with open('data/input.txt', 'r') as f:
        return f.read()