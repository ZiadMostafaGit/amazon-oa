from typing import List, Optional, Any


def guessesToFindSecret(words: List[str], secret: str) -> int:
    def match(a, b):
        return sum(x == y for x, y in zip(a, b))

    cand = sorted(words)
    for attempt in range(1, 11):
        best, best_worst = None, None
        for g in cand:  # sorted, so the first minimum is the lexicographically smallest
            buckets = [0] * 7
            for w in cand:
                buckets[match(g, w)] += 1
            worst = max(buckets)
            if best_worst is None or worst < best_worst:
                best, best_worst = g, worst
        fb = match(best, secret)
        if fb == 6:
            return attempt
        cand = [w for w in cand if match(best, w) == fb]
    return -1
