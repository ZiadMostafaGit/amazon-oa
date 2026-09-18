# Sweep line with a difference array over days, then count days hitting the max.
from typing import List, Optional, Any


def maximumUserTraffic(login: List[int], logout: List[int]) -> int:
    n = len(login)
    if n == 0:
        return 0
    lo = min(login)
    hi = max(logout)
    size = hi - lo + 2
    diff = [0] * size
    for i in range(n):
        diff[login[i] - lo] += 1
        diff[logout[i] - lo + 1] -= 1
    best = 0
    count = 0
    cur = 0
    for d in range(size - 1):
        cur += diff[d]
        if cur > best:
            best = cur
            count = 1
        elif cur == best:
            count += 1
    return count
