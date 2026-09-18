# Sliding window of size k with a hash-map count of values currently in the window.
from typing import List, Optional, Any
from collections import defaultdict


def countEqualCodePairs(code: List[int], k: int) -> int:
    if k <= 0:
        return 0
    counts = defaultdict(int)
    total = 0
    left = 0
    for right, value in enumerate(code):
        # keep only indices in [right-k, right-1] inside the window
        while left < right - k:
            counts[code[left]] -= 1
            left += 1
        total += counts[value]
        counts[value] += 1
    return total
