# Brute-force 1-NN scan with squared Euclidean distance and strict-less tie handling.
from typing import List, Optional, Any


def classifyOneNearestNeighbor(trainingFeatures: List[List[int]], trainingLabels: List[int], queries: List[List[int]]) -> List[int]:
    out = []
    for qv in queries:
        best = None
        best_label = trainingLabels[0]
        for feat, label in zip(trainingFeatures, trainingLabels):
            d = 0
            for a, b in zip(feat, qv):
                diff = a - b
                d += diff * diff
            if best is None or d < best:
                best = d
                best_label = label
        out.append(best_label)
    return out
