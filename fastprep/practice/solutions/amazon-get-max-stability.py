# Sort servers by availability descending; the best subset for each availability
# threshold is every server with availability >= it, so scan prefix sums of reliability.
from typing import List


MOD = 10 ** 9 + 7


def getMaxStability(reliability: List[int], availability: List[int]) -> int:
    servers = sorted(zip(availability, reliability), key=lambda p: -p[0])
    best = 0
    running = 0
    for avail, rel in servers:
        running += rel
        cand = avail * running
        if cand > best:
            best = cand
    return best % MOD
