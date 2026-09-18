# Reduce to counting pairs of differences with positive sum; sort + two pointers.
from typing import List


def howManyGamesDidTheyWin(n: int, firstTeam: List[int], secondTeam: List[int]) -> int:
    MOD = 10 ** 9 + 7
    diff = sorted(firstTeam[i] - secondTeam[i] for i in range(n))
    count = 0
    lo, hi = 0, n - 1
    while lo < hi:
        if diff[lo] + diff[hi] > 0:
            # every index in (lo, hi] pairs with hi to give a positive sum
            count += hi - lo
            hi -= 1
        else:
            lo += 1
    return count % MOD
