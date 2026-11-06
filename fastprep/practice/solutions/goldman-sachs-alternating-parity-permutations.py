from typing import List, Optional, Any


def alternatingParityPermutations(n: int) -> List[List[int]]:
    res = []
    used = [False] * (n + 1)
    cur = []

    def bt():
        if len(cur) == n:
            res.append(cur[:])
            return
        for v in range(1, n + 1):
            if not used[v] and (not cur or (cur[-1] - v) % 2 == 1):
                used[v] = True
                cur.append(v)
                bt()
                cur.pop()
                used[v] = False

    bt()
    return res
