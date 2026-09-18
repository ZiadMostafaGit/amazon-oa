# Greedy/counting: answer is max(most frequent location count, ceil(n/2)).
from typing import List, Optional, Any
from collections import Counter


def minOperation(m: int, locations: List[int]) -> int:
    n = len(locations)
    if n == 0:
        return 0
    best = max(Counter(locations).values())
    return max(best, (n + 1) // 2)
