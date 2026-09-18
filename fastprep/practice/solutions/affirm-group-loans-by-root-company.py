# parents[i] < i, so roots resolve in one forward pass; then bucket loan amounts by root.
from typing import List, Optional, Any


def groupLoans(parents: List[int], loanCompanies: List[int], amounts: List[int]) -> List[List[int]]:
    n = len(parents)
    root = [0] * n
    for i in range(n):
        p = parents[i]
        root[i] = i if p == -1 else root[p]

    totals = {}
    for idx, company in enumerate(loanCompanies):
        r = root[company]
        totals[r] = totals.get(r, 0) + amounts[idx]

    return [[r, totals[r]] for r in sorted(totals)]
