# Linear DP: dp[c] = minimum adjacent-mismatch count for a prefix ending with character c.
def findMinimumInefficiency(serverType: str) -> int:
    INF = float('inf')
    first = serverType[0]
    dp0 = 0 if first in ('0', '?') else INF
    dp1 = 0 if first in ('1', '?') else INF
    for ch in serverType[1:]:
        n0 = min(dp0, dp1 + 1) if ch in ('0', '?') else INF
        n1 = min(dp1, dp0 + 1) if ch in ('1', '?') else INF
        dp0, dp1 = n0, n1
    return int(min(dp0, dp1))
