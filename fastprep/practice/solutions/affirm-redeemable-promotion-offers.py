# Hash-map tally of net redemptions per (user, offer), then filter offers active on the cutoff date.
from typing import List, Optional, Any


def findRedeemableOffers(offers: List[str], events: List[str], cutoffDate: str) -> List[str]:
    offer_info = {}
    for o in offers:
        parts = o.split(',')
        oid, start, end, mx = parts[0], parts[1], parts[2], int(parts[3])
        offer_info[oid] = (start, end, mx)

    counts = {}
    users = []
    seen = set()
    for e in events:
        parts = e.split(',')
        uid, _date, action, oid = parts[0], parts[1], parts[2], parts[3]
        if uid not in seen:
            seen.add(uid)
            users.append(uid)
        delta = 1 if action == 'redeem' else -1
        counts[(uid, oid)] = counts.get((uid, oid), 0) + delta

    active = []
    for oid, (start, end, mx) in offer_info.items():
        if start <= cutoffDate <= end:
            active.append(oid)
    active.sort()

    result = []
    for uid in sorted(users):
        avail = [oid for oid in active
                 if counts.get((uid, oid), 0) < offer_info[oid][2]]
        if avail:
            result.append(uid + ':' + ','.join(avail))
    return result if result else ["None"]
