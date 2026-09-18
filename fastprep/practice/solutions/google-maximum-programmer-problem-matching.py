# Bipartite maximum matching (Hopcroft-Karp) over programmer-problem edges built from a tag -> problems index.
from typing import List
from collections import deque


def maximumProblemMatches(problemTags: List[List[str]], programmerSkills: List[List[str]]) -> int:
    tag_to_problems = {}
    for i, tags in enumerate(problemTags):
        for t in set(tags):
            tag_to_problems.setdefault(t, []).append(i)

    n = len(programmerSkills)
    m = len(problemTags)
    adj = []
    for skills in programmerSkills:
        seen = set()
        for s in set(skills):
            for p in tag_to_problems.get(s, ()):
                seen.add(p)
        adj.append(list(seen))

    INF = float('inf')
    matchL = [-1] * n
    matchR = [-1] * m
    result = 0

    while True:
        dist = [INF] * n
        q = deque()
        for u in range(n):
            if matchL[u] == -1:
                dist[u] = 0
                q.append(u)
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                w = matchR[v]
                if w == -1:
                    found = True
                elif dist[w] == INF:
                    dist[w] = dist[u] + 1
                    q.append(w)
        if not found:
            break

        it = [0] * n

        def try_augment(root):
            stack = [root]
            path = []
            while stack:
                u = stack[-1]
                advanced = False
                while it[u] < len(adj[u]):
                    v = adj[u][it[u]]
                    it[u] += 1
                    w = matchR[v]
                    if w == -1:
                        # augment along recorded path
                        path.append((u, v))
                        for uu, vv in path:
                            matchL[uu] = vv
                            matchR[vv] = uu
                        return True
                    if dist[w] == dist[u] + 1:
                        path.append((u, v))
                        stack.append(w)
                        advanced = True
                        break
                if not advanced:
                    dist[u] = INF
                    stack.pop()
                    if path:
                        path.pop()
            return False

        for u in range(n):
            if matchL[u] == -1 and try_augment(u):
                result += 1
    return result
