# Fixed risk rules (>= hard cap rejects, skew negated) with exact Decimal half-up rounding.
from typing import List, Optional, Any
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 60


def _dec(x) -> Decimal:
    return Decimal(str(x))


def priceQuote(currentInventory: int, side: str, quantity: int, reference: float,
               halfSpread: float, baseLimit: int, softFraction: float,
               skewCoefficient: float) -> List[str]:
    signed = quantity if side == "BUY" else -quantity
    projected = currentInventory + signed
    hard = _dec(baseLimit)
    soft = _dec(softFraction) * hard
    if abs(_dec(projected)) >= hard:
        return ["reject", "null"]

    ref = _dec(reference)
    hs = _dec(halfSpread)
    skew = -_dec(skewCoefficient) * _dec(currentInventory)
    quote = ref + hs + skew if side == "BUY" else ref - hs + skew

    action = "accept"
    if abs(_dec(projected)) > soft:
        action = "widen"
        quote = quote + hs if side == "BUY" else quote - hs

    rounded = quote.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    return [action, format(rounded, "f")]
