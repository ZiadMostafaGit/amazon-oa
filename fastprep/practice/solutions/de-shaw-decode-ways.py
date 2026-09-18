# Linear dynamic programming: dp[i] = ways to decode prefix of length i.
def countDecodings(digits: str) -> int:
    n = len(digits)
    if n == 0:
        return 0
    prev2 = 1          # ways for prefix of length i-2
    prev1 = 1 if digits[0] != '0' else 0   # ways for prefix of length 1
    if n == 1:
        return prev1
    for i in range(1, n):
        cur = 0
        if digits[i] != '0':
            cur += prev1
        two = (ord(digits[i - 1]) - 48) * 10 + (ord(digits[i]) - 48)
        if 10 <= two <= 26:
            cur += prev2
        if cur == 0:
            return 0
        prev2, prev1 = prev1, cur
    return prev1
