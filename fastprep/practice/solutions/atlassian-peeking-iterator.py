# Simulate the iterator with a cursor: peek reads at the cursor, next reads and advances.
from typing import List, Optional, Any


def runPeekingIterator(nums: List[int], operations: List[str]) -> List[str]:
    pos = 0
    out: List[str] = []
    for op in operations:
        if op == "peek":
            out.append(str(nums[pos]))
        elif op == "next":
            out.append(str(nums[pos]))
            pos += 1
        elif op == "hasNext":
            out.append("true" if pos < len(nums) else "false")
    return out
