# Prefix sums: subarray (l, r] is flagged iff (P[r]-r) == (P[l]-l) mod k and r-l < k; sliding-window hash counts.
from typing import List, Optional, Any
from collections import defaultdict


def findSecurityLevel(pid: List[int], k: int) -> int:
    n = len(pid)
    # q[i] = (prefix_sum(i) - i) mod k for i in 0..n
    q = [0] * (n + 1)
    running = 0
    for i in range(1, n + 1):
        running += pid[i - 1]
        q[i] = (running - i) % k

    counts = defaultdict(int)
    ans = 0
    for r in range(n + 1):
        drop = r - k
        if drop >= 0:
            counts[q[drop]] -= 1
        ans += counts[q[r]]
        counts[q[r]] += 1
    return ans
