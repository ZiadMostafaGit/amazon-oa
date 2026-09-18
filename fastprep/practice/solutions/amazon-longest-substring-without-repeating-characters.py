# Sliding window with last-seen index map.
def lengthOfLongestSubstring(s: str) -> int:
    last = {}
    best = 0
    start = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        if i - start + 1 > best:
            best = i - start + 1
    return best
