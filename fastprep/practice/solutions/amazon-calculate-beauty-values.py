# Difference array for index multiplicities + sorted prefix sums to count smaller values.
from bisect import bisect_left
from typing import List, Optional, Any


def solve(arr: List[int], pairs: List[List[int]]) -> int:
    n = len(arr)
    if n == 0:
        return 0

    diff = [0] * (n + 1)
    for p in pairs:
        s, e = p[0], p[1]
        if s > e:
            s, e = e, s
        if s < 0:
            s = 0
        if e > n - 1:
            e = n - 1
        if s > n - 1 or e < 0:
            continue
        diff[s] += 1
        diff[e + 1] -= 1

    cnt = [0] * n
    run = 0
    for i in range(n):
        run += diff[i]
        cnt[i] = run

    # multiset of the new array: value arr[i] repeated cnt[i] times
    pairs_vc = sorted((arr[i], cnt[i]) for i in range(n) if cnt[i] > 0)
    vals = [v for v, _ in pairs_vc]
    prefix = [0] * (len(pairs_vc) + 1)
    for j, (_v, c) in enumerate(pairs_vc):
        prefix[j + 1] = prefix[j] + c

    total = 0
    for i in range(n):
        if cnt[i] == 0:
            total += prefix[bisect_left(vals, arr[i])]
    return total
