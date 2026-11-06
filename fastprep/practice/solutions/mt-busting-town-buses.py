from typing import List, Optional, Any


def bustlingTownBuses(timeTable: List[str], moment: str) -> int:
    def mins(t: str) -> int:
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    now = mins(moment)
    last = -1
    for t in timeTable:
        x = mins(t)
        if x < now and x > last:
            last = x
    return -1 if last < 0 else now - last
