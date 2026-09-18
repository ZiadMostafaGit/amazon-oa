# Group bids by price descending; a bidder gets nothing only if shares run out before round one reaches them.
from typing import List, Optional, Any


def getResults(bids: List[List[int]], totalShares: int) -> List[int]:
    groups: dict = {}
    for order, bid in enumerate(bids):
        user, shares, price, stamp = bid[0], bid[1], bid[2], bid[3]
        groups.setdefault(price, []).append((stamp, order, user, shares))

    remaining = totalShares
    losers: List[int] = []
    for price in sorted(groups, reverse=True):
        group = sorted(groups[price])
        if remaining >= len(group):
            # Everyone in this group gets at least one share in round one.
            wanted = sum(entry[3] for entry in group)
            remaining -= min(remaining, wanted)
        else:
            # Round one stops partway through: the tail of the group gets nothing.
            for entry in group[remaining:]:
                losers.append(entry[2])
            remaining = 0
    losers.sort()
    return losers
