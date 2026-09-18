# Monotonic stack: count subarrays whose max sits at the left end + at the right end - both ends.
from typing import List, Optional, Any


def countMaximumProfitableGroups(stockPrice: List[int]) -> int:
    n = len(stockPrice)
    if n == 0:
        return 0

    # A: for each l, number of r >= l such that stockPrice[l] is a maximum of [l..r]
    # -> r goes up to (index of next strictly greater element) - 1
    next_greater = [n] * n
    stack = []
    for i in range(n):
        while stack and stockPrice[stack[-1]] < stockPrice[i]:
            next_greater[stack.pop()] = i
        stack.append(i)
    total_left = 0
    for l in range(n):
        total_left += next_greater[l] - l

    # B: for each r, number of l <= r such that stockPrice[r] is a maximum of [l..r]
    prev_greater = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and stockPrice[stack[-1]] < stockPrice[i]:
            prev_greater[stack.pop()] = i
        stack.append(i)
    total_right = 0
    for r in range(n):
        total_right += r - prev_greater[r]

    # C: subarrays where both ends equal the maximum (counted twice above).
    both = n  # every single-element subarray
    stack = []  # (value, how many live indices with that value visible)
    for x in stockPrice:
        while stack and stack[-1][0] < x:
            stack.pop()
        if stack and stack[-1][0] == x:
            both += stack[-1][1]
            stack[-1][1] += 1
        else:
            stack.append([x, 1])

    return total_left + total_right - both
