# Count matching mirrored pairs, then format 100*m/p with exact integer half-up rounding to hundredths.
def palindromeMatchPercentage(text: str) -> str:
    n = len(text)
    pairs = n // 2
    if pairs == 0:
        return "100.00"
    matching = 0
    for i in range(pairs):
        if text[i] == text[n - 1 - i]:
            matching += 1
    num = 10000 * matching
    den = pairs
    hundredths = (2 * num + den) // (2 * den)
    return "%d.%02d" % (hundredths // 100, hundredths % 100)
