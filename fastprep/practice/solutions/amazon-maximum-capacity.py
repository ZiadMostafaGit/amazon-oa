# Greedy: sort descending and pair adjacent servers, the smaller of each pair being the primary.
from typing import List, Optional, Any


def maximumCapacity(memory: List[int]) -> int:
    vals = sorted(memory, reverse=True)
    total = 0
    for i in range(1, len(vals), 2):
        total += vals[i]
    return total
