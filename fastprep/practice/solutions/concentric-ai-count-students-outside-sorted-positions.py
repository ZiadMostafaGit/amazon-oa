# Sort a copy and count positions whose value differs from the original.
from typing import List, Optional, Any


def countStudentsOutOfPosition(heights: List[int]) -> int:
    target = sorted(heights)
    return sum(1 for a, b in zip(heights, target) if a != b)
