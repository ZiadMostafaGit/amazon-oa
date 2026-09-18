# Parent map with iterative path compression to find each merchant's root business.
from typing import List, Optional, Any


def normalizeLoanMerchants(parents: List[str], children: List[str], loanMerchants: List[str]) -> List[str]:
    parent = {}
    for p, c in zip(parents, children):
        parent[c] = p

    def root(name: str) -> str:
        path = []
        cur = name
        while cur in parent:
            path.append(cur)
            cur = parent[cur]
        for node in path:
            parent[node] = cur
        return cur

    return [root(m) for m in loanMerchants]
