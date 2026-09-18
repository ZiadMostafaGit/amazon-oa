# Direct numerically stable evaluation of logistic loss, gradient, and sigmoid derivatives.
from typing import List, Optional, Any
import math


def _sigmoid(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def logisticRegressionDiagnostics(features: List[List[float]], labels: List[int], weights: List[float]) -> List[List[float]]:
    m = len(features)
    n = len(weights)

    total_cost = 0.0
    residuals = []
    derivatives = []
    for i in range(m):
        row = features[i]
        z = 0.0
        for j in range(n):
            z += row[j] * weights[j]
        y = float(labels[i])
        # stable full binary cross-entropy
        total_cost += max(z, 0.0) - y * z + math.log1p(math.exp(-abs(z)))
        h = _sigmoid(z)
        residuals.append(h - y)
        derivatives.append(h * (1.0 - h))

    gradient = [0.0] * n
    for i in range(m):
        row = features[i]
        r = residuals[i]
        if r == 0.0:
            continue
        for j in range(n):
            gradient[j] += row[j] * r
    for j in range(n):
        gradient[j] /= m

    return [[total_cost / m], gradient, derivatives]
