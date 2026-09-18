# Reduce to |a-b| <= min(a,b) on absolute values, then count with sorting + two pointers.
from typing import List


def getPerfectPairsCount(arr: List[int]) -> int:
    # For any signs, {|x-y|, |x+y|} == {|a-b|, a+b} where a=|x|, b=|y|.
    # max condition a+b >= max(a,b) always holds; min condition is |a-b| <= min(a,b),
    # i.e. max(a,b) <= 2*min(a,b).
    vals = sorted(abs(v) for v in arr)
    n = len(vals)
    total = 0
    j = 0
    for i in range(n):
        if j < i + 1:
            j = i + 1
        limit = 2 * vals[i]
        while j < n and vals[j] <= limit:
            j += 1
        total += j - (i + 1)
    return total
