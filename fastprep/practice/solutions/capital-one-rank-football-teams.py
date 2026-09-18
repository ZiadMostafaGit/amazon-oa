# Sort team indices by (points, goal difference, goals scored) descending with index ascending; take the top two.
from typing import List, Optional, Any


def rankTeams(wins: List[int], draws: List[int], scored: List[int], conceded: List[int]) -> List[int]:
    n = len(wins)
    order = sorted(
        range(n),
        key=lambda i: (-(3 * wins[i] + draws[i]), -(scored[i] - conceded[i]), -scored[i], i),
    )
    return [order[0], order[1]]
