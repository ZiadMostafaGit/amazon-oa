# LCS: dp[i][j] over prefixes; match -> diagonal + 1, else the better of dropping one character.
def lcsLength(text1: str, text2: str) -> int:
    prev = [0] * (len(text2) + 1)
    for a in text1:
        cur = [0]
        for j, b in enumerate(text2, 1):
            cur.append(prev[j - 1] + 1 if a == b else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]
