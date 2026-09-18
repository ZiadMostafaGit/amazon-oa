# Recursive-descent parse of the bracketed string, collecting (value, depth), then weight by D-d+1.


def depthSumInverse(nestedList: str) -> int:
    s = nestedList
    n = len(s)
    i = 0
    items = []  # (value, depth)

    def parse_list(depth: int) -> None:
        nonlocal i
        # s[i] == '['
        i += 1
        if i < n and s[i] == ']':
            i += 1
            return
        while True:
            if s[i] == '[':
                parse_list(depth + 1)
            else:
                j = i
                if s[j] == '-':
                    j += 1
                while j < n and s[j].isdigit():
                    j += 1
                items.append((int(s[i:j]), depth))
                i = j
            if i < n and s[i] == ',':
                i += 1
                continue
            # s[i] == ']'
            i += 1
            return

    while i < n and s[i] != '[':
        i += 1
    if i < n:
        parse_list(1)

    if not items:
        return 0
    D = max(d for _, d in items)
    return sum(v * (D - d + 1) for v, d in items)
