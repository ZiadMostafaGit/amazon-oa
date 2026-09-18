# Bucket tiers by (country, product), sort by minQuantity, and fill remaining units tier by tier.
from typing import List, Optional, Any


def calculateTieredShippingCost(country: str, items: List[str], rules: List[str]) -> int:
    tiers = {}
    for rule in rules:
        parts = [p.strip() for p in rule.split(",")]
        if len(parts) < 5:
            continue
        c, product, lo, hi, cost = parts[0], parts[1], parts[2], parts[3], parts[4]
        lo_v = int(lo)
        hi_v = None if hi == "*" else int(hi)
        tiers.setdefault((c, product), []).append((lo_v, hi_v, int(cost)))

    total = 0
    for entry in items:
        parts = [p.strip() for p in entry.split(",")]
        if len(parts) < 2:
            continue
        product, qty = parts[0], int(parts[1])
        product_tiers = tiers.get((country, product))
        if not product_tiers:
            continue
        product_tiers = sorted(product_tiers, key=lambda t: t[0])
        remaining = qty
        for lo_v, hi_v, cost in product_tiers:
            if remaining <= 0:
                break
            capacity = remaining if hi_v is None else hi_v - lo_v
            if capacity <= 0:
                continue
            units = capacity if capacity < remaining else remaining
            total += units * cost
            remaining -= units
    return total
