# Sparse day-by-day simulation over a coordinate dict, expanding only from currently infected plants.
from typing import List, Optional, Any


def solve(plants: List[List[int]], threshold: int, recoveryDays: int) -> int:
    state = {}
    for row in plants:
        r, c, s = row[0], row[1], row[2]
        state[(r, c)] = s

    infected = {}  # coord -> day on which it became infected
    for pos, s in state.items():
        if s == 1:
            infected[pos] = 0

    day = 0
    last_change = 0

    while infected:
        # count infected neighbours of every healthy plant adjacent to an infected one
        counts = {}
        for (r, c) in infected:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    p = (r + dr, c + dc)
                    if state.get(p) == 0:
                        counts[p] = counts.get(p, 0) + 1

        newly = [p for p, ct in counts.items() if ct >= threshold]
        nxt = day + 1
        recovered = [p for p, d in infected.items() if nxt - d >= recoveryDays]

        if not newly and not recovered:
            break  # nothing can ever change again

        day = nxt
        for p in recovered:
            state[p] = 2
            del infected[p]
        for p in newly:
            state[p] = 1
            infected[p] = day
        last_change = day

    return last_change
