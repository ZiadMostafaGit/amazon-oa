# Fixed recurrence: quote uses prior state, then state = (state + current impact) * decay.
from typing import List, Optional, Any


def quoteImpactStream(reference: float, impactParams: List[float], liquidityScore: float,
                      sides: List[str], quantities: List[float]) -> List[float]:
    k, decay, half_spread = impactParams[0], impactParams[1], impactParams[2]
    accumulated = 0.0
    quotes = []
    for i, side in enumerate(sides):
        direction = 1.0 if side == "BUY" else -1.0
        quotes.append(reference + direction * half_spread + accumulated)
        current = direction * k * quantities[i] * (1.0 - liquidityScore)
        accumulated = (accumulated + current) * decay
    return quotes
