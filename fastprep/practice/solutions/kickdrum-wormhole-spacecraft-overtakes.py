# Map ids to exit ranks, then use prefix maxima and suffix minima to flag every element in an inversion.
from typing import List, Optional, Any


def countCrossingSpacecraft(entryOrder: List[str], exitOrder: List[str]) -> int:
    rank = {name: idx for idx, name in enumerate(exitOrder)}
    p = [rank[name] for name in entryOrder]
    n = len(p)
    if n < 2:
        return 0

    suffix_min = [0] * n
    cur = p[n - 1]
    for i in range(n - 1, -1, -1):
        if p[i] < cur:
            cur = p[i]
        suffix_min[i] = cur

    count = 0
    prefix_max = None
    for i in range(n):
        crossed = False
        if prefix_max is not None and prefix_max > p[i]:
            crossed = True
        elif i + 1 < n and suffix_min[i + 1] < p[i]:
            crossed = True
        if crossed:
            count += 1
        if prefix_max is None or p[i] > prefix_max:
            prefix_max = p[i]
    return count
