# Greedy pool simulation: reuse a free chair when possible, otherwise buy one.
from typing import List, Optional, Any


def minChairs(simulations: List[str]) -> List[int]:
    res = []
    for s in simulations:
        available = 0
        bought = 0
        for ch in s:
            if ch == 'C' or ch == 'U':
                if available > 0:
                    available -= 1
                else:
                    bought += 1
            else:  # 'R' or 'L' frees a chair
                available += 1
        res.append(bought)
    return res
