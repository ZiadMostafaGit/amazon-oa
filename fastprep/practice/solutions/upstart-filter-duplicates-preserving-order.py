# Single pass with a seen-set, keeping the first occurrence of each value.
from typing import List


def filterDuplicates(data: List[int]) -> List[int]:
    seen = set()
    out = []
    for v in data:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out
