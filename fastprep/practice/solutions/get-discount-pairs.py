# Bucket prices by remainder mod x and pair remainder r with x-r.
from typing import List, Optional, Any
from collections import Counter


def getDiscountPairs(x: int, prices: List[int]) -> int:
    counts = Counter(p % x for p in prices)
    total = 0
    for r, c in counts.items():
        comp = (x - r) % x
        if comp == r:
            total += c * (c - 1) // 2
        elif r < comp:
            total += c * counts.get(comp, 0)
    return total
