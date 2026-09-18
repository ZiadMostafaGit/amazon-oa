# Iterative parse into a canonical form (ints as ints, sets as frozensets) and compare.


def _parse(s: str):
    stack = []
    current = None
    i = 0
    n = len(s)
    root = None
    while i < n:
        ch = s[i]
        if ch == '{':
            new = []
            if current is not None:
                stack.append(current)
            current = new
            i += 1
        elif ch == '}':
            value = frozenset(current)
            if stack:
                current = stack.pop()
                current.append(value)
            else:
                root = value
                current = None
            i += 1
        elif ch == ',':
            i += 1
        else:
            j = i
            if s[j] in '+-':
                j += 1
            while j < n and s[j].isdigit():
                j += 1
            current.append(int(s[i:j]))
            i = j
    return root


def nestedSetsEqual(left: str, right: str) -> bool:
    return _parse(left) == _parse(right)
