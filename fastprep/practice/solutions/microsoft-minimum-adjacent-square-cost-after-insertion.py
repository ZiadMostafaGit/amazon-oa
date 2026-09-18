# Splitting a gap d optimally costs ceil(d^2/2), so subtract the best floor(d^2/2) saving.
from typing import List, Optional, Any


def minimumSquaredDifferenceCost(values: List[int]) -> int:
    n = len(values)
    if n < 2:
        return 0
    total = 0
    best_saving = 0
    for i in range(1, n):
        d = values[i] - values[i - 1]
        sq = d * d
        total += sq
        saving = sq // 2  # sq - ceil(sq/2)
        if saving > best_saving:
            best_saving = saving
    return total - best_saving
