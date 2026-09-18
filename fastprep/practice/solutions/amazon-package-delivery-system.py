# Greedy with a max-heap: assign the heaviest remaining package to the largest current capacity, then halve it.
import heapq
from typing import List, Optional, Any


def canDeliverAllPackages(truckCapacities: List[List[int]], packageWeights: List[List[int]]) -> List[int]:
    results: List[int] = []
    for i in range(len(packageWeights)):
        caps = truckCapacities[i] if i < len(truckCapacities) else []
        weights = sorted(packageWeights[i], reverse=True)
        heap = [-c for c in caps]
        heapq.heapify(heap)
        feasible = 1
        for w in weights:
            if not heap:
                feasible = 0
                break
            best = -heap[0]
            if best < w:
                feasible = 0
                break
            heapq.heapreplace(heap, -(best // 2))
        results.append(feasible)
    return results
