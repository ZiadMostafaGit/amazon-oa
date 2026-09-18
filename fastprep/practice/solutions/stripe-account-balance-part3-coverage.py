# Sequential simulation: per-account balances, platform pays the exact shortfall on any non-platform overdraft.
from typing import List, Optional, Any


def processWithCoverage(transactions: List[str], platformAccount: str) -> int:
    balances = {}
    covered = 0
    for tx in transactions:
        idx = tx.rfind(",")
        account = tx[:idx]
        amount = int(tx[idx + 1:])
        current = balances.get(account, 0)
        new_balance = current + amount
        if new_balance < 0 and account != platformAccount:
            shortfall = -new_balance
            covered += shortfall
            balances[account] = 0
            balances[platformAccount] = balances.get(platformAccount, 0) - shortfall
        else:
            balances[account] = new_balance
    return covered
