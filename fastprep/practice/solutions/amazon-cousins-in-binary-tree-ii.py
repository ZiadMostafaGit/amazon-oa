# Parse the level-order array into index links, then BFS level by level: cousin sum = level sum - sibling-group sum.
from typing import List, Optional, Any
from collections import deque


def replaceValueInTree(levelOrder: List[str]) -> List[str]:
    tokens = list(levelOrder)
    if not tokens or tokens[0] == "null":
        return tokens

    val = {0: int(tokens[0])}
    kids = {0: []}
    q = deque([0])
    i = 1
    n = len(tokens)
    while q and i < n:
        node = q.popleft()
        for _ in range(2):
            if i >= n:
                break
            t = tokens[i]
            if t != "null":
                val[i] = int(t)
                kids[i] = []
                kids[node].append(i)
                q.append(i)
            i += 1

    result = list(tokens)
    result[0] = "0"
    level = [0]
    while level:
        nxt = []
        for node in level:
            nxt.extend(kids[node])
        if not nxt:
            break
        total = 0
        for c in nxt:
            total += val[c]
        for node in level:
            group = kids[node]
            if not group:
                continue
            gsum = 0
            for c in group:
                gsum += val[c]
            other = total - gsum
            for c in group:
                result[c] = str(other)
        level = nxt
    return result
