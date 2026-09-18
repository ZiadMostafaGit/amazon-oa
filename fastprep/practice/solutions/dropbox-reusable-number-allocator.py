# Min-heap of released numbers plus a high-water counter for never-assigned numbers.
from typing import List, Optional, Any
import heapq


def runNumberAllocator(n: int, operations: List[str], values: List[int]) -> List[int]:
    freed = []
    nxt = 0
    out = []
    for op, val in zip(operations, values):
        if op == "assign":
            if freed:
                out.append(heapq.heappop(freed))
            elif nxt < n:
                out.append(nxt)
                nxt += 1
            else:
                out.append(-1)
        else:
            heapq.heappush(freed, val)
    return out
