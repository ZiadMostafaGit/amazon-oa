# Group logs by timestamp, apply each batch atomically to an edge set, then test connectivity
# with a fresh union-find after every batch; return the first timestamp where the graph is whole.
from typing import List


def solve(n: int, logs: List[List[str]]) -> int:
    if not logs:
        return -1

    edges = set()
    i = 0
    total = len(logs)
    while i < total:
        ts = logs[i][0]
        j = i
        while j < total and logs[j][0] == ts:
            op = logs[j][1].upper()
            u = int(logs[j][2])
            v = int(logs[j][3])
            key = (u, v) if u <= v else (v, u)
            if op == "ADD":
                if u != v:
                    edges.add(key)
            else:
                edges.discard(key)
            j += 1
        i = j

        if _connected(n, edges):
            return int(ts)

    return -1


def _connected(n: int, edges) -> bool:
    if n <= 1:
        return True
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    comps = n
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            comps -= 1
    return comps == 1
