# Simulation: tally first-choice weights, then iteratively eliminate the weakest candidate.
from typing import List, Optional, Any


def electionWinners(rankings: List[List[str]], ballotCounts: List[int]) -> List[str]:
    candidates = set()
    for row in rankings:
        candidates.update(row)

    total = sum(ballotCounts)

    def tally(active):
        counts = {c: 0 for c in active}
        for row, w in zip(rankings, ballotCounts):
            for name in row:
                if name in counts:
                    counts[name] += w
                    break
        return counts

    first = tally(candidates)
    popular = min(first, key=lambda c: (-first[c], c))

    active = set(candidates)
    runoff = None
    while True:
        counts = tally(active)
        if len(active) == 1:
            runoff = next(iter(active))
            break
        best = min(counts, key=lambda c: (-counts[c], c))
        if counts[best] * 2 > total:
            runoff = best
            break
        worst = min(counts, key=lambda c: (counts[c], [-ord(ch) for ch in c]))
        active.discard(worst)

    return [popular, runoff]
