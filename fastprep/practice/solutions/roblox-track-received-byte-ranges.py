# Approach: keep disjoint ranges sorted; for each chunk binary-search the touching window and splice in the merged range.
from typing import List, Optional, Any
import bisect


def trackReceivedByteRanges(chunks: List[List[int]]) -> List[List[str]]:
    starts: List[int] = []
    ends: List[int] = []
    out: List[List[str]] = []
    for c in chunks:
        s, e = c[0], c[1]
        # first range whose end >= s - 1 (touches or overlaps)
        lo = bisect.bisect_left(ends, s - 1)
        # first range whose start > e + 1 (beyond the merge window)
        hi = bisect.bisect_right(starts, e + 1)
        if lo < hi:
            s = min(s, starts[lo])
            e = max(e, ends[hi - 1])
        starts[lo:hi] = [s]
        ends[lo:hi] = [e]
        out.append([str(a) + ":" + str(b) for a, b in zip(starts, ends)])
    return out
