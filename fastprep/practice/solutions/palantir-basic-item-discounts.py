# Hash map from discount name to percent, then exact integer banker's rounding of price*pct/100 per item.
from typing import List, Optional, Any


def calculateItemDiscountTotals(itemNames: List[str], prices: List[int], discountNames: List[str], percentOff: List[int]) -> List[int]:
    pct = {}
    for i in range(min(len(discountNames), len(percentOff))):
        pct[discountNames[i]] = percentOff[i]

    subtotal = 0
    discount = 0
    for i in range(len(itemNames)):
        price = prices[i]
        subtotal += price
        p = pct.get(itemNames[i])
        if not p:
            continue
        q, r = divmod(price * p, 100)
        # round half to even on the exact rational price*p/100
        if r * 2 > 100 or (r * 2 == 100 and q % 2 == 1):
            q += 1
        discount += q
    return [subtotal, discount, subtotal - discount]
