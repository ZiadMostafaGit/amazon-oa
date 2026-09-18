# Bucket trades by (symbol, price, quantity), then two-pointer merge of time-sorted buys and sells within each bucket.
from typing import List, Optional, Any


def findUnmatchedTrades(trades: List[List[str]], tolerance: int) -> List[str]:
    buckets = {}
    for i, row in enumerate(trades):
        trade_id, symbol, side, price, quantity, timestamp = row
        key = (symbol, price, quantity)
        slot = buckets.get(key)
        if slot is None:
            slot = ([], [])
            buckets[key] = slot
        target = slot[0] if side == "BUY" else slot[1]
        target.append((int(timestamp), i))

    matched = [False] * len(trades)
    tol = int(tolerance)
    for buys, sells in buckets.values():
        buys.sort()
        sells.sort()
        bi = 0
        si = 0
        while bi < len(buys) and si < len(sells):
            bt, bidx = buys[bi]
            st, sidx = sells[si]
            diff = bt - st
            if -tol <= diff <= tol:
                matched[bidx] = True
                matched[sidx] = True
                bi += 1
                si += 1
            elif diff < 0:
                bi += 1
            else:
                si += 1

    return [trades[i][0] for i in range(len(trades)) if not matched[i]]
