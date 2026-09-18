# Group bids by price descending; within a group the first R bidders by timestamp get a share when R < group size.
from typing import List


def getUnallottedUsers(bids: List[List[int]], totalShares: int) -> List[int]:
    groups = {}
    for user, shares, price, ts in bids:
        groups.setdefault(price, []).append((ts, user, shares))
    remaining = totalShares
    zero = []
    for price in sorted(groups, reverse=True):
        group = sorted(groups[price])
        m = len(group)
        if remaining <= 0:
            zero.extend(user for _, user, _ in group)
            continue
        if remaining < m:
            # one share each, in timestamp order, until shares run out
            for _, user, _ in group[remaining:]:
                zero.append(user)
            remaining = 0
        else:
            total_req = sum(s for _, _, s in group)
            remaining -= min(remaining, total_req)
    zero.sort()
    return zero
