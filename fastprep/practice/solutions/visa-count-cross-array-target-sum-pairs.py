# Hash-map frequency count of the complement value from the second array.
from typing import List, Optional, Any
from collections import Counter


def countCrossArrayTargetSumPairs(first: List[int], second: List[int], target: int) -> int:
    if not first or not second:
        return 0
    freq = Counter(second)
    total = 0
    for value in first:
        total += freq.get(target - value, 0)
    return total
