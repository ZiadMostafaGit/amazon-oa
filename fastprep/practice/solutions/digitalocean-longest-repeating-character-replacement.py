# Sliding window keeping the count of the most frequent letter; shrink when window - maxFreq > k.
def characterReplacement(s: str, k: int) -> int:
    counts = {}
    left = 0
    max_freq = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        if counts[ch] > max_freq:
            max_freq = counts[ch]
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1
            max_freq = max(counts.values()) if counts else 0
        if right - left + 1 > best:
            best = right - left + 1
    return best
