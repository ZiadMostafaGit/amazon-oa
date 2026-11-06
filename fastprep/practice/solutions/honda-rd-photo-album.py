# Offline in reverse: the last photo's index is final. Going backwards, photo i takes the (index[i]+1)-th
# still-free slot; a Fenwick tree of free slots finds it by binary descent.
from typing import List


def photoAlbum(index: List[int], identity: List[int]) -> List[int]:
    n = len(index)
    tree = [0] * (n + 1)
    for i in range(1, n + 1):            # all slots free: O(n) build of an all-ones Fenwick tree
        tree[i] += 1
        j = i + (i & -i)
        if j <= n:
            tree[j] += tree[i]
    LOG = n.bit_length()
    out = [0] * n
    for i in range(n - 1, -1, -1):
        k = index[i] + 1
        pos = 0
        for b in range(LOG, -1, -1):
            nxt = pos + (1 << b)
            if nxt <= n and tree[nxt] < k:
                pos = nxt
                k -= tree[nxt]
        slot = pos + 1
        out[slot - 1] = identity[i]
        j = slot
        while j <= n:
            tree[j] -= 1
            j += j & -j
    return out
