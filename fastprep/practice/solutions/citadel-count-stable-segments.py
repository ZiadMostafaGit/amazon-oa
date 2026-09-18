# Prefix sums plus binary search: interior sums grow strictly, so each left end has at most one candidate right end.
from bisect import bisect_left
from typing import List, Optional, Any


def countStableSegments(capacity: List[int]) -> int:
    n = len(capacity)
    if n < 3:
        return 0
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + capacity[i]
    total = 0
    for l in range(n - 2):
        target = pre[l + 1] + capacity[l]
        r = bisect_left(pre, target, l + 2, n + 1)
        # pre[r] is the prefix ending just before index r, so interior is capacity[l+1..r-1]
        if r <= n and pre[r] == target and r < n and capacity[r] == capacity[l]:
            total += 1
    return total
