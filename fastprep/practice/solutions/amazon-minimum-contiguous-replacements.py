# Partition-labels sweep: the most groups possible equals the number of cuts where no value straddles.
from typing import List, Optional, Any


def minOperations(arr: List[int]) -> int:
    last = {}
    for i, v in enumerate(arr):
        last[v] = i
    parts = 0
    end = 0
    for i, v in enumerate(arr):
        if last[v] > end:
            end = last[v]
        if i == end:
            parts += 1
    return len(last) - parts
