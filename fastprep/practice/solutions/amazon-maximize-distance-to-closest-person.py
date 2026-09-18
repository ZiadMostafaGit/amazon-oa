# Approach: two linear sweeps for nearest occupied seat distance, then take the best empty index.
from typing import List, Optional, Any


def solve(seats: List[int]) -> int:
    n = len(seats)
    INF = float('inf')
    dist = [INF] * n
    last = -1
    for i in range(n):
        if seats[i] == 1:
            last = i
            dist[i] = 0
        elif last >= 0:
            dist[i] = i - last
    last = -1
    for i in range(n - 1, -1, -1):
        if seats[i] == 1:
            last = i
        elif last >= 0:
            dist[i] = min(dist[i], last - i)
    best_i = -1
    best_d = -1
    for i in range(n):
        if seats[i] == 0 and dist[i] > best_d:
            best_d = dist[i]
            best_i = i
    return best_i
