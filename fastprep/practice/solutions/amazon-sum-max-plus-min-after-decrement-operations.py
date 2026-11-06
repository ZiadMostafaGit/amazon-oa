# Sort descending; level the top group in whole "rounds" with arithmetic series. O(n log n).
from typing import List, Optional, Any


def sumMaxPlusMinAfterOperations(arr: List[int], requests: int) -> int:
    a = sorted(arr, reverse=True)
    n = len(a)
    m = a[-1]
    left = requests
    total = 0
    k = 1          # top k elements are all equal to v
    v = a[0]
    while k < n and a[k] == v:
        k += 1
    while left > 0:
        if k < n:
            rounds = v - a[k]
        else:
            rounds = left // k + 1
        r = min(rounds, left // k)
        if r > 0:
            s = r * v - r * (r - 1) // 2          # sum of v, v-1, ..., v-r+1
            total += k * s
            if k < n:
                total += r * k * m
            else:
                total += s + (k - 1) * (s - r)
            v -= r
            left -= r * k
        if k < n and v == a[k]:
            while k < n and a[k] == v:
                k += 1
            continue
        if left == 0:
            break
        # partial round: left < k ops, all with max v
        p = left
        total += p * v
        if k < n:
            total += p * m
        else:
            total += v + (p - 1) * (v - 1)
        left = 0
    return total
