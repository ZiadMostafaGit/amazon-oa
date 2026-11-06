from typing import List, Optional, Any


def getFraudRingSize(transactions: List[str], targetUser: str) -> int:
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    users = set()
    for row in transactions:
        user, dev, card = [p.strip() for p in row.split(",")]
        users.add(user)
        u = find(("u", user))
        for other in (("d", dev), ("c", card)):
            ro = find(other)
            if ro != u:
                parent[ro] = u
    if targetUser not in users:
        return 0
    root = find(("u", targetUser))
    return sum(1 for u in users if find(("u", u)) == root)
