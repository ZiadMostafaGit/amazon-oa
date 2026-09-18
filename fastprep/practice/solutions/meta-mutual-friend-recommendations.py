# Approach: BFS to depth 2 over adjacency lists, counting distinct mutual friends per candidate, then sort by (-score, id).
from typing import List, Optional, Any


def recommendFriends(n: int, friendships: List[List[int]], user: int, k: int) -> List[int]:
    if k <= 0:
        return []
    adj = [[] for _ in range(n)]
    for a, b in friendships:
        adj[a].append(b)
        adj[b].append(a)

    direct = set(adj[user])
    direct.add(user)

    counts = {}
    for f in adj[user]:
        for cand in adj[f]:
            if cand in direct:
                continue
            counts[cand] = counts.get(cand, 0) + 1

    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [uid for uid, _ in ranked[:k]]
