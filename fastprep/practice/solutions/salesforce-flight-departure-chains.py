# Build next-hop map, find path roots (departures that are never arrivals), walk each chain.
from typing import List, Optional, Any


def reconstructDepartureChains(legs: List[List[str]]) -> List[List[str]]:
    nxt = {}
    arrivals = set()
    for leg in legs:
        dep, arr = leg[0], leg[1]
        nxt[dep] = arr
        arrivals.add(arr)

    roots = sorted(d for d in nxt if d not in arrivals)
    chains = []
    for root in roots:
        chain = []
        cur = root
        while cur in nxt:
            chain.append(cur)
            cur = nxt[cur]
        chains.append(chain)
    return chains
