# Counting sort with values capped at n: bucket[min(r, n)], then scan k from n down with a suffix count. O(n).
from typing import List, Optional, Any


def maximumRatingThreshold(ratings: List[int]) -> int:
    n = len(ratings)
    bucket = [0] * (n + 1)
    for r in ratings:
        bucket[min(r, n)] += 1
    at_least = 0
    for k in range(n, 0, -1):
        at_least += bucket[k]
        if at_least >= k:
            return k
    return 0
