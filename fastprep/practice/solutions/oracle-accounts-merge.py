# Union-Find over email addresses, then group emails by component root and sort.
from typing import List, Optional, Any


def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    parent = {}
    name_of = {}

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for acct in accounts:
        name = acct[0]
        emails = acct[1:]
        for e in emails:
            if e not in parent:
                parent[e] = e
            name_of[e] = name
        for e in emails[1:]:
            union(emails[0], e)

    groups = {}
    for e in parent:
        groups.setdefault(find(e), []).append(e)

    result = []
    for root, emails in groups.items():
        emails.sort()
        result.append([name_of[root]] + emails)

    result.sort(key=lambda row: (row[0], row[1] if len(row) > 1 else ""))
    return result
