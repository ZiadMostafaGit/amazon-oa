# Prefix sums of read times: the earliest start is max(0, max_i(ready_i - 40*i)).
from typing import List, Optional, Any


def scheduleVideoFrames(readDurations: List[int]) -> List[int]:
    start = 0
    ready = 0
    for i, d in enumerate(readDurations):
        ready += d
        need = ready - 40 * i
        if need > start:
            start = need
    return [start + 40 * i for i in range(len(readDurations))]
