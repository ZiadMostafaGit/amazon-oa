# Iterate over the sparse (nonzero) entries of the shorter side and multiply matching indices.
from typing import List, Optional, Any


def sparseDotProduct(first: List[int], second: List[int]) -> int:
    a = {i: v for i, v in enumerate(first) if v != 0}
    b = {i: v for i, v in enumerate(second) if v != 0}
    if len(b) < len(a):
        a, b = b, a
    total = 0
    for i, v in a.items():
        w = b.get(i)
        if w:
            total += v * w
    return total
