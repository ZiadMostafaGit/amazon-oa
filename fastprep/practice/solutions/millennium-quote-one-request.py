# Exact rational arithmetic on the decimal inputs, then tick ceiling/flooring by side.
from fractions import Fraction


def quoteOneRequest(reference: float, halfSpread: float, penaltyPerUnit: float, quantity: int, side: str, tickSize: float) -> float:
    def f(x):
        return Fraction(str(x))

    adjusted = f(halfSpread) + f(penaltyPerUnit) * Fraction(quantity)
    tick = f(tickSize)
    if side == "BUY":
        raw = f(reference) + adjusted
        ticks = -((-raw.numerator * tick.denominator) // (raw.denominator * tick.numerator))
    else:
        raw = f(reference) - adjusted
        ticks = (raw.numerator * tick.denominator) // (raw.denominator * tick.numerator)
    price = ticks * tick
    scaled = price * 1000000
    units = (scaled.numerator * 2 + scaled.denominator) // (scaled.denominator * 2)
    return float(Fraction(units, 1000000))
