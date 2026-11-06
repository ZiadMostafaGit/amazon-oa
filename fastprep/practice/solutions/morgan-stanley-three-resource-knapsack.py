# 0/1 knapsack with three capacities: the DP state is the remaining (a, b, c); iterate all three downward.
from typing import List


def maximizeKnapsackValue(values: List[int], firstCosts: List[int], secondCosts: List[int], thirdCosts: List[int],
                          firstCapacity: int, secondCapacity: int, thirdCapacity: int) -> int:
    A, B, C = firstCapacity, secondCapacity, thirdCapacity
    best = [[[0] * (C + 1) for _ in range(B + 1)] for _ in range(A + 1)]
    for v, x, y, z in zip(values, firstCosts, secondCosts, thirdCosts):
        if x > A or y > B or z > C:
            continue
        for a in range(A, x - 1, -1):
            pa, cur_a = best[a - x], best[a]
            for b in range(B, y - 1, -1):
                pb, cur_b = pa[b - y], cur_a[b]
                for c in range(C, z - 1, -1):
                    cand = pb[c - z] + v
                    if cand > cur_b[c]:
                        cur_b[c] = cand
    return best[A][B][C]
