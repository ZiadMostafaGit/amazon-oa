# Sliding window with a count map of at most two distinct characters.
def longestTwoDistinct(s: str) -> int:
    counts = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > 2:
            lc = s[left]
            counts[lc] -= 1
            if counts[lc] == 0:
                del counts[lc]
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
