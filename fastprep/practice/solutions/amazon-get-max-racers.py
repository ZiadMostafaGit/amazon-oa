# Sliding window over the occurrence positions of each distinct speed.
from typing import List, Optional, Any
from collections import defaultdict


def getMaxRacers(speed: List[int], k: int) -> int:
    pos = defaultdict(list)
    for i, v in enumerate(speed):
        pos[v].append(i)

    best = 0
    for arr in pos.values():
        l = 0
        for r in range(len(arr)):
            # removals needed = span - kept
            while (arr[r] - arr[l] + 1) - (r - l + 1) > k:
                l += 1
            if r - l + 1 > best:
                best = r - l + 1
    return best
