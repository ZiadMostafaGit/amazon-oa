# Greedy task-scheduler formula: (maxFreq-1)*(minGap+1) + #(regions with maxFreq), floored at n.
from collections import Counter


def findMinimumTimeRequired(requests: str, minGap: int) -> int:
    n = len(requests)
    if n == 0:
        return 0
    counts = Counter(requests)
    max_freq = max(counts.values())
    num_max = sum(1 for v in counts.values() if v == max_freq)
    slots = (max_freq - 1) * (minGap + 1) + num_max
    return max(n, slots)
