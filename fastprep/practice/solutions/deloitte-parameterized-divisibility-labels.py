# Direct simulation of the fizz-buzz style divisibility rules.
from typing import List, Optional, Any


def divisibilityLabels(a: int, b: int, n: int) -> List[str]:
    out = []
    for i in range(n):
        da = i % a == 0
        db = i % b == 0
        if da and db:
            out.append("AB")
        elif da:
            out.append("A")
        elif db:
            out.append("B")
        else:
            out.append(str(i))
    return out
