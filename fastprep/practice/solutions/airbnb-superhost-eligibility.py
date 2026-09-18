# Aggregate count/rating-sum/recent-count per host, then apply the thresholds with integer math.
from typing import List
from collections import defaultdict


def qualifyingSuperhosts(listings: List[str], minListings: int, minAverageRating: int, minRecentPercent: int) -> List[str]:
    stats = defaultdict(lambda: [0, 0, 0])  # count, rating sum, recent count
    for record in listings:
        parts = record.split()
        host = parts[0]
        rating = int(parts[1])
        recent = int(parts[2])
        s = stats[host]
        s[0] += 1
        s[1] += rating
        s[2] += recent

    out = []
    for host in sorted(stats):
        count, total, recent = stats[host]
        if count < minListings:
            continue
        if total < minAverageRating * count:
            continue
        if recent * 100 < minRecentPercent * count:
            continue
        out.append(host)
    return out
