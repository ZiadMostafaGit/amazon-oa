# Two Fenwick trees over compressed values give, for each prefix, the count and sum of smaller/larger elements in O(n log n).
from typing import List
from bisect import bisect_left


def arrayChallenge(arr: List[int]) -> List[int]:
    n = len(arr)
    order = sorted(set(arr))
    m = len(order)
    cnt_tree = [0] * (m + 1)
    sum_tree = [0] * (m + 1)

    def update(i, val):
        while i <= m:
            cnt_tree[i] += 1
            sum_tree[i] += val
            i += i & (-i)

    def query(i):
        c = 0
        s = 0
        while i > 0:
            c += cnt_tree[i]
            s += sum_tree[i]
            i -= i & (-i)
        return c, s

    res = [0] * n
    total = 0
    for i, x in enumerate(arr):
        pos = bisect_left(order, x) + 1  # 1-based rank
        c_le, s_le = query(pos)
        c_lt, s_lt = query(pos - 1)
        c_gt = i - c_le
        s_gt = total - s_le
        res[i] = (c_lt * x - s_lt) - (s_gt - c_gt * x)
        update(pos, x)
        total += x
    return res
