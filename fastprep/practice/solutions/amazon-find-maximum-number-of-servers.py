# Counting + sliding window: a valid cycle covers a contiguous value range whose interior values each appear at least twice.
from typing import List, Optional, Any
from collections import Counter


def getMaxServers(powers: List[int]) -> int:
    counts = Counter(powers)
    values = sorted(counts)
    m = len(values)
    best = 0
    i = 0
    while i < m:
        j = i
        while j + 1 < m and values[j + 1] == values[j] + 1:
            j += 1
        window = 0  # best total for a range ending at the current value
        for k in range(i, j + 1):
            c = counts[values[k]]
            window += c
            if window > best:
                best = window
            if c == 1:
                # this value can only be an endpoint, so later ranges must start here
                window = c
        i = j + 1
    return best
