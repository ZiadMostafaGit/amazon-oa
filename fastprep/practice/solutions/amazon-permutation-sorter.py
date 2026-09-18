# BFS over the 2n reachable states (rotations of the ascending / descending permutation).
from typing import List, Optional, Any
from collections import deque


def findMinimumOperations(arr: List[int]) -> int:
    n = len(arr)
    if n <= 1:
        return 0

    # Identify the current state.
    # ('A', k): [k+1, k+2, ..., n, 1, ..., k]
    # ('D', m): [m, m-1, ..., 1, n, n-1, ..., m+1]
    def is_asc() -> bool:
        for i in range(n):
            nxt = arr[i] + 1 if arr[i] < n else 1
            if arr[(i + 1) % n] != nxt:
                return False
        return True

    def is_desc() -> bool:
        for i in range(n):
            nxt = arr[i] - 1 if arr[i] > 1 else n
            if arr[(i + 1) % n] != nxt:
                return False
        return True

    if is_asc():
        start = (0, arr[0] - 1)          # type 0 = ascending, offset k
    elif is_desc():
        start = (1, arr[0])              # type 1 = descending, parameter m in 1..n
    else:
        return -1

    goal = (0, 0)
    if start == goal:
        return 0

    def neighbors(state):
        t, v = state
        if t == 0:
            # rotate left: offset k -> k+1
            yield (0, (v + 1) % n)
            # reverse: ascending k -> descending m (m = k, with 0 meaning n)
            yield (1, v if v != 0 else n)
        else:
            # rotate left: m -> m-1, with 1 -> n
            yield (1, v - 1 if v > 1 else n)
            # reverse: descending m -> ascending offset m % n
            yield (0, v % n)

    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        d = dist[cur]
        for nb in neighbors(cur):
            if nb not in dist:
                dist[nb] = d + 1
                if nb == goal:
                    return d + 1
                q.append(nb)
    return -1
