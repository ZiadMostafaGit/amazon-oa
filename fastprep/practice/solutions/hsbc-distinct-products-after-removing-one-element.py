# All values are positive, so the remaining product P/A[i] is distinct exactly when A[i] is: count distinct values.
from typing import List, Optional, Any


def solution(A: List[int]) -> int:
    seen = set()
    for v in A:
        seen.add(v)
    return len(seen)
