from typing import List, Optional, Any


def closestCost(pizzas: List[int], toppings: List[int], x: int) -> int:
    m = len(toppings)
    extras = [0] + toppings[:]
    for i in range(m):
        for j in range(i + 1, m):
            extras.append(toppings[i] + toppings[j])
    best = None
    for p in pizzas:
        for e in extras:
            c = p + e
            if best is None or abs(c - x) < abs(best - x) or (abs(c - x) == abs(best - x) and c < best):
                best = c
    return best
