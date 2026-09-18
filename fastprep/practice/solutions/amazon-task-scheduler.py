# Greedy counting formula: fill slots around the most frequent task, answer = max(len(tasks), (maxCount-1)*(n+1) + numberOfTasksWithMaxCount).
from typing import List
from collections import Counter


def solve(tasks: List[str], n: int) -> int:
    if not tasks:
        return 0
    counts = Counter(tasks)
    max_count = max(counts.values())
    num_max = sum(1 for c in counts.values() if c == max_count)
    return max(len(tasks), (max_count - 1) * (n + 1) + num_max)
