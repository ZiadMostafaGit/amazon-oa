# Linear scan: convert HH:MM to minutes and take the latest departure strictly before the current time.
from typing import List, Optional, Any


def _to_minutes(value: str) -> int:
    hour, minute = value.strip().split(":")
    return int(hour) * 60 + int(minute)


def busTime(plan: List[str], slot: str) -> int:
    now = _to_minutes(slot)
    best = -1
    for entry in plan:
        t = _to_minutes(entry)
        if t < now and t > best:
            best = t
    if best < 0:
        return -1
    return now - best
