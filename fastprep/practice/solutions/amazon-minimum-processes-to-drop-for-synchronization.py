# For each candidate centre, the processes it does NOT overlap end before its start or start after its end;
# count both with binary search over sorted ends and starts.
from typing import List, Optional, Any
from bisect import bisect_left, bisect_right


def minimumProcessesToDrop(starts: List[int], ends: List[int]) -> int:
    n = len(starts)
    if n == 0:
        return 0
    ss = sorted(starts)
    es = sorted(ends)
    best = n
    for a, b in zip(starts, ends):
        before = bisect_left(es, a)          # ends[j] < a
        after = n - bisect_right(ss, b)      # starts[j] > b
        best = min(best, before + after)
    return best
