# Only the first and last labels matter: full laps add one to every sector equally.
from typing import List, Optional, Any


def mostVisitedSectors(sectors: List[str], rounds: List[str]) -> List[str]:
    index = {s: i for i, s in enumerate(sectors)}
    start = index[rounds[0]]
    end = index[rounds[-1]]
    if start <= end:
        best = set(range(start, end + 1))
    else:
        best = set(range(start, len(sectors))) | set(range(0, end + 1))
    return [s for i, s in enumerate(sectors) if i in best]
