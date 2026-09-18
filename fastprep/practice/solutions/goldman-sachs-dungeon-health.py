# Bottom-up DP from the princess cell: need[i][j] = min health required on entering (i, j).
from typing import List, Optional, Any


def calculateMinimumHP(dungeon: List[List[int]]) -> int:
    m = len(dungeon)
    n = len(dungeon[0])
    INF = float('inf')
    # need[j] for the current row; sentinel column at the end
    need = [INF] * (n + 1)
    for i in range(m - 1, -1, -1):
        new = [INF] * (n + 1)
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                nxt = 1
            else:
                nxt = min(new[j + 1], need[j])
            val = nxt - dungeon[i][j]
            new[j] = val if val > 1 else 1
        need = new
    return need[0]
