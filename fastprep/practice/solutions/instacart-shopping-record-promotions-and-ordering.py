# Parse/validate rows and promos, take the cheapest promo per row, then stable-sort by (frozen, aisle).
from typing import List


def _printable(s: str) -> bool:
    return len(s) > 0 and all(32 <= ord(c) <= 126 for c in s)


def _no_ws(s: str) -> bool:
    return not any(c.isspace() for c in s)


def _money(cents: int) -> str:
    return "$" + str(cents // 100) + "." + str(cents % 100).zfill(2)


def processShoppingRecords(rows: List[str], promotions: List[str]) -> List[str]:
    promo = {}
    for p in promotions:
        f = p.split('|')
        if len(f) == 3 and f[1] == 'PERCENT':
            sku = f[0]
            if not (_printable(sku) and _no_ws(sku)):
                continue
            if f[2].isdigit() and 0 <= int(f[2]) <= 100:
                promo.setdefault(sku, []).append(('P', int(f[2]), 0))
        elif len(f) == 4 and f[1] == 'BUY_X_GET_Y':
            sku = f[0]
            if not (_printable(sku) and _no_ws(sku)):
                continue
            if f[2].isdigit() and f[3].isdigit():
                x, y = int(f[2]), int(f[3])
                if x > 0 and y > 0:
                    promo.setdefault(sku, []).append(('B', x, y))

    units = 0
    base_total = 0
    promo_total = 0
    valid = []  # (frozen, aisle, order, raw)

    for raw in rows:
        f = raw.split('|')
        if len(f) != 6:
            continue
        sku, name, q_s, pr_s, aisle, fr = f
        if not (_printable(sku) and _no_ws(sku)):
            continue
        if not _printable(name):
            continue
        if not _printable(aisle) or not _no_ws(aisle):
            continue
        if not q_s.isdigit() or not pr_s.isdigit():
            continue
        if fr != 'true' and fr != 'false':
            continue
        q = int(q_s)
        price = int(pr_s)
        row_base = q * price
        units += q
        base_total += row_base
        best = row_base
        for kind, a, b in promo.get(sku, ()):
            if kind == 'P':
                cost = (row_base * (100 - a) + 50) // 100
            else:
                group = a + b
                charged = (q // group) * a + min(q % group, a)
                cost = charged * price
            if cost < best:
                best = cost
        promo_total += best
        valid.append((1 if fr == 'true' else 0, aisle, len(valid), raw))

    valid.sort(key=lambda t: (t[0], t[1], t[2]))
    out = ["units=" + str(units), "base=" + _money(base_total), "promoted=" + _money(promo_total)]
    out.extend(t[3] for t in valid)
    return out
