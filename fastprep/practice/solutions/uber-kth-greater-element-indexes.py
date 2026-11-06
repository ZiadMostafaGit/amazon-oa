from typing import List, Optional, Any


def kthGreaterElementIndexes(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    tree = [0] * (n + 1)  # Fenwick tree over positions 1..n

    def add(i):
        while i <= n:
            tree[i] += 1
            i += i & -i

    def prefix(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    LOG = n.bit_length()

    def kth(target):  # smallest position p with prefix(p) >= target
        p = 0
        for b in range(LOG, -1, -1):
            q = p + (1 << b)
            if q <= n and tree[q] < target:
                p = q
                target -= tree[q]
        return p + 1

    ans = [-1] * n
    order = sorted(range(n), key=lambda i: -nums[i])
    total = 0
    g = 0
    while g < n:
        h = g
        while h < n and nums[order[h]] == nums[order[g]]:
            h += 1
        # tree holds exactly the strictly greater values
        for idx in order[g:h]:
            before = prefix(idx + 1)
            if total - before >= k:
                ans[idx] = kth(before + k)
        for idx in order[g:h]:
            add(idx + 1)
            total += 1
        g = h
    return ans
