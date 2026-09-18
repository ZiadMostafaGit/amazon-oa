# Partial selection with a heap (heapq.nlargest), keeping duplicate occurrences.
from typing import List, Optional, Any
import heapq


def kLargestIntegers(nums: List[int], k: int) -> List[int]:
    if k <= 0:
        return []
    return heapq.nlargest(k, nums)
