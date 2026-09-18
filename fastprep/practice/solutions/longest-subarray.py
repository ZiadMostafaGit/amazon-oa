# Sliding window over positive values: grow right, shrink left while the sum exceeds k.
from typing import List, Optional, Any


def longestSubarray(a: List[int], k: int) -> int:
    best = 0
    total = 0
    left = 0
    for right, value in enumerate(a):
        total += value
        while total > k and left <= right:
            total -= a[left]
            left += 1
        if total <= k:
            best = max(best, right - left + 1)
    return best
