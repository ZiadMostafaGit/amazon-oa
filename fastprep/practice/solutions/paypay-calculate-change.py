# Greedy denomination breakdown in integer cents, then alphabetical sort of the bill names.
DENOMS = [
    (10000, "One Hundred"),
    (5000, "Fifty"),
    (2000, "Twenty"),
    (1000, "Ten"),
    (500, "Five"),
    (200, "Two"),
    (100, "One"),
    (50, "Half Dollar"),
    (25, "Quarter"),
    (10, "Dime"),
    (5, "Nickel"),
    (1, "Penny"),
]


def calculateChange(pp: float, cash: float) -> str:
    price_cents = int(round(pp * 100))
    cash_cents = int(round(cash * 100))
    if cash_cents < price_cents:
        return "ERROR"
    change = cash_cents - price_cents
    if change == 0:
        return "ZERO"
    out = []
    for value, name in DENOMS:
        count, change = divmod(change, value)
        out.extend([name] * count)
        if change == 0:
            break
    out.sort()
    return ",".join(out)
