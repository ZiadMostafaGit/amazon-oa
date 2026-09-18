# Shift b by the forced positive increments: the constraints collapse to non-decreasing sequences in [0,T], i.e. C(n+T, n).
from typing import List, Optional, Any

MOD = 1000000007


def countPerfectBreaks(arr: List[int]) -> int:
    n = len(arr)
    # forced growth of b: b[i] - b[i-1] >= max(0, arr[i]-arr[i-1])
    forced = 0
    for i in range(1, n):
        diff = arr[i] - arr[i - 1]
        if diff > 0:
            forced += diff
    # after removing the forced growth every cap collapses to this single value
    top = arr[n - 1] - forced
    if top < 0:
        return 0
    # C(n + top, n) mod MOD
    k = n
    total = n + top
    num = 1
    den = 1
    if k > total - k:
        k = total - k
    for i in range(1, k + 1):
        num = num * ((total - k + i) % MOD) % MOD
        den = den * i % MOD
    return num * pow(den, MOD - 2, MOD) % MOD
