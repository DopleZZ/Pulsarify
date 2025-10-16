import random
from typing import List, Tuple, Optional


def assign_boldness_random(text: str, min_z: float = -2.0, max_z: float = 4.0, seed: Optional[int] = None) -> List[Tuple[str, float]]:

    rnd = random.Random(seed)
    result: List[Tuple[str, float]] = []
    for ch in text:
        z = rnd.uniform(min_z, max_z)
        result.append((ch, z))
    return result
