# Sort, then try every split into two contiguous groups; each group is served best by its median (prefix sums).
from typing import List, Optional, Any


def minSumDistancesToWarehouses(dist_centers: List[int]) -> int:
    a = sorted(dist_centers)
    n = len(a)
    if n <= 2:
        return 0
    pref = [0] * (n + 1)
    for i, v in enumerate(a):
        pref[i + 1] = pref[i] + v

    def cost(i: int, j: int) -> int:
        if i > j:
            return 0
        m = (i + j) // 2
        x = a[m]
        left = x * (m - i + 1) - (pref[m + 1] - pref[i])
        right = (pref[j + 1] - pref[m + 1]) - x * (j - m)
        return left + right

    best = None
    for k in range(n - 1):
        c = cost(0, k) + cost(k + 1, n - 1)
        if best is None or c < best:
            best = c
    return best
