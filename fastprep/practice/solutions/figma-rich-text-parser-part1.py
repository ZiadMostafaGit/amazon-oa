# Approach: single pass with a depth counter; never negative and zero at the end.
from typing import List, Optional, Any


def isWellFormed(tokens: List[str]) -> bool:
    depth = 0
    for tok in tokens:
        if tok == "(":
            depth += 1
        elif tok == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0
