# Sliding window with a last-seen index map, jumping the left bound past any repeat.
def lengthOfLongestSubstring(s: str) -> int:
    last = {}
    left = 0
    best = 0
    for i, ch in enumerate(s):
        prev = last.get(ch)
        if prev is not None and prev >= left:
            left = prev + 1
        last[ch] = i
        span = i - left + 1
        if span > best:
            best = span
    return best
