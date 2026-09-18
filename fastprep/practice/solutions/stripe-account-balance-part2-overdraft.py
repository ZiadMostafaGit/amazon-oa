# Single pass over transactions with a running per-account balance map.
from typing import List, Optional, Any


def rejectedTransactions(transactions: List[str]) -> List[str]:
    balances = {}
    rejected = []
    for tx in transactions:
        idx = tx.rfind(",")
        account = tx[:idx]
        amount = int(tx[idx + 1:])
        current = balances.get(account, 0)
        if current + amount < 0:
            rejected.append(tx)
        else:
            balances[account] = current + amount
    return rejected
