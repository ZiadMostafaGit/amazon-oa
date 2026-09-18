# Exact integer arithmetic over 1/10000 units: stack the two percentage factors, cap at 80%, round half-to-even.
from typing import List, Optional, Any


def _round_half_even(num: int, den: int) -> int:
    q, r = divmod(num, den)
    twice = 2 * r
    if twice > den:
        return q + 1
    if twice < den:
        return q
    return q if q % 2 == 0 else q + 1


def calculateStackedDiscountTotals(itemNames: List[str], prices: List[int], categories: List[str], discountTypes: List[str], discountNames: List[str], percentOff: List[int]) -> List[int]:
    item_disc = {}
    cat_disc = {}
    for t, name, pct in zip(discountTypes, discountNames, percentOff):
        if t == "item":
            item_disc[name] = pct
        elif t == "category":
            cat_disc[name] = pct

    subtotal = 0
    total_discount = 0
    for name, price, cat in zip(itemNames, prices, categories):
        subtotal += price
        a = item_disc.get(name, 0)
        b = cat_disc.get(cat, 0)
        # discount fraction numerator over 10000
        frac_num = 10000 - (100 - a) * (100 - b)
        if frac_num > 8000:
            frac_num = 8000
        total_discount += _round_half_even(price * frac_num, 10000)

    return [subtotal, total_discount, subtotal - total_discount]
