# Maintain a sorted list of disjoint free intervals; allocate from the leftmost fitting one, erase merges back.
from typing import List, Optional, Any
import bisect


def processMemoryQueries(memory: List[int], queries: List[List[int]]) -> List[int]:
    free: List[List[int]] = []  # [start, end] inclusive, sorted, disjoint, non-adjacent
    n = len(memory)
    i = 0
    while i < n:
        if memory[i] == 0:
            j = i
            while j + 1 < n and memory[j + 1] == 0:
                j += 1
            free.append([i, j])
            i = j + 1
        else:
            i += 1

    starts = [iv[0] for iv in free]
    blocks = {}  # id -> (start, length)
    next_id = 1
    res: List[int] = []

    for q in queries:
        kind, val = q[0], q[1]
        if kind == 0:
            x = val
            found = -1
            for k in range(len(free)):
                s, e = free[k]
                if e - s + 1 >= x:
                    found = k
                    break
            if found < 0:
                res.append(-1)
                continue
            s, e = free[found]
            if s + x > e:
                free.pop(found)
                starts.pop(found)
            else:
                free[found][0] = s + x
                starts[found] = s + x
            blocks[next_id] = (s, x)
            next_id += 1
            res.append(s)
        else:
            bid = val
            if bid not in blocks:
                res.append(-1)
                continue
            s, length = blocks.pop(bid)
            e = s + length - 1
            k = bisect.bisect_left(starts, s)
            # merge with the right neighbour if adjacent
            if k < len(free) and free[k][0] == e + 1:
                e = free[k][1]
                free.pop(k)
                starts.pop(k)
            # merge with the left neighbour if adjacent
            if k - 1 >= 0 and free[k - 1][1] == s - 1:
                free[k - 1][1] = e
            else:
                free.insert(k, [s, e])
                starts.insert(k, s)
            res.append(length)
    return res
