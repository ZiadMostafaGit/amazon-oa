# Task-scheduler greedy: the most frequent region fixes the skeleton of slots of width minGap+1.
from collections import Counter


def getMinTime2(n: int, requests: str, minGap: int) -> int:
    if not requests:
        return 0
    counts = Counter(requests)
    max_count = max(counts.values())
    num_max = sum(1 for c in counts.values() if c == max_count)
    total = len(requests)
    skeleton = (max_count - 1) * (minGap + 1) + num_max
    return max(total, skeleton)
