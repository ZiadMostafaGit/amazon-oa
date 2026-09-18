# Sliding window: rolling sum for the average (reduced with gcd) and a monotonic deque for the max.
from collections import deque
from math import gcd
from typing import List, Optional, Any


def temperatureWindowStatistics(operations: List[str], windowSize: int) -> List[str]:
    window = deque()          # values currently in the window
    maxdq = deque()           # indices into the stream, decreasing values
    total = 0
    start = 0                 # index of the oldest value in the window
    idx = 0                   # index of the next reading
    out = []
    for op in operations:
        if op[0] == 'A' and op[1] == 'D':      # "ADD <temperature>"
            v = int(op[4:])
            window.append(v)
            total += v
            while maxdq and maxdq[-1][1] <= v:
                maxdq.pop()
            maxdq.append((idx, v))
            idx += 1
            if len(window) > windowSize:
                total -= window.popleft()
                start += 1
                if maxdq[0][0] < start:
                    maxdq.popleft()
        elif op[0] == 'A':                      # "AVERAGE"
            if not window:
                out.append("null")
            else:
                den = len(window)
                num = total
                g = gcd(abs(num), den)
                if g == 0:
                    out.append("0/1")
                else:
                    out.append("%d/%d" % (num // g, den // g))
        else:                                   # "MAX"
            if not window:
                out.append("null")
            else:
                out.append(str(maxdq[0][1]))
    return out
