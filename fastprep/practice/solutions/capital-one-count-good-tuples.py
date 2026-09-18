# Sliding window over consecutive triples, counting windows with exactly two distinct-equal values.
from typing import List, Optional, Any


def solution(a: List[int]) -> int:
    n = len(a)
    count = 0
    for i in range(n - 2):
        x, y, z = a[i], a[i + 1], a[i + 2]
        pairs = (x == y) + (y == z) + (x == z)
        if pairs == 1:
            count += 1
    return count
