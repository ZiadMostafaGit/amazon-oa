# Accumulate per-account sums in a dict, then emit the strictly positive ones sorted by id.
from typing import List, Optional, Any


def getAccountBalances(transactions: List[str]) -> List[str]:
    balances = {}
    for entry in transactions:
        account, _, amount = entry.rpartition(",")
        account = account.strip()
        balances[account] = balances.get(account, 0) + int(amount.strip())
    return ["%s:%d" % (acc, bal) for acc, bal in sorted(balances.items()) if bal > 0]
