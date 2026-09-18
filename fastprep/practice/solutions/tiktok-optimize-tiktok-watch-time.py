# Scan every unlocked prefix length, adding its unlock cost plus the remaining views at the prefix's cheapest repeat cost.
from typing import List, Optional, Any


def optimizeTikTokWatchTime(n: int, initialWatch: List[int], repeatWatch: List[int], m: int) -> int:
    limit = min(n, m)
    best = None
    unlock = 0
    cheapest = None
    for k in range(1, limit + 1):
        i = k - 1
        unlock += initialWatch[i] + repeatWatch[i]
        r = repeatWatch[i]
        if cheapest is None or r < cheapest:
            cheapest = r
        total = unlock + (m - k) * cheapest
        if best is None or total < best:
            best = total
    return best if best is not None else 0
