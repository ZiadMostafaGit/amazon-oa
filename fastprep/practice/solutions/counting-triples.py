# Multiset counts with incremental recomputation of the 3 affected arithmetic-triple bases per query.
from typing import List, Optional, Any
from collections import defaultdict


def solution(queries: List[str], difference: int) -> List[int]:
    d = difference
    cnt = defaultdict(int)
    total = 0
    out = []

    def term(v: int) -> int:
        a = cnt.get(v, 0)
        if a == 0:
            return 0
        b = cnt.get(v + d, 0)
        if b == 0:
            return 0
        c = cnt.get(v + 2 * d, 0)
        if c == 0:
            return 0
        return a * b * c

    for q in queries:
        q = q.strip()
        sign = q[0]
        x = int(q[1:])
        bases = {x - 2 * d, x - d, x}
        for v in bases:
            total -= term(v)
        if sign == '+':
            cnt[x] += 1
        else:
            cnt[x] = 0
        for v in bases:
            total += term(v)
        out.append(total)
    return out
