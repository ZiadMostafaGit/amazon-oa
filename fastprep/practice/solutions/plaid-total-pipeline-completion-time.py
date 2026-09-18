# Sum of taskTime * taskCount over every row (single sequential worker).
from typing import List, Optional, Any


def totalPipelineTime(tasks: List[List[int]]) -> int:
    total = 0
    for row in tasks:
        total += row[0] * row[1]
    return total
