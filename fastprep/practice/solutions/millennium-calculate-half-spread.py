# Exact decimal arithmetic: base*(1+vol)/liquidity, floored by the minimum, ROUND_HALF_UP to 6 dp.
from decimal import Decimal, getcontext, ROUND_HALF_UP


def _dec(x) -> Decimal:
    if isinstance(x, Decimal):
        return x
    if isinstance(x, int):
        return Decimal(x)
    # str() of a float gives the shortest repr, which recovers the intended decimal literal
    return Decimal(str(x))


def calculateHalfSpread(baseHalfSpread: float, volatility: float, liquidityScore: float, minimumHalfSpread: float) -> float:
    getcontext().prec = 60
    base = _dec(baseHalfSpread)
    vol = _dec(volatility)
    liq = _dec(liquidityScore)
    floor_ = _dec(minimumHalfSpread)

    modeled = base * (Decimal(1) + vol) / liq
    result = modeled if modeled > floor_ else floor_
    result = result.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
    return float(result)
