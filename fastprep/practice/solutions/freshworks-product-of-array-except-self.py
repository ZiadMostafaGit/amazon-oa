# Prefix and suffix product sweep, no division.
from typing import List, Optional, Any


def productExceptSelf(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [1] * n
    pref = 1
    for i in range(n):
        ans[i] = pref
        pref *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= suf
        suf *= nums[i]
    return ans
