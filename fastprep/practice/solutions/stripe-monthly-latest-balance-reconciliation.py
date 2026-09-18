# Hash-map scan: keep the max-endDate row per bank/account within the month for each input, then join.
from typing import List, Optional, Any


def _latest_in_month(rows: List[str], month: str):
    best = {}
    for row in rows:
        bank, account, end_date, balance = row.split(",")
        if not end_date.startswith(month + "-"):
            continue
        key = (bank, account)
        prev = best.get(key)
        if prev is None or end_date > prev[0]:
            best[key] = (end_date, balance)
    return best


def reconcileMonthlyBalances(primaryRows: List[str], comparisonRows: List[str], month: str) -> List[str]:
    primary = _latest_in_month(primaryRows, month)
    comparison = _latest_in_month(comparisonRows, month)
    out = []
    for (bank, account) in sorted(primary):
        end_date, balance = primary[(bank, account)]
        other = comparison.get((bank, account))
        matched = other is not None and int(other[1]) == int(balance)
        out.append("%s,%s,%s,%s,%s" % (bank, account, end_date, balance, "MATCH" if matched else "NOT_MATCH"))
    return out
