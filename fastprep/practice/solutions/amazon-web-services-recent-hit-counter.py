# Sliding-window deque over the nondecreasing timestamps, evicting hits outside (t-300, t].
from typing import List, Optional, Any
from collections import deque


def countRecentHits(operationTypes: List[int], timestamps: List[int]) -> List[int]:
    window = deque()
    out = []
    for op, t in zip(operationTypes, timestamps):
        if op == 0:
            window.append(t)
        else:
            while window and window[0] <= t - 300:
                window.popleft()
            out.append(len(window))
    return out
