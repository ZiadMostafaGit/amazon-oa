# Two pointers over each maximal vowel-only block, counting windows that hold all five vowels.
VOWELS = frozenset('aeiou')


def vowelSubstring(s: str) -> int:
    total = 0
    n = len(s)
    start = 0
    while start < n:
        if s[start] not in VOWELS:
            start += 1
            continue
        end = start
        while end < n and s[end] in VOWELS:
            end += 1
        total += _countBlock(s, start, end)
        start = end
    return total


def _countBlock(s: str, lo: int, hi: int) -> int:
    counts = {}
    left = lo
    result = 0
    for right in range(lo, hi):
        ch = s[right]
        counts[ch] = counts.get(ch, 0) + 1
        # Shrink while the leftmost character is redundant.
        while counts[s[left]] > 1:
            counts[s[left]] -= 1
            left += 1
        if len(counts) == 5:
            result += left - lo + 1
    return result
