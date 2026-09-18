# Hash-map counter over b; each count query sums cnt[x - ai] over a.
from typing import List, Optional, Any
from collections import Counter


def findSumPairs(a: List[int], b: List[int], queries: List[List[int]]) -> List[int]:
    cnt = Counter(b)
    out = []
    for q in queries:
        if q[0] == 0:
            _, i, x = q
            a[i] = x
        else:
            x = q[1]
            total = 0
            for v in a:
                total += cnt.get(x - v, 0)
            out.append(total)
    return out
