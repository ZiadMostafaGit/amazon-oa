# Single-pass event simulation of a shared counter with two independently exiting workers.
from typing import List, Optional, Any


def sumSnapshots(events: List[str]) -> int:
    counter = 0
    threshold_active = True
    timer_active = True
    threshold_snapshot = 0
    timer_snapshot = 0
    for event in events:
        if event == "THRESHOLD":
            if not threshold_active:
                continue
            counter += 1
        elif event == "TIMER":
            if not timer_active:
                continue
            counter += 1
        else:
            if timer_active:
                timer_snapshot = counter
                timer_active = False
            continue
        if threshold_active and counter == 10:
            threshold_snapshot = 10
            threshold_active = False
    return threshold_snapshot + timer_snapshot
