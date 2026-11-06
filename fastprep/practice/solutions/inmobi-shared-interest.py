from typing import List


def maxShared(friendsNodes: int, friendsFrom: List[int], friendsTo: List[int], friendsWeight: List[int]) -> int:
    n = friendsNodes
    by_label = {}
    for a, b, w in zip(friendsFrom, friendsTo, friendsWeight):
        by_label.setdefault(w, []).append((a, b))

    count = [[0] * (n + 1) for _ in range(n + 1)]
    for edges in by_label.values():
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
        groups = {}
        for v in range(1, n + 1):
            groups.setdefault(find(v), []).append(v)
        for members in groups.values():
            if len(members) < 2:
                continue
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    count[members[i]][members[j]] += 1

    best_cnt, best_prod = -1, 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            c = count[i][j]
            if c > best_cnt or (c == best_cnt and i * j > best_prod):
                best_cnt, best_prod = c, i * j
    return best_prod
