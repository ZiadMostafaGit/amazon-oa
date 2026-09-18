# Greedy: scan the rightmost position we may bump (limited by the first adjacent-duplicate in s),
# raise it to the smallest valid char, then fill the suffix with the smallest alternating chars.
def getSpecialString(s: str) -> str:
    n = len(s)
    # the untouched prefix must itself be special, so we cannot keep s beyond its
    # first pair of equal adjacent characters
    first_bad = n
    for i in range(1, n):
        if s[i] == s[i - 1]:
            first_bad = i
            break

    limit = min(n - 1, first_bad)
    for i in range(limit, -1, -1):
        left = s[i - 1] if i > 0 else None
        cand = None
        for o in range(ord(s[i]) + 1, ord('z') + 1):
            ch = chr(o)
            if ch != left:
                cand = ch
                break
        if cand is None:
            continue
        out = [s[j] for j in range(i)]
        out.append(cand)
        prev = cand
        for _ in range(i + 1, n):
            nxt = 'a' if prev != 'a' else 'b'
            out.append(nxt)
            prev = nxt
        return ''.join(out)
    return "-1"
