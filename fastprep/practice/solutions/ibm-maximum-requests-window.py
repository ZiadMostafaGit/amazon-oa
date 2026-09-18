# Sliding window over the sorted timestamps, keeping the widest span within [x, x+window-1].
from typing import List, Optional, Any


def maximumRequests(window: int, timestamps: List[int]) -> int:
    ts = sorted(timestamps)
    best = 0
    left = 0
    for right in range(len(ts)):
        while ts[right] - ts[left] > window - 1:
            left += 1
        span = right - left + 1
        if span > best:
            best = span
    return best
