from typing import List, Optional, Any
from collections import deque


def isMaxHeap(values: List[int], leftChild: List[int], rightChild: List[int]) -> bool:
    n = len(values)
    if n == 0:
        return True
    q = deque([0])
    seen_gap = False
    while q:
        u = q.popleft()
        for c in (leftChild[u], rightChild[u]):
            if c == -1:
                seen_gap = True
            else:
                if seen_gap:
                    return False
                if values[c] > values[u]:
                    return False
                q.append(c)
    return True
