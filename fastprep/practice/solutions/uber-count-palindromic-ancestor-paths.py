# XOR-bitmask prefix over root paths with a running counter maintained during an iterative DFS.
from typing import List, Optional, Any
from collections import defaultdict


def countPalindromicAncestorPaths(parent: List[int], labels: str, queries: List[int]) -> List[int]:
    n = len(parent)
    mask = [0] * n
    children = [[] for _ in range(n)]
    for i in range(n):
        b = 1 << (ord(labels[i]) - 97)
        if parent[i] == -1:
            mask[i] = b
        else:
            mask[i] = mask[parent[i]] ^ b
            children[parent[i]].append(i)

    ans = [0] * n
    cnt = defaultdict(int)
    cnt[0] = 1  # virtual parent of the root

    roots = [i for i in range(n) if parent[i] == -1]
    for root in roots:
        stack = [(root, False)]
        while stack:
            u, done = stack.pop()
            if done:
                cnt[mask[u]] -= 1
                continue
            m = mask[u]
            total = cnt[m]
            for b in range(26):
                total += cnt[m ^ (1 << b)]
            ans[u] = total
            cnt[m] += 1
            stack.append((u, True))
            for c in children[u]:
                stack.append((c, False))

    return [ans[q] for q in queries]
