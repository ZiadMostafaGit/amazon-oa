# Per-camera maximal qualifying runs, then two-pointer intersection across cameras.
from typing import List, Optional, Any


def _runs(ts: List[int], inten: List[float], threshold: float) -> List[List[int]]:
    out = []
    i = 0
    n = len(ts)
    while i < n:
        if inten[i] >= threshold:
            j = i
            while j + 1 < n and inten[j + 1] >= threshold:
                j += 1
            out.append([ts[i], ts[j]])
            i = j + 1
        else:
            i += 1
    return out


def _intersect(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    res = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            res.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return res


def commonMotionIntervals(timestamps: List[List[int]], intensities: List[List[float]], threshold: float) -> List[List[int]]:
    if not timestamps:
        return []
    cur = _runs(timestamps[0], intensities[0], threshold)
    for c in range(1, len(timestamps)):
        if not cur:
            return []
        cur = _intersect(cur, _runs(timestamps[c], intensities[c], threshold))
    return cur
