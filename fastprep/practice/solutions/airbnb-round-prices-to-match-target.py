# Greedy: start from all floors, then round up the largest fractional parts (ties by smaller index).
import math
from typing import List, Optional, Any


def roundPricesToMatchTarget(prices: List[float], target: int) -> List[int]:
    n = len(prices)
    result = [0] * n
    fracs = []
    total = 0
    for i, p in enumerate(prices):
        f = math.floor(p)
        result[i] = f
        total += f
        frac = p - f
        if frac > 0:
            fracs.append((-frac, i))
    need = target - total
    if need < 0 or need > len(fracs):
        return []
    fracs.sort()
    for j in range(need):
        result[fracs[j][1]] += 1
    return result
