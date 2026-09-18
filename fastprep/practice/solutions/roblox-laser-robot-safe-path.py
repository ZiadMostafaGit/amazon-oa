# Binary search over sorted blocked row/column indices to find the nearest obstacle in each direction.
from typing import List, Optional, Any
import bisect


def maxSafeSteps(numRows: int, numCols: int, curRow: int, curCol: int, laserCoordinates: List[List[int]]) -> int:
    bad_rows = sorted({c[0] for c in laserCoordinates})
    bad_cols = sorted({c[1] for c in laserCoordinates})

    def reach(arr, cur, lo, hi):
        # steps upward (toward lo) and downward (toward hi)
        i = bisect.bisect_left(arr, cur)
        # nearest blocked strictly below cur
        if i > 0:
            up = cur - arr[i - 1] - 1
        else:
            up = cur - lo
        j = bisect.bisect_right(arr, cur)
        if j < len(arr):
            down = arr[j] - cur - 1
        else:
            down = hi - cur
        return up, down

    a, b = reach(bad_rows, curRow, 1, numRows)
    c, d = reach(bad_cols, curCol, 1, numCols)
    return max(a, b, c, d)
