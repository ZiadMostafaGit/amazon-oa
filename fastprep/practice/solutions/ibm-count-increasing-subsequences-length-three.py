from typing import List, Optional, Any


def countIncreasingSubsequences(n: int, arr: List[int]) -> int:
    MOD = 10**9 + 7
    n = len(arr)
    vals = sorted(set(arr))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)

    def add(t, i):
        while i <= m:
            t[i] += 1
            i += i & -i

    def query(t, i):
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    left = [0] * n
    t = [0] * (m + 1)
    for j in range(n):
        r = rank[arr[j]]
        left[j] = query(t, r - 1)
        add(t, r)
    t = [0] * (m + 1)
    total = 0
    seen = 0
    for j in range(n - 1, -1, -1):
        r = rank[arr[j]]
        right = seen - query(t, r)
        total += left[j] * right
        add(t, r)
        seen += 1
    return total % MOD
