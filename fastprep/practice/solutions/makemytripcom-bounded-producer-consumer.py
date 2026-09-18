# Deque-based FIFO simulation of a bounded ready queue plus a FIFO queue of blocked producers.
from typing import List, Optional, Any
from collections import deque


def simulateBoundedQueue(capacity: int, events: List[str]) -> List[str]:
    ready = deque()
    waiting = deque()
    out = []
    for ev in events:
        if ev.startswith("PRODUCE"):
            task = ev.split(" ", 1)[1]
            if len(ready) < capacity:
                ready.append(task)
                out.append("ENQUEUED " + task)
            else:
                waiting.append(task)
                out.append("WAIT " + task)
        else:
            if not ready:
                out.append("IDLE")
            else:
                task = ready.popleft()
                line = "CONSUMED " + task
                if waiting:
                    nxt = waiting.popleft()
                    ready.append(nxt)
                    line += " RESUMED " + nxt
                out.append(line)
    return out
