# Track the furthest last occurrence of any letter seen in the current part; cut when i reaches it.
from typing import List, Optional, Any


def partitionLabels(text: str) -> List[int]:
    last = {c: i for i, c in enumerate(text)}
    res = []
    start = end = 0
    for i, c in enumerate(text):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res
