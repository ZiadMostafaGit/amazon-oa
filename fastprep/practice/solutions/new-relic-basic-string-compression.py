def compressIfShorter(text: str) -> str:
    if not text:
        return text
    parts = []
    n = len(text)
    i = 0
    total = 0
    while i < n:
        j = i
        while j < n and text[j] == text[i]:
            j += 1
        run = j - i
        piece = text[i] + str(run)
        total += len(piece)
        if total >= n:
            # cannot become strictly shorter; bail out early
            return text
        parts.append(piece)
        i = j
    compressed = "".join(parts)
    return compressed if len(compressed) < n else text
