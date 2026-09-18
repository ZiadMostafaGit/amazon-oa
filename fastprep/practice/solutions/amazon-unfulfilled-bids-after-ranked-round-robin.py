# Group bids by descending amount and simulate one-unit-per-bid round-robin with a deque.
from collections import deque
from typing import List


def findUnfulfilledBids(bids: List[List[int]], totalInventory: int) -> List[int]:
    groups = {}
    for cid, amount, qty, placed in bids:
        groups.setdefault(amount, []).append((placed, cid, qty))

    remaining = totalInventory
    unfulfilled = []
    for amount in sorted(groups, reverse=True):
        group = sorted(groups[amount])
        if remaining <= 0:
            for _, cid, qty in group:
                if qty > 0:
                    unfulfilled.append(cid)
            continue
        q = deque((cid, qty) for _, cid, qty in group)
        while q and remaining > 0:
            cid, need = q.popleft()
            remaining -= 1
            need -= 1
            if need > 0:
                q.append((cid, need))
        for cid, need in q:
            if need > 0:
                unfulfilled.append(cid)
    unfulfilled.sort()
    return unfulfilled
