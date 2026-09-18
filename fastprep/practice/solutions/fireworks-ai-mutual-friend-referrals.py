# Adjacency sets: count mutual friends over the target's friends, then rank by (-count, id).
from typing import List


def recommendReferrals(n: int, friendships: List[List[int]], user: int, k: int) -> List[str]:
    if k <= 0:
        return []
    adj = [[] for _ in range(n)]
    for a, b in friendships:
        adj[a].append(b)
        adj[b].append(a)
    friends = set(adj[user])
    friends.discard(user)
    d = len(friends)
    if d == 0:
        return []
    mutual = {}
    for f in friends:
        for g in adj[f]:
            if g == user or g in friends:
                continue
            mutual[g] = mutual.get(g, 0) + 1
    ranked = sorted(mutual.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    return ["%d:%.6f" % (uid, m / d) for uid, m in ranked]
