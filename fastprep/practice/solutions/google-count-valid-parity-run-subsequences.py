from typing import List, Optional, Any


def countValidSubsequences(nums: List[int]) -> int:
    MOD = 10**9 + 7
    # end[p][k]: subsequences whose last selected value has parity p and the
    # trailing run of parity p has length k (k = 1 or 2).
    end = [[0, 0], [0, 0]]
    for x in nums:
        p = x & 1
        q = p ^ 1
        one = (1 + end[q][0] + end[q][1]) % MOD
        two = end[p][0]
        end[p][0] = (end[p][0] + one) % MOD
        end[p][1] = (end[p][1] + two) % MOD
    return (end[0][0] + end[0][1] + end[1][0] + end[1][1]) % MOD
