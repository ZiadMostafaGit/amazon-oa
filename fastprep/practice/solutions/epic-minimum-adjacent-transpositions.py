# Greedy char-to-position matching (earliest unused occurrence) + BIT inversion count.
from collections import defaultdict, deque


def minimumAdjacentSwaps(source: str, target: str) -> int:
    n = len(source)
    slots = defaultdict(deque)
    for i, ch in enumerate(target):
        slots[ch].append(i)

    perm = [0] * n
    for i, ch in enumerate(source):
        perm[i] = slots[ch].popleft()

    # count inversions in perm with a Fenwick tree
    tree = [0] * (n + 1)
    inv = 0
    for i in range(n - 1, -1, -1):
        # number of already-seen (to the right) values strictly smaller than perm[i]
        j = perm[i]  # query prefix [0, perm[i]-1] -> index perm[i]
        while j > 0:
            inv += tree[j]
            j -= j & -j
        j = perm[i] + 1
        while j <= n:
            tree[j] += 1
            j += j & -j
    return inv
