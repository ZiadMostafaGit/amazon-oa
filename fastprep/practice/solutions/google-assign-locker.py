# Min-heap of released locker numbers plus a rising counter for never-used lockers.
import heapq
from typing import List, Optional, Any


def assignLocker(clients: List[str]) -> int:
    free: List[int] = []
    next_locker = 1
    held = {}
    last = 0
    for name in clients:
        if name in held:
            heapq.heappush(free, held.pop(name))
        else:
            if free:
                locker = heapq.heappop(free)
            else:
                locker = next_locker
                next_locker += 1
            held[name] = locker
            last = locker
    return last
