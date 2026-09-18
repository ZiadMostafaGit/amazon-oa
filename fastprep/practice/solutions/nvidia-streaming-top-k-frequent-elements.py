# Hash-map counter plus a partial selection (heap) per query ordered by (-freq, value).
from typing import List, Optional, Any
import heapq


def streamTopK(operations: List[List[int]]) -> List[List[int]]:
    freq = {}
    out = []
    for op, arg in operations:
        if op == 0:
            freq[arg] = freq.get(arg, 0) + 1
        else:
            top = heapq.nsmallest(arg, freq.items(), key=lambda kv: (-kv[1], kv[0]))
            out.append([v for v, _ in top])
    return out
