# Split the pattern on '*' and greedily locate each literal segment with str.find (prefix/suffix anchored).
def matchesPattern(text: str, pattern: str) -> bool:
    if '*' not in pattern:
        return text == pattern
    segments = [s for s in pattern.split('*') if s]
    lo, hi = 0, len(text)
    if not pattern.startswith('*'):
        head = segments[0]
        if not text.startswith(head):
            return False
        lo = len(head)
        segments = segments[1:]
    if segments and not pattern.endswith('*'):
        tail = segments[-1]
        if hi - lo < len(tail) or not text.endswith(tail):
            return False
        hi -= len(tail)
        segments = segments[:-1]
    for seg in segments:
        found = text.find(seg, lo, hi)
        if found == -1:
            return False
        lo = found + len(seg)
    return True
