# Min-plus convolution of two convex cost curves, done by greedily merging their sorted marginal increments.
from typing import List


def minimumKCapableModelCosts(cost: List[int], featureAvailability: List[str]) -> List[int]:
    n = len(cost)
    both, onlyx, onlyy = [], [], []
    for c, f in zip(cost, featureAvailability):
        a = f[0] == '1'
        b = f[1] == '1'
        if a and b:
            both.append(c)
        elif a:
            onlyx.append(c)
        elif b:
            onlyy.append(c)
    both.sort()
    onlyx.sort()
    onlyy.sort()
    # increments of taking one more "both" model
    inc = list(both)
    # increments of taking one more pair (one x-only + one y-only)
    m = min(len(onlyx), len(onlyy))
    for i in range(m):
        inc.append(onlyx[i] + onlyy[i])
    inc.sort()
    res = [-1] * n
    total = 0
    limit = min(n, len(inc))
    for k in range(1, limit + 1):
        total += inc[k - 1]
        res[k - 1] = total
    return res
