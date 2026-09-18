# Group processes by original execution time; each group's remaining value halves (ceiling) per execution.
from typing import List, Optional, Any


def totalExecutionTime(execution: List[int]) -> int:
    current = {}
    total = 0
    for value in execution:
        cur = current.get(value, value)
        total += cur
        current[value] = (cur + 1) // 2 if cur > 0 else cur
    return total
