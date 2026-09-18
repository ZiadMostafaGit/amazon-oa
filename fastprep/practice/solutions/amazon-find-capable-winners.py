# Sort each player's three boosters; X beats Y iff X.max > Y.mid and X.mid > Y.min, so compare
# each player against the global top-2 of mids and top-2 of mins (to exclude self) in O(n log n).
from typing import List


def findCapableWinners(power_a: List[int], power_b: List[int], power_c: List[int]) -> int:
    n = len(power_a)
    if n <= 1:
        return n

    mids = []
    mins = []
    maxs = []
    for i in range(n):
        t = sorted((power_a[i], power_b[i], power_c[i]), reverse=True)
        maxs.append(t[0])
        mids.append(t[1])
        mins.append(t[2])

    def top2(vals):
        best = second = float('-inf')
        for v in vals:
            if v > best:
                second = best
                best = v
            elif v > second:
                second = v
        return best, second

    mid1, mid2 = top2(mids)
    min1, min2 = top2(mins)

    count = 0
    for i in range(n):
        # best mid / best min among all players other than i
        other_mid = mid2 if mids[i] == mid1 else mid1
        other_min = min2 if mins[i] == min1 else min1
        # careful: ties -- if mids[i] equals mid1 but another player also has mid1,
        # then mid2 == mid1 and the value is still correct.
        if maxs[i] > other_mid and mids[i] > other_min:
            count += 1
    return count
