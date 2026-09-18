# Sliding window keeping every id's count at or below the minimum global frequency.
from typing import List, Optional, Any
from collections import Counter


def findConsistentLogs(userEvent: List[int]) -> int:
    total = Counter(userEvent)
    k = min(total.values())

    window = {}
    best = 0
    left = 0
    for right, x in enumerate(userEvent):
        window[x] = window.get(x, 0) + 1
        while window[x] > k:
            window[userEvent[left]] -= 1
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
