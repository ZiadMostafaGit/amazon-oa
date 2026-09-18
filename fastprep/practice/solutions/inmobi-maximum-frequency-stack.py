# Freq-stack: counter of frequencies plus a stack-of-stacks keyed by frequency level.
from typing import List, Optional, Any
from collections import defaultdict


def processFrequencyStack(operations: List[str], values: List[int]) -> List[int]:
    freq = defaultdict(int)
    group = defaultdict(list)
    max_freq = 0
    result = []

    for op, val in zip(operations, values):
        if op == "push":
            freq[val] += 1
            f = freq[val]
            if f > max_freq:
                max_freq = f
            group[f].append(val)
        else:
            if max_freq == 0:
                continue
            val = group[max_freq].pop()
            freq[val] -= 1
            if not group[max_freq]:
                max_freq -= 1
            result.append(val)
    return result
