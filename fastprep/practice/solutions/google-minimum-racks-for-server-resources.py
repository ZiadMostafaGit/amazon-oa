# Bitmask DP over subsets: partition servers into the fewest feasible racks (submask enumeration).
from typing import List, Optional, Any


def minimumRacks(bandwidth: List[int], power: List[int], rackBandwidthCapacity: int, rackPowerCapacity: int) -> int:
    n = len(bandwidth)
    if n == 0:
        return 0
    full = (1 << n) - 1
    sb = [0] * (1 << n)
    sp = [0] * (1 << n)
    feasible = [False] * (1 << n)
    feasible[0] = True
    for mask in range(1, 1 << n):
        low = mask & -mask
        i = low.bit_length() - 1
        rest = mask ^ low
        sb[mask] = sb[rest] + bandwidth[i]
        sp[mask] = sp[rest] + power[i]
        feasible[mask] = sb[mask] <= rackBandwidthCapacity and sp[mask] <= rackPowerCapacity

    INF = n + 1
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        low = mask & -mask
        # force the lowest set bit into the rack we are forming, to avoid duplicate work
        sub = mask
        best = INF
        while sub:
            if sub & low and feasible[sub]:
                cand = dp[mask ^ sub]
                if cand + 1 < best:
                    best = cand + 1
            sub = (sub - 1) & mask
        dp[mask] = best
    return dp[full]
