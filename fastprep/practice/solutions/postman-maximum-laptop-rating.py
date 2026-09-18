# Sort laptops by price, build a sparse table of rating maxima, binary search each query range.
from typing import List, Optional, Any
from bisect import bisect_left, bisect_right


def maximumRatings(prices: List[int], ratings: List[int], queries: List[List[int]]) -> List[int]:
    n = len(prices)
    if n == 0:
        return [-1] * len(queries)

    order = sorted(range(n), key=lambda i: prices[i])
    sorted_prices = [prices[i] for i in order]
    base = [ratings[i] for i in order]

    # sparse table
    table = [base]
    span = 1
    while span * 2 <= n:
        prev = table[-1]
        cur = [0] * (n - span * 2 + 1)
        for i in range(len(cur)):
            a = prev[i]
            b = prev[i + span]
            cur[i] = a if a > b else b
        table.append(cur)
        span *= 2

    out = []
    for q in queries:
        low, high = q[0], q[1]
        lo = bisect_left(sorted_prices, low)
        hi = bisect_right(sorted_prices, high) - 1
        if lo > hi:
            out.append(-1)
            continue
        length = hi - lo + 1
        k = length.bit_length() - 1
        row = table[k]
        a = row[lo]
        b = row[hi - (1 << k) + 1]
        out.append(a if a > b else b)
    return out
