# Parse the trailing whitespace-separated byte count of each record and aggregate those over 5000.
from typing import List


def summarizeLargeResponses(records: List[str]) -> List[int]:
    count = 0
    total = 0
    for rec in records:
        if not rec or not rec.strip():
            continue
        last = rec.rsplit(None, 1)[-1]
        try:
            size = int(last)
        except ValueError:
            continue
        if size > 5000:
            count += 1
            total += size
    return [count, total]
