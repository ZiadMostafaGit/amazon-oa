from typing import List, Optional, Any


def allAboutCave(A: List[str]) -> int:
    n = len(A)
    if n == 0:
        return -1
    m = len(A[0])
    NEG = float("-inf")
    # prev[c] = best count of chambers visited when arriving at (r, c) from above
    prev = [NEG] * m
    if A[0][0] != '.':
        return -1
    prev[0] = 0
    for r in range(n):
        row = A[r]
        # enter at e (value prev[e]), walk monotonically to d: prev[e] + |e-d| + 1
        left = [NEG] * m   # best ending at d, came from e <= d
        best = NEG
        for c in range(m):
            if row[c] != '.':
                best = NEG
                continue
            best = max(best + 1, prev[c] + 1)
            left[c] = best
        right = [NEG] * m
        best = NEG
        for c in range(m - 1, -1, -1):
            if row[c] != '.':
                best = NEG
                continue
            best = max(best + 1, prev[c] + 1)
            right[c] = best
        cur = [max(left[c], right[c]) for c in range(m)]
        if r == n - 1:
            return int(cur[m - 1]) if cur[m - 1] != NEG else -1
        nxt = [NEG] * m
        for c in range(m):
            if cur[c] != NEG and A[r + 1][c] == '.':
                nxt[c] = cur[c]
        prev = nxt
    return -1
