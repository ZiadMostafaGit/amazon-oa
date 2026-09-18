# Backtracking over segment lengths 1..3 with feasibility pruning, emitting results in lexicographic order.
from typing import List, Optional, Any


def restoreAddresses(digits: str, segmentCount: int) -> List[str]:
    n = len(digits)
    if segmentCount < 1 or n < segmentCount or n > 3 * segmentCount:
        return []
    out = []
    parts = []

    def dfs(i: int, left: int) -> None:
        rem = n - i
        if left == 0:
            if rem == 0:
                out.append(".".join(parts))
            return
        if rem < left or rem > 3 * left:
            return
        for size in (1, 2, 3):
            if i + size > n:
                break
            piece = digits[i:i + size]
            if size > 1 and piece[0] == "0":
                break
            if int(piece) > 255:
                break
            parts.append(piece)
            dfs(i + size, left - 1)
            parts.pop()

    dfs(0, segmentCount)
    out.sort()
    return out
