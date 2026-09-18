# For each operating count k, every robot with threshold < k must operate and none may equal k: sort and count valid k.
from typing import List, Optional, Any
import bisect


def countStableConfigurations(coordinationThreshold: List[int]) -> int:
    n = len(coordinationThreshold)
    t = sorted(coordinationThreshold)
    ans = 0
    for k in range(n + 1):
        lo = bisect.bisect_left(t, k)
        hi = bisect.bisect_right(t, k)
        if lo == k and hi == lo:
            ans += 1
    return ans
