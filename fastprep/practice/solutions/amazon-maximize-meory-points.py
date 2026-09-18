# Exchange argument: read chapters in decreasing order, so value at rank i is counted (n - i) times.
from typing import List, Optional, Any


def maximizeMemoryPoints(memory: List[int]) -> int:
    n = len(memory)
    total = 0
    for i, v in enumerate(sorted(memory, reverse=True)):
        total += (n - i) * v
    return total
