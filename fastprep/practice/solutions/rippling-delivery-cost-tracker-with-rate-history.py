# Offline-compressed effective times per driver + segment tree for predecessor rate lookup; money in integer cents.
from typing import List, Optional, Any
from bisect import bisect_right
from heapq import heappush, heappop


def trackDeliveryCostsWithRateHistory(operations: List[List[str]]) -> List[str]:
    # ---- pass 1: collect every effective time that can ever exist per driver
    times = {}
    for op in operations:
        name = op[0]
        if name == "ADD_DRIVER":
            times.setdefault(op[1], set()).add(0)
        elif name == "UPDATE_DRIVER_RATE":
            times.setdefault(op[1], set()).add(int(op[3]))

    axis = {}      # driver -> sorted list of candidate effective times
    rates = {}     # driver -> list of rate cents per index (None if not yet submitted)
    trees = {}     # driver -> segment tree of "rightmost assigned index"
    sizes = {}
    for d, s in times.items():
        arr = sorted(s)
        axis[d] = arr
        m = len(arr)
        sizes[d] = m
        rates[d] = [None] * m
        trees[d] = [-1] * (2 * m)

    def assign(d, idx):
        m = sizes[d]
        tree = trees[d]
        i = idx + m
        tree[i] = idx
        i >>= 1
        while i >= 1:
            tree[i] = max(tree[2 * i], tree[2 * i + 1])
            i >>= 1

    def rightmost_upto(d, pos):
        # largest assigned index in [0, pos], or -1
        m = sizes[d]
        tree = trees[d]
        lo, hi = 0 + m, pos + m + 1
        best = -1
        while lo < hi:
            if lo & 1:
                if tree[lo] > best:
                    best = tree[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if tree[hi] > best:
                    best = tree[hi]
            lo >>= 1
            hi >>= 1
        return best

    def parse_money(s):
        if "." in s:
            whole, frac = s.split(".", 1)
            frac = (frac + "00")[:2]
        else:
            whole, frac = s, "00"
        return int(whole) * 100 + int(frac)

    out = []
    total_cents = 0
    unpaid_cents = 0
    unpaid = []  # min-heap of (endTime, cost_cents) for deliveries not yet paid

    for op in operations:
        name = op[0]
        if name == "ADD_DRIVER":
            d = op[1]
            arr = axis[d]
            idx = bisect_right(arr, 0) - 1
            rates[d][idx] = parse_money(op[2])
            assign(d, idx)
        elif name == "UPDATE_DRIVER_RATE":
            d = op[1]
            eff = int(op[3])
            arr = axis[d]
            idx = bisect_right(arr, eff) - 1
            rates[d][idx] = parse_money(op[2])
            assign(d, idx)
        elif name == "RECORD_DELIVERY":
            d = op[1]
            start, end = int(op[2]), int(op[3])
            arr = axis[d]
            pos = bisect_right(arr, start) - 1
            idx = rightmost_upto(d, pos) if pos >= 0 else -1
            rate = rates[d][idx] if idx >= 0 else 0
            cost = rate * (end - start) // 3600
            total_cents += cost
            unpaid_cents += cost
            heappush(unpaid, (end, cost))
        elif name == "GET_TOTAL_COST":
            out.append(fmt(total_cents))
        elif name == "PAY_UP_TO":
            pt = int(op[1])
            while unpaid and unpaid[0][0] <= pt:
                unpaid_cents -= heappop(unpaid)[1]
        elif name == "GET_UNPAID_COST":
            out.append(fmt(unpaid_cents))
    return out


def fmt(cents: int) -> str:
    return "%d.%02d" % (cents // 100, cents % 100)
