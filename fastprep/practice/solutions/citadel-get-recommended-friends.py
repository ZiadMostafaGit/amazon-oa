# Friend-of-friend enumeration: each user has <=15 friends, so scan the <=225 two-hop
# candidates per user and count common neighbours with a hash map.
from typing import List, Optional, Any


def getRecommendedFriends(n: int, friendships: List[List[int]]) -> List[int]:
    adj = [set() for _ in range(n)]
    for a, b in friendships:
        if 0 <= a < n and 0 <= b < n and a != b:
            adj[a].add(b)
            adj[b].add(a)

    result = [-1] * n
    for y in range(n):
        counts = {}
        my_friends = adj[y]
        for f in my_friends:
            for x in adj[f]:
                if x == y or x in my_friends:
                    continue
                counts[x] = counts.get(x, 0) + 1
        if not counts:
            continue
        best_x = -1
        best_c = 0
        for x, c in counts.items():
            if c > best_c or (c == best_c and x < best_x):
                best_c = c
                best_x = x
        result[y] = best_x
    return result
