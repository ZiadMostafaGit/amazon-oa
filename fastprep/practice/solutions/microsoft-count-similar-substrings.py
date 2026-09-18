# Brute force over every window of |key|: equal, or equal after one adjacent swap.
def countSimilarSubstrings(key: str, text: str) -> int:
    m = len(key)
    n = len(text)
    if m > n:
        return 0

    def similar(window: str) -> bool:
        diff = [i for i in range(m) if window[i] != key[i]]
        if not diff:
            return True
        if len(diff) == 2:
            i, j = diff
            if j == i + 1 and window[i] == key[j] and window[j] == key[i]:
                return True
        return False

    return sum(1 for start in range(n - m + 1) if similar(text[start:start + m]))
