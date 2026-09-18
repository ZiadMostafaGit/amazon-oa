# Incremental best-price tracking: ADD-only books let best bid/ask move monotonically, with a per-price lexicographically smallest exchange map for NBBO.
from typing import List, Optional, Any


def orderBookQuotes(operations: List[str]) -> List[str]:
    bids = {}          # exchange -> {price: qty}
    asks = {}
    best_bid_px = {}   # exchange -> highest bid price
    best_ask_px = {}   # exchange -> lowest ask price
    bid_px_ex = {}     # price -> lexicographically smallest exchange quoting a bid there
    ask_px_ex = {}
    nb_bid = None      # market-wide highest bid price
    nb_ask = None      # market-wide lowest ask price
    out = []

    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "ADD":
            ex, side, price, qty = parts[1], parts[2], int(parts[3]), int(parts[4])
            if side == "BID":
                book = bids.setdefault(ex, {})
                book[price] = book.get(price, 0) + qty
                cur = best_bid_px.get(ex)
                if cur is None or price > cur:
                    best_bid_px[ex] = price
                owner = bid_px_ex.get(price)
                if owner is None or ex < owner:
                    bid_px_ex[price] = ex
                if nb_bid is None or price > nb_bid:
                    nb_bid = price
            else:
                book = asks.setdefault(ex, {})
                book[price] = book.get(price, 0) + qty
                cur = best_ask_px.get(ex)
                if cur is None or price < cur:
                    best_ask_px[ex] = price
                owner = ask_px_ex.get(price)
                if owner is None or ex < owner:
                    ask_px_ex[price] = ex
                if nb_ask is None or price < nb_ask:
                    nb_ask = price
        elif cmd == "BBO":
            ex = parts[1]
            bp = best_bid_px.get(ex)
            ap = best_ask_px.get(ex)
            left = "NA" if bp is None else "%d@%d" % (bp, bids[ex][bp])
            right = "NA" if ap is None else "%d@%d" % (ap, asks[ex][ap])
            out.append(left + "," + right)
        else:  # NBBO
            if nb_bid is None:
                left = "NA"
            else:
                ex = bid_px_ex[nb_bid]
                left = "%s:%d@%d" % (ex, nb_bid, bids[ex][nb_bid])
            if nb_ask is None:
                right = "NA"
            else:
                ex = ask_px_ex[nb_ask]
                right = "%s:%d@%d" % (ex, nb_ask, asks[ex][nb_ask])
            out.append(left + "," + right)
    return out
