# Insight: the answer is max(last[c] - first[c]) over letters c that occur in at least two separate runs.
def longestPerfectAnagrams(s: str) -> int:
    first = {}
    last = {}
    runs = {}
    prev = None
    for i, ch in enumerate(s):
        if ch not in first:
            first[ch] = i
            runs[ch] = 1
        elif prev != ch:
            runs[ch] += 1
        last[ch] = i
        prev = ch
    best = -1
    for c, r in runs.items():
        if r >= 2:
            d = last[c] - first[c]
            if d > best:
                best = d
    return best
