from typing import List, Tuple

STEP = 3

def assign_boldness_vertical_inverted(text: str, z_values: List[float], step: int = STEP) -> List[Tuple[str, float]]:
    lines = text.split('\n')
    max_len = max((len(line) for line in lines), default=0)
    positions = []
    for col in range(max_len):
        for row in range(len(lines)):
            if col < len(lines[row]):
                positions.append((row, col))

    result_map = {(r, c): (lines[r][c]) for r in range(len(lines)) for c in range(len(lines[r]))}
    result: List[Tuple[str, float]] = []

    idx = 0
    assigned = {}
    for pos in positions:
        r, c = pos
        z_index = idx // step
        base = z_values[z_index] if z_index < len(z_values) else 0
        z_inv = -base
        if max_len <= 1:
            factor = 1.0
        else:
            mid = (max_len - 1) / 2.0
            dist = abs(c - mid)
            factor = dist / mid
        assigned[(r, c)] = z_inv * factor
        idx += 1

    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            z = assigned.get((r, c), 0.0)
            result.append((ch, z))
        if r != len(lines) - 1:
            result.append(("\n", 0.0))
    return result
