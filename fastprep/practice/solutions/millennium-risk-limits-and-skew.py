# Exact decimal arithmetic (Decimal) to apply the risk-limit rules and format the quote.
from typing import List, Optional, Any
from decimal import Decimal, ROUND_HALF_UP


def _d(x) -> Decimal:
    if isinstance(x, Decimal):
        return x
    if isinstance(x, int):
        return Decimal(x)
    return Decimal(repr(x))


def decideRequest(currentInventory: int, side: str, quantity: int, reference: float, halfSpread: float, liquidityScore: float, baseLimit: int, softFraction: float, skewCoefficient: float) -> List[str]:
    inv = _d(currentInventory)
    qty = _d(quantity)
    ref = _d(reference)
    hs = _d(halfSpread)
    liq = _d(liquidityScore)
    base = _d(baseLimit)
    softFrac = _d(softFraction)
    skewCoef = _d(skewCoefficient)

    hard = base * liq
    soft = softFrac * hard

    signed = -qty if side == "BUY" else qty
    projected = inv + signed

    if abs(projected) > hard:
        return ["reject", "null"]

    skew = -skewCoef * inv
    if side == "BUY":
        quote = ref + hs + skew
    else:
        quote = ref - hs + skew

    if abs(projected) > soft:
        action = "widen"
        if side == "BUY":
            quote = quote + hs
        else:
            quote = quote - hs
    else:
        action = "accept"

    q = quote.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    return [action, "{0:.6f}".format(q)]
