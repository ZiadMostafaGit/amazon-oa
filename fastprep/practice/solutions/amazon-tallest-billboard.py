from typing import List, Optional, Any


def tallestBillboard(rods: List[int]) -> int:
    # dp[diff] = tallest shorter side achievable with that height difference
    dp = {0: 0}
    for r in rods:
        nxt = dict(dp)
        for d, low in dp.items():
            # put r on the taller side
            nd = d + r
            if nxt.get(nd, -1) < low:
                nxt[nd] = low
            # put r on the shorter side
            if r <= d:
                nd, nl = d - r, low + r
            else:
                nd, nl = r - d, low + d
            if nxt.get(nd, -1) < nl:
                nxt[nd] = nl
        dp = nxt
    return dp[0]
