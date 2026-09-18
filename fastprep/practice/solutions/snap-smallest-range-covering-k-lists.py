# Min-heap over one pointer per list, tracking the current maximum to shrink the covering window.
import heapq
from typing import List, Optional, Any


def smallestRange(nums: List[List[int]]) -> List[int]:
    heap = []
    cur_max = None
    for i, lst in enumerate(nums):
        heap.append((lst[0], i, 0))
        if cur_max is None or lst[0] > cur_max:
            cur_max = lst[0]
    heapq.heapify(heap)

    best_left, best_right = heap[0][0], cur_max
    while True:
        val, i, j = heapq.heappop(heap)
        if cur_max - val < best_right - best_left or (
            cur_max - val == best_right - best_left and val < best_left
        ):
            best_left, best_right = val, cur_max
        if j + 1 == len(nums[i]):
            break
        nxt = nums[i][j + 1]
        if nxt > cur_max:
            cur_max = nxt
        heapq.heappush(heap, (nxt, i, j + 1))
    return [best_left, best_right]
