# Clamp a centered interior window of (maxVisiblePages - 2) pages between 1 and totalPages, then join with ellipses at gaps.
def paginate(currentPage: int, totalPages: int, maxVisiblePages: int) -> str:
    if totalPages <= maxVisiblePages:
        pages = list(range(1, totalPages + 1))
    else:
        width = maxVisiblePages - 2
        offset = (width - 1) // 2
        start = currentPage - offset
        lowest = 2
        highest = totalPages - 1 - width + 1
        if start < lowest:
            start = lowest
        elif start > highest:
            start = highest
        pages = [1] + list(range(start, start + width)) + [totalPages]

    tokens = []
    prev = None
    for p in pages:
        if prev is not None and p != prev + 1:
            tokens.append("...")
        tokens.append("[%d]" % p if p == currentPage else str(p))
        prev = p
    return " ".join(tokens)
