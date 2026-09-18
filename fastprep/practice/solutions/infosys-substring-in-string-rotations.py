# Approach: a rotation substring check reduces to searching needle in s+s (with length guard).
def substringInAnyRotation(s: str, needle: str) -> bool:
    if not needle:
        return True
    if len(needle) > len(s):
        return False
    return needle in (s + s)
