# Greedy list-scheduling per phase with a min-heap of worker availabilities; phase makespans accumulate at each barrier.
from typing import List, Optional, Any
import heapq


def phaseBarrierCompletionTimes(workers: int, phaseDurations: List[List[int]]) -> List[int]:
    numTasks = len(phaseDurations)
    if numTasks == 0:
        return []
    numPhases = len(phaseDurations[0])
    m = min(workers, numTasks)

    result = []
    cumulative = 0
    for p in range(numPhases):
        heap = [0] * m
        makespan = 0
        for t in range(numTasks):
            d = phaseDurations[t][p]
            free = heapq.heappop(heap)
            finish = free + d
            if finish > makespan:
                makespan = finish
            heapq.heappush(heap, finish)
        cumulative += makespan
        result.append(cumulative)
    return result
