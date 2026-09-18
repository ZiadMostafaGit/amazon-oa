# Single-server queue simulation with a monotonic pointer over increasing finish times.
from typing import List, Optional, Any


def solveOneQueueCheckInSimulation(input: str) -> List[str]:
    toks = input.split()
    if not toks:
        return []
    n = int(toks[0])
    arrivals = [int(x) for x in toks[1:1 + n]]

    SERVICE = 30
    CAP = 10

    ends: List[int] = []   # finish times of accepted people, increasing
    head = 0               # first index in ends that may still be in the system
    free_at = 0            # time the server becomes free
    result: List[str] = []

    for t in arrivals:
        while head < len(ends) and ends[head] <= t:
            head += 1
        in_system = len(ends) - head
        if in_system > CAP:
            result.append("null")
            continue
        start = free_at if free_at > t else t
        result.append(str(start))
        free_at = start + SERVICE
        ends.append(free_at)
    return result
