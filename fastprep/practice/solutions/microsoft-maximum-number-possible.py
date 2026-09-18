# Greedy left-to-right: spend replacements on early digits below 5, spend the
# allowed skips on early digits above 5.
def maximumNumberPossible(s: str, k: int) -> str:
    total = sum(1 for c in s if c != '5')
    if total < k:
        return "IMPOSSIBLE"
    skips = total - k
    left = k
    out = []
    for c in s:
        if c == '5':
            out.append(c)
            continue
        if c < '5':
            if left > 0:
                out.append('5')
                left -= 1
            else:
                out.append(c)
                skips -= 1
        else:
            if skips > 0:
                out.append(c)
                skips -= 1
            else:
                out.append('5')
                left -= 1
    return ''.join(out)
