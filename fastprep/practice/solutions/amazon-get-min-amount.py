# Partition-labels greedy: split into minimal blocks no value crosses, keep the
# most frequent value of each block free and pay for every other product in it.
from typing import List, Optional, Any
from collections import Counter


def solve(quality: List[int]) -> int:
    n = len(quality)
    if n == 0:
        return 0
    last = {}
    for i, v in enumerate(quality):
        last[v] = i

    total_kept = 0
    end = 0
    freq = Counter()
    for i, v in enumerate(quality):
        if last[v] > end:
            end = last[v]
        freq[v] += 1
        if i == end:
            total_kept += max(freq.values())
            freq.clear()
            end = i + 1
    return n - total_kept
