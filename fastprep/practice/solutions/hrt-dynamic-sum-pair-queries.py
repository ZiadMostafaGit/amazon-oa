# Hash-map frequency counts of both arrays; each sum query scans the smaller distinct-value set.
from typing import List, Optional, Any
from collections import Counter


def solution(a: List[int], b: List[int], queries: List[List[int]]) -> List[int]:
    cnt_a = Counter(a)
    cnt_b = Counter(b)
    arr = list(a)
    res = []
    for q in queries:
        if q[0] == 0:
            i, x = q[1], q[2]
            old = arr[i]
            if old != x:
                cnt_a[old] -= 1
                if cnt_a[old] == 0:
                    del cnt_a[old]
                cnt_a[x] += 1
                arr[i] = x
        else:
            x = q[1]
            total = 0
            if len(cnt_a) <= len(cnt_b):
                for v, c in cnt_a.items():
                    d = cnt_b.get(x - v)
                    if d:
                        total += c * d
            else:
                for v, c in cnt_b.items():
                    d = cnt_a.get(x - v)
                    if d:
                        total += c * d
            res.append(total)
    return res
