# Sort uploaded intervals, take the uncovered gaps; a gap of length L needs popcount(L) power-of-two chunks.
from typing import List, Optional, Any


def minimumChunksRequired(totalPackets: int, uploadedChunks: List[List[int]]) -> int:
    intervals = sorted((int(s), int(e)) for s, e in uploadedChunks)
    total = 0
    cursor = 1
    for start, end in intervals:
        if start > cursor:
            total += bin(start - cursor).count("1")
        if end + 1 > cursor:
            cursor = end + 1
    if cursor <= totalPackets:
        total += bin(totalPackets - cursor + 1).count("1")
    return total
