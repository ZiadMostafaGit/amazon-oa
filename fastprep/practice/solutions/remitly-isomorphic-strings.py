# Two-way character mapping with dictionaries.
def isIsomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    fwd = {}
    bwd = {}
    for a, b in zip(s, t):
        if a in fwd:
            if fwd[a] != b:
                return False
        else:
            fwd[a] = b
        if b in bwd:
            if bwd[b] != a:
                return False
        else:
            bwd[b] = a
    return True
