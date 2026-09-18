# Prefix non-increasing run lengths and suffix non-decreasing run lengths, one pass each.
from typing import List, Optional, Any


def findIdealDays(forecast: List[int], window: int) -> List[int]:
    n = len(forecast)
    down = [0] * n
    for i in range(1, n):
        down[i] = down[i - 1] + 1 if forecast[i - 1] >= forecast[i] else 0
    up = [0] * n
    for i in range(n - 2, -1, -1):
        up[i] = up[i + 1] + 1 if forecast[i] <= forecast[i + 1] else 0
    return [i + 1 for i in range(n) if down[i] >= window and up[i] >= window]
