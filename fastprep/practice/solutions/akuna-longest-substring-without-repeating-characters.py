# Sliding window with last-seen index map.
def lengthOfLongestSubstring(s: str) -> int:
    last = {}
    best = 0
    start = 0
    for i, ch in enumerate(s):
        p = last.get(ch, -1)
        if p >= start:
            start = p + 1
        last[ch] = i
        if i - start + 1 > best:
            best = i - start + 1
    return best
