# Sliding window with a last-seen index map.
def lengthOfLongestSubstring(s: str) -> int:
    last = {}
    best = 0
    start = 0
    for i, ch in enumerate(s):
        prev = last.get(ch)
        if prev is not None and prev >= start:
            start = prev + 1
        last[ch] = i
        if i - start + 1 > best:
            best = i - start + 1
    return best
