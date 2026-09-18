# Batch the vectors into consecutive chunks and right-pad each chunk to its own max length.
from typing import List, Optional, Any


def runDataPipeline(vectors: List[List[int]], batchSize: int, padValue: int, dropLast: bool) -> List[List[int]]:
    out: List[List[int]] = []
    n = len(vectors)
    for start in range(0, n, batchSize):
        batch = vectors[start:start + batchSize]
        if dropLast and len(batch) < batchSize:
            break
        width = max(len(v) for v in batch)
        for v in batch:
            out.append(list(v) + [padValue] * (width - len(v)))
    return out
