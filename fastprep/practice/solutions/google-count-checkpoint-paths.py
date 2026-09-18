# Column-by-column DP over row counts; at a checkpoint column every row but the checkpoint's is zeroed.
from typing import List


def solve(rows: int, columns: int, checkpoints: List[List[int]]) -> int:
    if rows <= 0 or columns <= 0:
        return 0

    need = {}
    prev_col = -1
    for cp in checkpoints:
        r, c = cp[0], cp[1]
        if c < prev_col:
            return 0  # cannot be visited in the given order
        if c in need and need[c] != r:
            return 0
        if not (0 <= r < rows) or not (0 <= c < columns):
            return 0
        need[c] = r
        prev_col = c

    dp = [0] * rows
    dp[rows - 1] = 1
    if 0 in need and need[0] != rows - 1:
        return 0

    for c in range(1, columns):
        ndp = [0] * rows
        for r in range(rows):
            v = dp[r]
            if v:
                if r > 0:
                    ndp[r - 1] += v
                ndp[r] += v
                if r + 1 < rows:
                    ndp[r + 1] += v
        if c in need:
            keep = need[c]
            val = ndp[keep]
            ndp = [0] * rows
            ndp[keep] = val
        dp = ndp

    return dp[rows - 1]
