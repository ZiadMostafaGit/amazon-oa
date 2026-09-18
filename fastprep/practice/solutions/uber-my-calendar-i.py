# Keep accepted intervals in a sorted list; bisect the neighbours to test half-open overlap.
from typing import List, Optional, Any
import bisect


def bookCalendar(starts: List[int], ends: List[int]) -> List[bool]:
    booked_starts: List[int] = []
    booked_ends: List[int] = []
    res: List[bool] = []
    for i in range(len(starts)):
        s = starts[i]
        e = ends[i]
        idx = bisect.bisect_right(booked_starts, s)
        ok = True
        if idx > 0 and booked_ends[idx - 1] > s:
            ok = False
        if ok and idx < len(booked_starts) and booked_starts[idx] < e:
            ok = False
        if ok:
            booked_starts.insert(idx, s)
            booked_ends.insert(idx, e)
        res.append(ok)
    return res
