# Binary-search lower bound insertion into a running sorted list, copying a snapshot after each insert.
from typing import List, Optional, Any
import bisect


def sortedInsertionSnapshots(values: List[int]) -> List[List[int]]:
    cur = []
    out = []
    for v in values:
        pos = bisect.bisect_left(cur, v)
        cur.insert(pos, v)
        out.append(list(cur))
    return out
