# Index promotions by SKU, then price each valid product record as the min of regular and promoted totals.
from typing import List, Optional, Any


def minimumProductTotal(products: List[str], promotions: List[str]) -> int:
    pct = {}
    bxyf = {}
    for rec in promotions:
        parts = rec.split("|")
        sku = parts[0]
        kind = parts[1]
        if kind == "pct":
            pct[sku] = int(parts[2])
        elif kind == "bxyf":
            bxyf[sku] = (int(parts[2]), int(parts[3]))

    total = 0
    for rec in products:
        parts = rec.split("|")
        sku = parts[0]
        quantity = int(parts[2])
        price = int(parts[3])
        if quantity < 0 or price < 0:
            continue
        best = quantity * price
        if sku in pct:
            p = pct[sku]
            best = min(best, (quantity * price * (100 - p)) // 100)
        if sku in bxyf:
            x, y = bxyf[sku]
            charged = quantity - (quantity // (x + y)) * y
            best = min(best, charged * price)
        total += best
    return total
