from typing import List, Optional, Any
from collections import deque


def shortestPath(strArr: List[str]) -> str:
    n = int(strArr[0])
    names = strArr[1:1 + n]
    nameset = set(names)
    adj = {x: [] for x in names}
    for e in strArr[1 + n:]:
        # names may contain spaces; split on a hyphen that separates two known names
        a = b = None
        for i, ch in enumerate(e):
            if ch == "-" and e[:i] in nameset and e[i + 1:] in nameset:
                a, b = e[:i], e[i + 1:]
                break
        if a is None:
            a, b = e.split("-", 1)
            adj.setdefault(a, [])
            adj.setdefault(b, [])
        adj[a].append(b)
        adj[b].append(a)
    src, dst = names[0], names[-1]
    par = {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v in adj[u]:
            if v not in par:
                par[v] = u
                q.append(v)
    if dst not in par:
        return "-1"
    path = []
    cur = dst
    while cur is not None:
        path.append(cur)
        cur = par[cur]
    return "-".join(reversed(path))
