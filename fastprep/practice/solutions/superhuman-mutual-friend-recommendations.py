from typing import List, Optional, Any
from collections import defaultdict


def recommendFriends(friends: List[List[str]], t: str) -> List[str]:
    adj = defaultdict(set)
    for a, b in friends:
        adj[a].add(b)
        adj[b].add(a)
    direct = adj[t]
    cnt = defaultdict(int)
    for f in direct:
        for c in adj[f]:
            if c != t and c not in direct:
                cnt[c] += 1
    ranked = sorted(cnt, key=lambda c: (-cnt[c], c))
    return ranked[:3]
