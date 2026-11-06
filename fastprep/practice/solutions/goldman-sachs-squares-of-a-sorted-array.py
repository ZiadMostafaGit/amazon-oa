from typing import List


def sortedSquares(nums: List[int]) -> List[int]:
    n = len(nums)
    out = [0] * n
    lo, hi = 0, n - 1
    for w in range(n - 1, -1, -1):
        a, b = nums[lo] * nums[lo], nums[hi] * nums[hi]
        if a > b:
            out[w] = a
            lo += 1
        else:
            out[w] = b
            hi -= 1
    return out
