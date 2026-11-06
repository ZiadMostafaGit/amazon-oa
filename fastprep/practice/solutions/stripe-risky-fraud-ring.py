from typing import List, Optional, Any


def shouldBlockFraudRing(transactions: List[str], targetUser: str) -> bool:
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    score = {}
    for row in transactions:
        user, dev, card, risk = [p.strip() for p in row.split(",")]
        score[user] = int(risk)
        union(("u", user), ("d", dev))
        union(("u", user), ("c", card))
    if targetUser not in score:
        return False
    root = find(("u", targetUser))
    total = cnt = 0
    for u, s in score.items():
        if s > 0 and find(("u", u)) == root:
            total += s
            cnt += 1
    return cnt > 0 and total > 75 * cnt
