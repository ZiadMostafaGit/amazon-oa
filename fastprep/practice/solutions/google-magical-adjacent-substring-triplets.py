# For each split point keep the O(26) distinct letter-set bitmasks of suffixes on the left and prefixes on the right, then multiply matching counts.
def solve(text: str) -> int:
    n = len(text)
    if n < 2:
        return 0

    # right_groups[j] = list of (mask, count) over substrings text[j:k], k > j
    right_groups = [None] * (n + 1)
    cur = []
    for j in range(n - 1, -1, -1):
        bit = 1 << (ord(text[j]) - 97)
        merged = [[bit, 1]]
        for mask, cnt in cur:
            m = mask | bit
            if m == merged[-1][0]:
                merged[-1][1] += cnt
            else:
                merged.append([m, cnt])
        cur = merged
        right_groups[j] = merged

    total = 0
    left = []
    for j in range(1, n):
        bit = 1 << (ord(text[j - 1]) - 97)
        merged = [[bit, 1]]
        for mask, cnt in left:
            m = mask | bit
            if m == merged[-1][0]:
                merged[-1][1] += cnt
            else:
                merged.append([m, cnt])
        left = merged

        rmap = {}
        for mask, cnt in right_groups[j]:
            rmap[mask] = rmap.get(mask, 0) + cnt
        for mask, cnt in left:
            other = rmap.get(mask)
            if other:
                total += cnt * other

    return total
