# BFS level-order traversal from root 0, returning the frontier at the requested depth.
from typing import List, Optional, Any


def solve(children: List[List[int]], level: int) -> List[int]:
    if not children or level < 0:
        return []
    frontier = [0]
    depth = 0
    while frontier and depth < level:
        nxt = []
        for node in frontier:
            if 0 <= node < len(children):
                nxt.extend(children[node])
        frontier = nxt
        depth += 1
    return list(frontier) if depth == level else []
