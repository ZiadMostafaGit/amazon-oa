# Greedy interval jump: best reach per start index, then minimum-jumps sweep.
from typing import List, Optional, Any


def minTaps(n: int, ranges: List[int]) -> int:
    far = [0] * (n + 1)
    for i, r in enumerate(ranges):
        if r <= 0:
            continue
        left = i - r
        if left < 0:
            left = 0
        right = i + r
        if right > n:
            right = n
        if right > far[left]:
            far[left] = right
    taps = 0
    covered = 0
    reach = 0
    i = 0
    while covered < n:
        while i <= covered:
            if far[i] > reach:
                reach = far[i]
            i += 1
        if reach <= covered:
            return -1
        covered = reach
        taps += 1
    return taps
