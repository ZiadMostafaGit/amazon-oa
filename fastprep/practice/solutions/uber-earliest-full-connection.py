from typing import List, Optional, Any


def earliestFullConnection(users: List[str], logs: List[str]) -> int:
    parent = {u: u for u in users}
    size = {u: 1 for u in users}
    groups = len(parent)

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    entries = []
    for line in logs:
        t, a, b = line.split()
        entries.append((int(t), a, b))
    entries.sort(key=lambda e: e[0])
    for t, a, b in entries:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        groups -= 1
        if groups == 1:
            return t
    return -1
