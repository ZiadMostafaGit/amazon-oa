# Any character followed by 'B' forms AB or BB: a 'B' cancels whatever is on top of the stack.
def getMinimumRemainingLength(seq: str) -> int:
    size = 0
    for ch in seq:
        if ch == 'B' and size:
            size -= 1
        else:
            size += 1
    return size
