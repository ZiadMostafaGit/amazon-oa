# Simulation: hash map of account_id -> balance, applying each operation in order.
from typing import List, Optional, Any


def bankingSystemLevel1(operations: List[List[str]]) -> List[List[str]]:
    balances = {}
    results: List[List[str]] = []

    for op in operations:
        name = op[0]
        if name == "CREATE_ACCOUNT":
            account_id = op[2]
            if account_id in balances:
                results.append(["false"])
            else:
                balances[account_id] = 0
                results.append(["true"])
        elif name == "DEPOSIT":
            account_id = op[2]
            amount = int(op[3])
            if account_id not in balances:
                results.append(["null"])
            else:
                balances[account_id] += amount
                results.append([str(balances[account_id])])
        elif name == "TRANSFER":
            source, target = op[2], op[3]
            amount = int(op[4])
            if (source not in balances or target not in balances
                    or source == target or balances[source] < amount):
                results.append(["null"])
            else:
                balances[source] -= amount
                balances[target] += amount
                results.append([str(balances[source])])
        else:
            results.append(["null"])

    return results
