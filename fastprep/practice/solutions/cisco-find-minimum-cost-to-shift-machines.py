# Subset-mask DP: partition regions into 3 merged groups (merge cost + one adjust op each).
from typing import List


def findMinimumCostToShiftMachines(machineCount: List[int], finalMachineCount: List[int], shiftingCost: int) -> int:
    n = len(machineCount)
    full = 1 << n

    # sum of machines and number of regions in every subset mask
    total = [0] * full
    size = [0] * full
    for mask in range(1, full):
        low = mask & -mask
        i = low.bit_length() - 1
        rest = mask ^ low
        total[mask] = total[rest] + machineCount[i]
        size[mask] = size[rest] + 1

    INF = float("inf")
    # cost of turning the regions of a mask into one region holding finalMachineCount[j]:
    # (size-1) shift operations to merge them, plus one add/remove operation if the
    # merged total does not already equal the required count.
    cost = [[INF] * full for _ in range(3)]
    for j in range(3):
        want = finalMachineCount[j]
        row = cost[j]
        for mask in range(1, full):
            row[mask] = (size[mask] - 1) * shiftingCost + (0 if total[mask] == want else 1)

    # best[mask] = cheapest way to serve target 2 using some non-empty subset of mask
    best2 = [INF] * full
    row2 = cost[2]
    for mask in range(1, full):
        b = row2[mask]
        m = mask
        while m:
            low = m & -m
            sub = best2[mask ^ low]
            if sub < b:
                b = sub
            m ^= low
        best2[mask] = b

    row0, row1 = cost[0], cost[1]
    ans = INF
    mask0 = 1
    while mask0 < full:
        c0 = row0[mask0]
        if c0 < ans:
            comp0 = (full - 1) ^ mask0
            mask1 = comp0
            while mask1:
                c1 = c0 + row1[mask1]
                if c1 < ans:
                    rest = comp0 ^ mask1
                    if rest:
                        c2 = c1 + best2[rest]
                        if c2 < ans:
                            ans = c2
                mask1 = (mask1 - 1) & comp0
        mask0 += 1

    return int(ans)
