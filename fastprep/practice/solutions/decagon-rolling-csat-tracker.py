# Sliding time-window with a monotone deque, exact rational average via gcd reduction.
from typing import List, Optional, Any
from collections import deque
from math import gcd


def rollingCsat(operations: List[str], windowSize: int) -> List[str]:
    window = deque()  # (timestamp, score) in nondecreasing timestamp order
    total = 0
    out = []
    for op in operations:
        parts = op.split()
        kind = parts[0].upper()
        if kind == "ADD":
            t = int(parts[1])
            score = int(parts[2])
            window.append((t, score))
            total += score
        else:
            t = int(parts[1])
            low = t - windowSize + 1
            while window and window[0][0] < low:
                total -= window.popleft()[1]
            # timestamps are nondecreasing, so nothing in the deque exceeds t
            while window and window[-1][0] > t:
                total -= window.pop()[1]
            count = len(window)
            if count == 0:
                out.append("EMPTY")
            else:
                g = gcd(total, count)
                out.append(str(total // g) + "/" + str(count // g))
    return out
