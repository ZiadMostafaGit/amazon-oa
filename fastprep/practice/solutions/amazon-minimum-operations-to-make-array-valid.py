# Partition-labels sweep: each merge group must be a maximal contiguous segment, so answer = distinct - max segments.
from typing import List, Optional, Any


def minimumOperationsToMakeArrayValid(arr: List[int]) -> int:
    last = {}
    for i, v in enumerate(arr):
        last[v] = i
    distinct = len(last)
    segments = 0
    end = -1
    for i, v in enumerate(arr):
        if last[v] > end:
            end = last[v]
        if i == end:
            segments += 1
    return distinct - segments
