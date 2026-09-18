# Frequency-indexed stacks: keep one stack per frequency level and pop from the highest.
from typing import List, Optional, Any
from collections import defaultdict


def processFrequencyStack(operations: List[str], values: List[int]) -> List[int]:
    freq = defaultdict(int)
    groups = defaultdict(list)
    maxfreq = 0
    out = []
    for op, val in zip(operations, values):
        if op == "push":
            freq[val] += 1
            f = freq[val]
            if f > maxfreq:
                maxfreq = f
            groups[f].append(val)
        else:
            v = groups[maxfreq].pop()
            freq[v] -= 1
            if not groups[maxfreq]:
                del groups[maxfreq]
                maxfreq -= 1
            out.append(v)
    return out
