# Greedy simulation: walk the evenings, packing as many whole consecutive chapters as fit.
from typing import List, Optional, Any


def solve(chapter: List[int], evening: List[int]) -> int:
    i = 0
    n = len(chapter)
    if n == 0:
        return 0
    for j, minutes in enumerate(evening):
        left = minutes
        while i < n and chapter[i] <= left:
            left -= chapter[i]
            i += 1
        if i == n:
            return j + 1
    return -1
