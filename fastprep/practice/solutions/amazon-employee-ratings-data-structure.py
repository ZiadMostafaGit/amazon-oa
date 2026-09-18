# Fenwick tree for index<->slot mapping plus a max segment tree for the earliest maximum.
from typing import List, Optional, Any

NEG = float("-inf")


def solve(operations: List[List[int]]) -> List[List[int]]:
    n = len(operations)
    cap = max(n, 1)

    size = 1
    while size < cap:
        size <<= 1
    tree = [NEG] * (2 * size)

    def seg_set(pos: int, val: float) -> None:
        i = pos + size
        tree[i] = val
        i >>= 1
        while i >= 1:
            left = tree[2 * i]
            right = tree[2 * i + 1]
            tree[i] = left if left >= right else right
            i >>= 1

    def seg_leftmost_max() -> int:
        # returns the slot of the leftmost occurrence of the global maximum
        i = 1
        while i < size:
            if tree[2 * i] >= tree[2 * i + 1]:
                i = 2 * i
            else:
                i = 2 * i + 1
        return i - size

    bit = [0] * (cap + 1)

    def bit_add(pos: int, delta: int) -> None:
        i = pos + 1
        while i <= cap:
            bit[i] += delta
            i += i & (-i)

    def bit_prefix(pos: int) -> int:
        # count of active slots in [0, pos]
        i = pos + 1
        total = 0
        while i > 0:
            total += bit[i]
            i -= i & (-i)
        return total

    log = 0
    while (1 << (log + 1)) <= cap:
        log += 1

    def bit_kth(k: int) -> int:
        # slot of the k-th (0-based) active element
        pos = 0
        remaining = k + 1
        for step in range(log, -1, -1):
            nxt = pos + (1 << step)
            if nxt <= cap and bit[nxt] < remaining:
                pos = nxt
                remaining -= bit[nxt]
        return pos

    results: List[List[int]] = []
    next_slot = 0
    active = 0

    for op in operations:
        kind = op[0]
        if kind == 1:
            rating = op[1]
            seg_set(next_slot, rating)
            bit_add(next_slot, 1)
            next_slot += 1
            active += 1
        elif kind == 2:
            index = op[1]
            if 0 <= index < active:
                slot = bit_kth(index)
                seg_set(slot, NEG)
                bit_add(slot, -1)
                active -= 1
        else:
            if active > 0:
                slot = seg_leftmost_max()
                best = tree[1]
                current_index = bit_prefix(slot) - 1
                results.append([int(best), current_index])

    return results
