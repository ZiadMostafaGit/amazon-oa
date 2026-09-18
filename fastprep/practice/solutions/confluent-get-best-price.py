# Weighted set cover over the (at most 3) wanted items via bitmask DP in integer cents.
from typing import List, Optional, Any


def getBestPrice(menu: List[List[str]], userWants: List[str]) -> float:
    wanted = []
    index = {}
    for name in userWants:
        key = name.strip()
        if key not in index:
            index[key] = len(wanted)
            wanted.append(key)
    m = len(wanted)
    full = (1 << m) - 1
    if m == 0:
        return 0.0

    INF = float("inf")
    best = [INF] * (1 << m)
    best[0] = 0

    options = []
    for row in menu:
        price_text = str(row[0]).strip()
        cents = int(round(float(price_text) * 100))
        mask = 0
        for item in str(row[1]).split(","):
            key = item.strip()
            if key in index:
                mask |= 1 << index[key]
        if mask:
            options.append((mask, cents))

    # relax repeatedly: combinations of value meals may cover the set more cheaply
    changed = True
    while changed:
        changed = False
        for mask, cents in options:
            for state in range(1 << m):
                if best[state] == INF:
                    continue
                nxt = state | mask
                if best[state] + cents < best[nxt]:
                    best[nxt] = best[state] + cents
                    changed = True

    if best[full] == INF:
        return -1.0
    return best[full] / 100.0
