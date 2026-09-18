# Build a children adjacency map, then iterative DFS from the query summing file sizes.
from typing import List, Optional, Any
from collections import defaultdict


def totalEntitySize(ids: List[str], parentIds: List[str], types: List[str], sizes: List[int], queryId: str) -> int:
    children = defaultdict(list)
    index = {}
    for i, eid in enumerate(ids):
        index[eid] = i
        p = parentIds[i]
        if p != "":
            children[p].append(eid)
    if queryId not in index:
        return 0
    total = 0
    stack = [queryId]
    while stack:
        cur = stack.pop()
        i = index[cur]
        if types[i] == "FILE":
            total += sizes[i]
        else:
            stack.extend(children.get(cur, ()))
    return total
