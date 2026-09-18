# Approach: greedy - keep equal values contiguous and place the most frequent
# blocks first, so cost = sum(rank * frequency) with frequencies sorted descending.
from typing import List, Optional, Any
from collections import Counter


def minimumDistinctPrefixCost(arr: List[int]) -> int:
    freqs = sorted(Counter(arr).values(), reverse=True)
    total = 0
    for rank, c in enumerate(freqs, start=1):
        total += rank * c
    return total
