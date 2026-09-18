# Approach: single pass with a hash set to track seen lines, preserving first-appearance order.
from typing import List, Optional, Any


def getUniqueLines(lines: List[str]) -> List[str]:
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result
