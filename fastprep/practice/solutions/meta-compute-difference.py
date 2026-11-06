def computeDiff(text: str) -> int:
    upper = sum(1 for ch in text if ch.isupper())
    lower = sum(1 for ch in text if ch.islower())
    return upper - lower
