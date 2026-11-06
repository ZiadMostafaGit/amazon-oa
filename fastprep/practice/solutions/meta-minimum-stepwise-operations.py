from typing import List, Optional, Any


def solution(structures: List[int]) -> int:
    n = len(structures)
    if n == 0:
        return 0
    total = sum(structures)
    # ascending: final[i] = b + i, need b >= s[i] - i
    b = max(s - i for i, s in enumerate(structures))
    asc = n * b + n * (n - 1) // 2 - total
    # descending: final[i] = b - i, need b >= s[i] + i
    b = max(s + i for i, s in enumerate(structures))
    desc = n * b - n * (n - 1) // 2 - total
    return min(asc, desc)
