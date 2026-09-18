# Two lazy-deletion heaps (min-heap + max-heap) over a multiset with a live count map.
from typing import List, Optional, Any
import heapq


def maxMin(operations: List[str], x: List[int]) -> List[int]:
    cnt = {}
    lo = []   # min-heap of candidate values
    hi = []   # max-heap (negated) of candidate values
    size = 0
    out = []
    for op, v in zip(operations, x):
        if op == "push":
            cnt[v] = cnt.get(v, 0) + 1
            size += 1
            if cnt[v] == 1:
                heapq.heappush(lo, v)
                heapq.heappush(hi, -v)
            else:
                # value already live; heaps may have dropped it earlier, so re-seed
                heapq.heappush(lo, v)
                heapq.heappush(hi, -v)
        else:
            c = cnt.get(v, 0)
            if c > 0:
                cnt[v] = c - 1
                size -= 1
        if size == 0:
            out.append(0)
            continue
        while lo and cnt.get(lo[0], 0) == 0:
            heapq.heappop(lo)
        while hi and cnt.get(-hi[0], 0) == 0:
            heapq.heappop(hi)
        out.append(lo[0] * (-hi[0]))
    return out
