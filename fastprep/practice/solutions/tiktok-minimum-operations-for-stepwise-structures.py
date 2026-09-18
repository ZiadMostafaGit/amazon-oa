# Greedy: pick the minimal feasible base for each pattern (since only increments allowed), then sum the gaps.
from typing import List, Optional, Any


def minimumStepwiseOperations(structures: List[int]) -> int:
    n = len(structures)
    if n <= 1:
        return 0

    # Ascending: final[i] = base + i, need base + i >= structures[i]
    base_asc = max(structures[i] - i for i in range(n))
    cost_asc = sum(base_asc + i - structures[i] for i in range(n))

    # Descending: final[i] = base - i, need base - i >= structures[i]
    base_desc = max(structures[i] + i for i in range(n))
    cost_desc = sum(base_desc - i - structures[i] for i in range(n))

    return min(cost_asc, cost_desc)
