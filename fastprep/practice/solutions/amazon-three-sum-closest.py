# Sort plus two-pointer sweep; on an equal-distance tie keep the smaller sum.
from typing import List, Optional, Any


def solve(nums: List[int], target: int) -> int:
    arr = sorted(nums)
    n = len(arr)
    best = None
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = arr[i] + arr[lo] + arr[hi]
            if best is None:
                best = total
            else:
                d, bd = abs(total - target), abs(best - target)
                if d < bd or (d == bd and total < best):
                    best = total
            if total == target:
                return total
            if total < target:
                lo += 1
            else:
                hi -= 1
    return best
