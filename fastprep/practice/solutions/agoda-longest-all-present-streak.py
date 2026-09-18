# Linear scan tracking the current run of all-'Y' days and its maximum.
from typing import List


def longestAllPresentStreak(attendance: List[str]) -> int:
    best = 0
    cur = 0
    for day in attendance:
        if 'N' in day:
            cur = 0
        else:
            cur += 1
            if cur > best:
                best = cur
    return best
