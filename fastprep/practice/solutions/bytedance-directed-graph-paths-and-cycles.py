# DFS enumeration: simple paths start->target, plus simple cycles rooted at their minimum vertex.
from typing import List, Optional, Any


def enumeratePathsAndCycles(adjacency: List[List[int]], start: int, target: int) -> List[List[str]]:
    n = len(adjacency)
    paths: List[List[int]] = []
    cycles: List[List[int]] = []

    visited = [False] * n
    stack: List[int] = []

    def dfs_path(v: int) -> None:
        if v == target:
            paths.append(list(stack))
            return
        for w in adjacency[v]:
            if not visited[w]:
                visited[w] = True
                stack.append(w)
                dfs_path(w)
                stack.pop()
                visited[w] = False

    if 0 <= start < n:
        visited[start] = True
        stack.append(start)
        dfs_path(start)
        stack.pop()
        visited[start] = False

    # Each simple cycle is enumerated exactly once, from its smallest vertex.
    def dfs_cycle(root: int, v: int) -> None:
        for w in adjacency[v]:
            if w == root:
                cycles.append(list(stack))
            elif w > root and not visited[w]:
                visited[w] = True
                stack.append(w)
                dfs_cycle(root, w)
                stack.pop()
                visited[w] = False

    for root in range(n):
        visited = [False] * n
        visited[root] = True
        stack = [root]
        dfs_cycle(root, root)

    def sort_seqs(seqs: List[List[int]]) -> List[str]:
        # Lexicographic on the integer sequence; a prefix sorts before its extension.
        seqs.sort()
        return [",".join(str(x) for x in s) for s in seqs]

    return [sort_seqs(paths), sort_seqs(cycles)]
