# Levenshtein edit distance via rolling DP, picking min distance then lexicographically smallest.
from typing import List, Optional, Any


def _edit_distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    cur = [0] * (m + 1)
    for i in range(1, n + 1):
        cur[0] = i
        ai = a[i - 1]
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev, cur = cur, prev
    return prev[m]


def findClosestStrings(strings: List[str], queries: List[str]) -> List[str]:
    result = []
    for q in queries:
        best = None
        best_d = None
        for s in strings:
            d = _edit_distance(s, q)
            if best_d is None or d < best_d or (d == best_d and s < best):
                best_d = d
                best = s
        result.append(best)
    return result
