# Cost(k) = min over t (pairs of single-feature models) of prefC[k-t] + prefA[t] + prefB[t]; the function is convex in t, so binary search the discrete derivative.
from typing import List, Optional, Any


def getMinimumModelCosts(cost: List[int], featureAvailability: List[str]) -> List[int]:
    n = len(cost)
    only_a = []
    only_b = []
    both = []
    for c, f in zip(cost, featureAvailability):
        if f == "10":
            only_a.append(c)
        elif f == "01":
            only_b.append(c)
        elif f == "11":
            both.append(c)
    only_a.sort()
    only_b.sort()
    both.sort()

    def prefix(arr):
        out = [0] * (len(arr) + 1)
        run = 0
        for i, v in enumerate(arr):
            run += v
            out[i + 1] = run
        return out

    pa = prefix(only_a)
    pb = prefix(only_b)
    pc = prefix(both)
    na, nb, nc = len(only_a), len(only_b), len(both)

    ans = []
    for k in range(1, n + 1):
        lo = max(0, k - nc)
        hi = min(k, na, nb)
        if lo > hi:
            ans.append(-1)
            continue

        def f(t):
            return pc[k - t] + pa[t] + pb[t]

        a, b = lo, hi
        while a < b:
            mid = (a + b) // 2
            if f(mid + 1) < f(mid):
                a = mid + 1
            else:
                b = mid
        ans.append(f(a))
    return ans
