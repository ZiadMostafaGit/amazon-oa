# Parse both amounts to integer cents, then greedily peel off the largest denominations.
DENOMS = [
    (10000, "ONE HUNDRED"),
    (5000, "FIFTY"),
    (2000, "TWENTY"),
    (1000, "TEN"),
    (500, "FIVE"),
    (200, "TWO"),
    (100, "ONE"),
    (50, "HALF DOLLAR"),
    (25, "QUARTER"),
    (10, "DIME"),
    (5, "NICKEL"),
    (1, "PENNY"),
]


def _to_cents(value: str) -> int:
    value = value.strip()
    if "." in value:
        whole, frac = value.split(".", 1)
    else:
        whole, frac = value, ""
    frac = (frac + "00")[:2]
    whole = whole or "0"
    return int(whole) * 100 + int(frac)


def cashRegister(purchasePrice: str, cashPaid: str) -> str:
    price = _to_cents(purchasePrice)
    paid = _to_cents(cashPaid)
    if paid < price:
        return "ERROR"
    if paid == price:
        return "ZERO"
    change = paid - price
    names = []
    for value, name in DENOMS:
        count, change = divmod(change, value)
        names.extend([name] * count)
    names.sort()
    return ",".join(names)
