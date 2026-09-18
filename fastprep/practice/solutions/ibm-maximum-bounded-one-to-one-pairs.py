# Greedy sweep over sorted arr2 with a min-heap of candidate arr1 values.
import heapq
from typing import List


def maxValidPairs(arr1: List[int], arr2: List[int], d: int) -> int:
    a = sorted(arr1)
    b = sorted(arr2)
    heap: List[int] = []
    i = 0
    n = len(a)
    count = 0
    for val in b:
        while i < n and a[i] <= val:
            heapq.heappush(heap, a[i])
            i += 1
        while heap and heap[0] < val - d:
            heapq.heappop(heap)
        if heap:
            heapq.heappop(heap)
            count += 1
    return count
