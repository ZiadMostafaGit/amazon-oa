# Baseline of one_adjacent plus a DP picking an alternating seed/merge subsequence (seed ... merge ... seed).
from typing import List, Optional, Any


def getMaximumSum(no_adjacent: List[int], one_adjacent: List[int], both_adjacent: List[int]) -> int:
    n = len(no_adjacent)
    base = sum(one_adjacent)
    NEG = float('-inf')
    # after_seed: last chosen marker is a seed (valid stopping state)
    # need_seed: ready to choose the next seed (start, or right after a merge point)
    after_seed = NEG
    need_seed = 0
    for i in range(n):
        d_seed = no_adjacent[i] - one_adjacent[i]
        d_merge = both_adjacent[i] - one_adjacent[i]
        new_after = need_seed + d_seed
        if after_seed > new_after:
            new_after = after_seed
        new_need = need_seed
        if after_seed != NEG and after_seed + d_merge > new_need:
            new_need = after_seed + d_merge
        after_seed = new_after
        need_seed = new_need
    return base + after_seed
