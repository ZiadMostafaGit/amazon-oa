# Simulate the round-robin deal, then score each 5-card hand with a category+kickers tuple.
from typing import List, Optional, Any

_RANKS = {r: i for i, r in enumerate("23456789TJQKA", start=2)}


def _score(cards: List[str]) -> tuple:
    ranks = sorted((_RANKS[c[0]] for c in cards), reverse=True)
    suits = [c[1] for c in cards]
    flush = len(set(suits)) == 1

    uniq = sorted(set(ranks), reverse=True)
    straight_high = 0
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            straight_high = uniq[0]
        elif uniq == [14, 5, 4, 3, 2]:
            straight_high = 5

    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1
    # group ranks by multiplicity, highest multiplicity then highest rank
    grouped = sorted(counts.items(), key=lambda kv: (-kv[1], -kv[0]))
    shape = [c for _, c in grouped]
    ordered = [r for r, _ in grouped]

    if straight_high and flush:
        return (8, straight_high)
    if shape[0] == 4:
        return (7,) + tuple(ordered)
    if shape[0] == 3 and shape[1] == 2:
        return (6,) + tuple(ordered)
    if flush:
        return (5,) + tuple(ranks)
    if straight_high:
        return (4, straight_high)
    if shape[0] == 3:
        return (3,) + tuple(ordered)
    if shape[0] == 2 and shape[1] == 2:
        return (2,) + tuple(ordered)
    if shape[0] == 2:
        return (1,) + tuple(ordered)
    return (0,) + tuple(ranks)


def simulatePoker(userIds: List[str], dealtCards: List[str]) -> List[str]:
    n = len(userIds)
    hands = {u: [] for u in userIds}
    log = []
    for i, card in enumerate(dealtCards):
        u = userIds[i % n]
        hands[u].append(card)
        log.append("DEAL " + u + " " + card)

    scores = {u: _score(hands[u]) for u in userIds}
    best = max(scores.values())
    winners = sorted(u for u in userIds if scores[u] == best)
    log.append("WINNERS " + ",".join(winners))
    return log
