# Count descents in the position array of values 1..n: each drop forces a new left-to-right pass.
from typing import List, Optional, Any


def packageSorting(sortingSequence: List[int]) -> int:
    n = len(sortingSequence)
    pos = [0] * (n + 1)
    for i, v in enumerate(sortingSequence):
        pos[v] = i
    ops = 1
    for v in range(2, n + 1):
        if pos[v] < pos[v - 1]:
            ops += 1
    return ops
