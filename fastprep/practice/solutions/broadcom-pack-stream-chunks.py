# Flatten the chunks in order and slice into fixed 32-byte groups.
from typing import List, Optional, Any


def packStreamChunks(chunks: List[List[int]]) -> List[List[int]]:
    flat = [b for chunk in chunks for b in chunk]
    cap = 32
    return [flat[i:i + cap] for i in range(0, len(flat), cap)]
