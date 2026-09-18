# Convert each endpoint to minutes from Monday 00:00, sort, then sweep merging closed intervals that touch.
from typing import List, Optional, Any

_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_IDX = {d: i for i, d in enumerate(_DAYS)}


def _to_min(day: str, hhmm: str) -> int:
    h, m = hhmm.split(":")
    return _IDX[day] * 1440 + int(h) * 60 + int(m)


def _to_str(total: int) -> str:
    day, rest = divmod(total, 1440)
    h, m = divmod(rest, 60)
    return "%s %02d:%02d" % (_DAYS[day], h, m)


def mergeWeeklyIntervals(intervals: List[str]) -> List[str]:
    parsed = []
    for s in intervals:
        left, right = s.split("->")
        d1, t1 = left.strip().split()
        d2, t2 = right.strip().split()
        parsed.append((_to_min(d1, t1), _to_min(d2, t2)))
    parsed.sort()
    out = []
    for start, end in parsed:
        if out and start <= out[-1][1]:
            if end > out[-1][1]:
                out[-1][1] = end
        else:
            out.append([start, end])
    return [_to_str(a) + " -> " + _to_str(b) for a, b in out]
