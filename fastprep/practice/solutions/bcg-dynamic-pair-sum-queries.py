# Keep value-frequency counters for a and b; answer each sum query by scanning the smaller counter.
from typing import List, Optional, Any
from collections import Counter


def solution(a: List[int], b: List[int], queries: List[List[int]]) -> List[int]:
    cnt_a = Counter(a)
    cnt_b = Counter(b)
    cur_a = list(a)
    out = []
    for q in queries:
        if q[0] == 0:
            i, x = q[1], q[2]
            old = cur_a[i]
            if old != x:
                cnt_a[old] -= 1
                if cnt_a[old] == 0:
                    del cnt_a[old]
                cnt_a[x] += 1
                cur_a[i] = x
        else:
            x = q[1]
            total = 0
            if len(cnt_a) <= len(cnt_b):
                for v, c in cnt_a.items():
                    other = cnt_b.get(x - v)
                    if other:
                        total += c * other
            else:
                for v, c in cnt_b.items():
                    other = cnt_a.get(x - v)
                    if other:
                        total += c * other
            out.append(total)
    return out
