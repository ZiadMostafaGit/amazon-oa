from typing import List, Optional, Any


def minimumSwapsAfterUpdates(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)
    arr = list(nums)
    tree = [[0] * (n + 1) for _ in range(4)]  # one Fenwick tree per value 1..3

    def add(t, i, d):
        i += 1
        while i <= n:
            t[i] += d
            i += i & -i

    def pref(t, i):  # count in arr[0:i]
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    cnt = [0, 0, 0, 0]
    for i, v in enumerate(arr):
        add(tree[v], i, 1)
        cnt[v] += 1

    out = []
    for pos, val in queries:
        i = pos - 1
        old = arr[i]
        if old != val:
            add(tree[old], i, -1)
            add(tree[val], i, 1)
            cnt[old] -= 1
            cnt[val] += 1
            arr[i] = val
        b1, b2 = cnt[1], cnt[1] + cnt[2]
        bounds = [(0, b1), (b1, b2), (b2, n)]
        # m[a][b] = number of value b sitting in the region that value a should occupy
        m = [[0] * 4 for _ in range(4)]
        for a in (1, 2, 3):
            lo, hi = bounds[a - 1]
            for b in (1, 2, 3):
                if a != b:
                    m[a][b] = pref(tree[b], hi) - pref(tree[b], lo)
        two = 0
        misplaced = 0
        for a, b in ((1, 2), (1, 3), (2, 3)):
            two += min(m[a][b], m[b][a])
            misplaced += m[a][b] + m[b][a]
        rest = misplaced - 2 * two  # left in 3-cycles, each costs 2 swaps
        out.append(two + 2 * (rest // 3))
    return out
