# Expand around each center (odd and even), keeping the earliest longest match.


def longestPalindromicSubstring(text: str) -> str:
    n = len(text)
    if n == 0:
        return ""
    best_start, best_len = 0, 1

    def expand(lo: int, hi: int) -> None:
        nonlocal best_start, best_len
        while lo >= 0 and hi < n and text[lo] == text[hi]:
            lo -= 1
            hi += 1
        length = hi - lo - 1
        if length > best_len:
            best_len = length
            best_start = lo + 1

    for c in range(n):
        expand(c, c)
        expand(c, c + 1)
    return text[best_start:best_start + best_len]
