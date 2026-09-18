# Hash-map lookup: index the rules by (country, product), then sum quantity * per-unit cost.
from typing import List, Optional, Any


def calculateShippingCost(country: str, items: List[str], rules: List[str]) -> int:
    price = {}
    for rule in rules:
        parts = rule.split(",")
        if len(parts) < 3:
            continue
        c, product, cost = parts[0].strip(), parts[1].strip(), parts[2].strip()
        price[(c, product)] = int(cost)

    total = 0
    for entry in items:
        parts = entry.split(",")
        if len(parts) < 2:
            continue
        product, qty = parts[0].strip(), int(parts[1].strip())
        unit = price.get((country, product))
        if unit is None:
            continue
        total += qty * unit
    return total
