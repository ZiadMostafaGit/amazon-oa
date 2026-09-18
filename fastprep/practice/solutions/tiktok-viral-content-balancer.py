# Try every target frequency; each letter is either dropped entirely or moved to that frequency.
from collections import Counter


def balanceContentFrequency(content: str) -> int:
    counts = [c for c in Counter(content).values() if c > 0]
    if not counts:
        return 0
    top = max(counts)
    best = None
    for t in range(1, top + 1):
        cost = 0
        for c in counts:
            if c >= t:
                cost += c - t
            else:
                d = t - c
                cost += d if d < c else c
            if best is not None and cost >= best:
                break
        if best is None or cost < best:
            best = cost
    return best
