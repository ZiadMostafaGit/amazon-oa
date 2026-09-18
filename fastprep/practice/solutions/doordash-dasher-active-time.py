# Sweep over events keeping an active-delivery counter; accumulate time while the counter is positive.
from typing import List, Optional, Any


def totalActiveTime(timestamps: List[int], actions: List[str]) -> int:
    total = 0
    active = 0
    start = 0
    for i in range(len(timestamps)):
        t = timestamps[i]
        a = actions[i]
        if a == "PICKUP":
            if active == 0:
                start = t
            active += 1
        else:
            if active > 0:
                active -= 1
                if active == 0:
                    total += t - start
    return total
