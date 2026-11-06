from typing import List, Optional, Any


def threeSum(nums: List[int]) -> List[List[int]]:
    a = sorted(nums)
    n = len(a)
    out = []
    for i in range(n - 2):
        if a[i] > 0:
            break
        if i and a[i] == a[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append([a[i], a[lo], a[hi]])
                lo += 1
                hi -= 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
    return out
