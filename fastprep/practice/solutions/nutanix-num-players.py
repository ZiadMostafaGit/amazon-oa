# Scores are 0..100: counting sort into buckets, walk from 100 down; a score's rank is 1 + the number of higher scores. O(n + 100).
from typing import List, Optional, Any


def numPlayers(k: int, scores: List[int]) -> int:
    bucket = [0] * 101
    for s in scores:
        bucket[s] += 1
    higher = 0
    result = 0
    for s in range(100, 0, -1):
        if bucket[s] == 0:
            continue
        if higher + 1 > k:
            break
        result += bucket[s]
        higher += bucket[s]
    return result
