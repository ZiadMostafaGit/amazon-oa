# Monotonic decreasing stack of indices, resolved right-to-left as warmer days appear.
from typing import List, Optional, Any


def dailyTemperatures(temps: List[int]) -> List[int]:
    n = len(temps)
    answer = [0] * n
    stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
