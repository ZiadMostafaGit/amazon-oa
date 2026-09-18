# Sort by start, then sweep merging while the next start touches or overlaps the running end.
from typing import List, Optional, Any


def mergeIntervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    order = sorted(intervals, key=lambda iv: (iv[0], iv[1]))
    out = []
    cur_s, cur_e = order[0][0], order[0][1]
    for s, e in ((iv[0], iv[1]) for iv in order[1:]):
        if s <= cur_e:
            if e > cur_e:
                cur_e = e
        else:
            out.append([cur_s, cur_e])
            cur_s, cur_e = s, e
    out.append([cur_s, cur_e])
    return out
