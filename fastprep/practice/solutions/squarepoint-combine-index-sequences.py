# Direct concatenation preserving order.
from typing import List, Optional, Any


def combineIndexSequences(first: List[int], second: List[int]) -> List[int]:
    return list(first) + list(second)
