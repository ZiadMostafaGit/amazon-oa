# Convert to minutes, bisect_left for the first departure >= now.
from bisect import bisect_left
from typing import List, Optional, Any


def _minutes(t: str) -> int:
    return int(t[:2]) * 60 + int(t[3:])


def nextShuttleWait(shuttle_times: List[str], current_time: str) -> str:
    times = [_minutes(t) for t in shuttle_times]
    now = _minutes(current_time)
    i = bisect_left(times, now)
    if i == len(times):
        return "-1"
    wait = times[i] - now
    return "%02d:%02d" % (wait // 60, wait % 60)
