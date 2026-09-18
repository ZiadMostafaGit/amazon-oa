# Greedy interval scheduling: sort by end, take a pair whenever its start beats the last end.
from typing import List, Optional, Any


def maxPairChainLength(pairs: List[List[int]]) -> int:
    count = 0
    cur_end = None
    for start, end in sorted(pairs, key=lambda p: p[1]):
        if cur_end is None or start > cur_end:
            count += 1
            cur_end = end
    return count
