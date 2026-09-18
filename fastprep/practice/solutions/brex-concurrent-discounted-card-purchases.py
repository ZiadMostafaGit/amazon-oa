# Straight simulation: version guard, per-color discounts from owned cards, atomic deduct.
from typing import List


def processPurchases(gems: List[int], cards: List[List[int]], requests: List[List[int]]) -> List[int]:
    balance = list(gems)
    owned = [0] * 5
    version = 0
    out = []
    for expected, idx in requests:
        if expected != version:
            out.append(-1)
            continue
        row = cards[idx]
        cost = [max(0, row[1 + c] - owned[c]) for c in range(5)]
        if all(balance[c] >= cost[c] for c in range(5)):
            for c in range(5):
                balance[c] -= cost[c]
            owned[row[0]] += 1
            version += 1
            out.append(1)
        else:
            out.append(0)
    out.append(version)
    out.extend(balance)
    out.extend(owned)
    return out
