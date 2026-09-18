# Sort the distinct values, then for each smallest element run a two-pointer scan over the suffix.
from typing import List


def triplets(t: int, d: List[int]) -> int:
    a = sorted(d)
    n = len(a)
    total = 0
    for i in range(n - 2):
        budget = t - a[i]
        if a[i + 1] + a[i + 2] > budget:
            break  # values only grow from here, so no later i can work either
        m = n - 1 - i
        if a[n - 2] + a[n - 1] <= budget:
            total += m * (m - 1) // 2  # every pair in the suffix fits
            continue
        lo = i + 1
        hi = n - 1
        while lo < hi:
            if a[lo] + a[hi] <= budget:
                total += hi - lo
                lo += 1
            else:
                hi -= 1
    return total
