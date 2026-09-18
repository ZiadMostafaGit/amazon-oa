# Sliding window over a deque of timestamps, evicting anything older than 300 seconds.
from collections import deque
from typing import List, Optional, Any


def runHitCounter(operations: List[str], timestamps: List[int]) -> List[str]:
    window = deque()
    output: List[str] = []
    for op, ts in zip(operations, timestamps):
        if op == "hit":
            window.append(ts)
            output.append("null")
        elif op == "getHits":
            while window and window[0] <= ts - 300:
                window.popleft()
            output.append(str(len(window)))
        else:
            output.append("null")
    return output
