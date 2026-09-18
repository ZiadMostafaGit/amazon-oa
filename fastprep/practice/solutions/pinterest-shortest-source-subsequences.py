# Approach: greedy scan with a next-occurrence table over source, starting a new subsequence when stuck.
def shortestSourceSubsequences(source: str, target: str) -> int:
    if not target:
        return 0
    present = set(source)
    for ch in target:
        if ch not in present:
            return -1
    n = len(source)
    # nxt[i][c] = smallest index j >= i with source[j] == c, or n if none.
    nxt = [[n] * 26 for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        row = nxt[i]
        prev = nxt[i + 1]
        for c in range(26):
            row[c] = prev[c]
        row[ord(source[i]) - 97] = i
    count = 1
    pos = 0
    for ch in target:
        c = ord(ch) - 97
        j = nxt[pos][c]
        if j == n:
            count += 1
            j = nxt[0][c]
        pos = j + 1
    return count
