# Rank players inside each race by (time, id), then reduce each player's
# average rank to lowest terms with gcd.
from typing import List, Optional, Any
from math import gcd
from collections import defaultdict


def getAverageStanding(d: int, records: List[List[int]]) -> List[List[int]]:
    races = defaultdict(list)
    for race_id, player_id, time in records:
        races[race_id].append((time, player_id))

    total = [0] * d
    count = [0] * d
    for entries in races.values():
        entries.sort()
        for rank, (_, player_id) in enumerate(entries, start=1):
            if 0 <= player_id < d:
                total[player_id] += rank
                count[player_id] += 1

    result = []
    for i in range(d):
        if count[i] == 0:
            result.append([-1, -1])
        else:
            p, q = total[i], count[i]
            g = gcd(p, q)
            result.append([p // g, q // g])
    return result
