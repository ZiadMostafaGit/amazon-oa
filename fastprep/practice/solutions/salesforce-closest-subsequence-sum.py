# Values up to 10^7 make a sum-indexed table impossible; n <= 40 allows meet in the middle:
# all subset sums of each half (2^20), sort one, binary-search the best partner for each sum of the other.
from bisect import bisect_left
from typing import List


def _sums(arr):
    out = [0]
    for v in arr:
        out += [s + v for s in out]
    return out


def minAbsDifference(nums: List[int], goal: int) -> int:
    half = len(nums) // 2
    left, right = _sums(nums[:half]), sorted(_sums(nums[half:]))
    best = abs(goal)
    m = len(right)
    for s in left:
        need = goal - s
        i = bisect_left(right, need)
        if i < m:
            best = min(best, right[i] - need)
        if i:
            best = min(best, need - right[i - 1])
        if best == 0:
            return 0
    return best
