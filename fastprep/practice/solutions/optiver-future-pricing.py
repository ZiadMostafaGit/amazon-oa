# Fenwick tree over days: a dividend adds its amount at its day; a price query subtracts the prefix sum up to that day.
from typing import List

MAXD = 10 ** 6


def futurePrices(stockPrice: int, dividends: List[List[int]], operations: List[str]) -> List[int]:
    tree = [0] * (MAXD + 1)

    def add(day, amt):
        while day <= MAXD:
            tree[day] += amt
            day += day & -day

    def prefix(day):
        s = 0
        day = min(day, MAXD)
        while day > 0:
            s += tree[day]
            day -= day & -day
        return s

    divs = [list(d) for d in dividends]
    for amt, day in divs:
        add(day, amt)
    out = []
    for op in operations:
        parts = op.split()
        if parts[0] == "PRICE":
            out.append(stockPrice - prefix(int(parts[1])))
        else:
            i, amt, day = int(parts[1]) - 1, int(parts[2]), int(parts[3])
            add(divs[i][1], -divs[i][0])
            divs[i] = [amt, day]
            add(day, amt)
    return out
