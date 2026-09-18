# Approach: parse rules into per-(country,product) sorted tier lists, then greedily fill tiers per item.
from typing import List


def calculateMixedShippingCost(country: str, items: List[str], rules: List[str]) -> int:
    tiers = {}
    for rule in rules:
        parts = rule.split(",")
        if len(parts) < 6:
            continue
        c, product, ttype, lo, hi, cost = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
        lo = int(lo)
        hi = None if hi.strip() == "*" else int(hi)
        tiers.setdefault((c, product), []).append((lo, hi, ttype.strip(), int(cost)))

    for key in tiers:
        tiers[key].sort(key=lambda t: t[0])

    total = 0
    for item in items:
        parts = item.split(",")
        if len(parts) < 2:
            continue
        product = parts[0]
        remaining = int(parts[1])
        for lo, hi, ttype, cost in tiers.get((country, product), []):
            if remaining <= 0:
                break
            capacity = remaining if hi is None else max(0, hi - lo)
            take = min(remaining, capacity)
            if take <= 0:
                continue
            if ttype == "fixed":
                total += cost
            else:
                total += take * cost
            remaining -= take
    return total
