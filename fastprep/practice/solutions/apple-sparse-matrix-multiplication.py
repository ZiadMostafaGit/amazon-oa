# Sparse matrix multiplication: iterate only over nonzero entries of mat1, skipping zero factors.
from typing import List, Optional, Any


def multiply(mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
    m = len(mat1)
    k = len(mat2)
    n = len(mat2[0]) if k else 0
    product = [[0] * n for _ in range(m)]
    # Precompute nonzero columns per row of mat2
    nz2 = []
    for t in range(k):
        row = mat2[t]
        nz2.append([(j, row[j]) for j in range(n) if row[j] != 0])
    for i in range(m):
        prow = product[i]
        row1 = mat1[i]
        for t in range(k):
            a = row1[t]
            if a == 0:
                continue
            for j, b in nz2[t]:
                prow[j] += a * b
    return product
