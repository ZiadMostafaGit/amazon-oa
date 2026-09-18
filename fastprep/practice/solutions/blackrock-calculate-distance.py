# Parse "name, distance" pairs, sort the distances, and emit consecutive gaps starting from 0.
def calculateDistance(input: str) -> str:
    dists = []
    for chunk in input.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(",")
        value = parts[-1].strip()
        if not value:
            continue
        dists.append(int(float(value)))
    dists.sort()
    out = []
    prev = 0
    for d in dists:
        out.append(str(d - prev))
        prev = d
    return ", ".join(out)
