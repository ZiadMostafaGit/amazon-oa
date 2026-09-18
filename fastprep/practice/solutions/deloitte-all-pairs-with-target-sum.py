# Value-frequency counting: group equal values and emit each complementary pair with its multiplicity.
from typing import List, Optional, Any
from collections import Counter


def allPairsWithTargetSum(numbers: List[int], target: int) -> List[List[int]]:
    counts = Counter(numbers)
    result: List[List[int]] = []
    for a in sorted(counts):
        b = target - a
        if b < a:
            continue
        if b == a:
            n = counts[a]
            times = n * (n - 1) // 2
        else:
            if b not in counts:
                continue
            times = counts[a] * counts[b]
        for _ in range(times):
            result.append([a, b])
    return result
