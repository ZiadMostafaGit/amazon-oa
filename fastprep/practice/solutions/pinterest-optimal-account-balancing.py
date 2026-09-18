# Net out balances, then backtrack settling the first nonzero debt against every opposite-signed one.
from typing import List, Optional, Any


def minTransfers(transactions: List[List[int]]) -> int:
    balance = {}
    for frm, to, amount in transactions:
        balance[frm] = balance.get(frm, 0) + amount
        balance[to] = balance.get(to, 0) - amount

    debts = [v for v in balance.values() if v != 0]
    m = len(debts)
    if m == 0:
        return 0

    def dfs(start: int) -> int:
        while start < m and debts[start] == 0:
            start += 1
        if start == m:
            return 0
        best = m  # upper bound: never more than m - 1 transfers are needed
        for j in range(start + 1, m):
            if debts[j] * debts[start] < 0:
                debts[j] += debts[start]
                best = min(best, 1 + dfs(start + 1))
                debts[j] -= debts[start]
                if debts[j] + debts[start] == 0:
                    break
        return best

    return dfs(0)
