# Read-optimized index: lazily rebuild prev-occurrence array + sliding-window max so queries are O(1).
from typing import List, Optional, Any
from collections import deque


def solve(nums: List[int], k: int, operations: List[List[int]]) -> List[int]:
    a = list(nums)
    n = len(a)
    dup = []
    dirty = True

    def rebuild():
        prev = [-1] * n
        last = {}
        for i in range(n):
            v = a[i]
            if v in last:
                prev[i] = last[v]
            last[v] = i
        flags = []
        if k <= n:
            dq = deque()  # indices, prev values decreasing
            for i in range(n):
                while dq and prev[dq[-1]] <= prev[i]:
                    dq.pop()
                dq.append(i)
                s = i - k + 1
                if s >= 0:
                    while dq[0] < s:
                        dq.popleft()
                    flags.append(1 if prev[dq[0]] >= s else 0)
        return flags

    out = []
    for op in operations:
        kind, x, _y = op[0], op[1], op[2]
        if kind == 0:
            if a[x] != _y:
                a[x] = _y
                dirty = True
            continue
        if dirty:
            dup = rebuild()
            dirty = False
        out.append(dup[x] if 0 <= x < len(dup) else 0)
    return out
