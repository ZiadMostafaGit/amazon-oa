# Sort timestamps, then a two-pointer sliding window of span windowSize minutes.
from typing import List, Optional, Any


def maxRequestInWindow(timestamp: List[int], windowSize: int) -> int:
    ts = sorted(timestamp)
    best = 0
    left = 0
    for right in range(len(ts)):
        while ts[right] - ts[left] > windowSize - 1:
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
