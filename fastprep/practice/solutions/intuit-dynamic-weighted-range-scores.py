# sum_{p=l..r} (p-l+1)*a[p] = sum p*a[p] - (l-1)*sum a[p]: two Fenwick trees (a[p] and p*a[p]) with point updates.
from typing import List


def weightedScores(nums: List[int], operations: List[List[int]]) -> List[int]:
    n = len(nums)
    t1 = [0] * (n + 1)
    t2 = [0] * (n + 1)
    a = [0] + list(nums)

    def add(p, d):
        dp = d * p
        i = p
        while i <= n:
            t1[i] += d
            t2[i] += dp
            i += i & -i

    def pre(p):
        s1 = s2 = 0
        while p > 0:
            s1 += t1[p]
            s2 += t2[p]
            p -= p & -p
        return s1, s2

    # O(n) build
    for p in range(1, n + 1):
        t1[p] += a[p]
        t2[p] += a[p] * p
        q = p + (p & -p)
        if q <= n:
            t1[q] += t1[p]
            t2[q] += t2[p]
    out = []
    for op in operations:
        if op[0] == 0:
            p, v = op[1], op[2]
            add(p, v - a[p])
            a[p] = v
        else:
            l, r = op[1], op[2]
            r1, r2 = pre(r)
            l1, l2 = pre(l - 1)
            out.append((r2 - l2) - (l - 1) * (r1 - l1))
    return out
