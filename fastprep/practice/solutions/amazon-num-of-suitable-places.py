# Convex cost: binary search the leftmost and rightmost integer x whose sum of distances fits the budget.
from bisect import bisect_left
from typing import List


def numberOfSuitablePlaces(center: List[int], d: int) -> int:
    LO, HI = -10 ** 9, 10 ** 9
    c = sorted(center)
    n = len(c)
    pre = [0] * (n + 1)
    for i, v in enumerate(c):
        pre[i + 1] = pre[i] + v
    budget = d // 2  # 2 * sum|x - c| <= d

    def cost(x: int) -> int:
        j = bisect_left(c, x)
        left = x * j - pre[j]
        right = (pre[n] - pre[j]) - x * (n - j)
        return left + right

    med = c[n // 2]
    if med < LO:
        med = LO
    elif med > HI:
        med = HI
    if cost(med) > budget:
        return 0

    # leftmost feasible point in [LO, med]
    lo, hi = LO, med
    while lo < hi:
        mid = (lo + hi) // 2
        if cost(mid) <= budget:
            hi = mid
        else:
            lo = mid + 1
    left_end = lo

    # rightmost feasible point in [med, HI]
    lo, hi = med, HI
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    right_end = lo
    return right_end - left_end + 1
