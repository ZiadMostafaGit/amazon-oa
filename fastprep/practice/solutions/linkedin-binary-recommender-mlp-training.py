# Full-batch gradient descent on a 1-hidden-layer ReLU MLP with logistic output.
import math
from typing import List, Optional, Any


def trainRecommender(members: List[List[float]], items: List[List[float]], pairs: List[List[int]], hiddenWeights: List[List[float]], hiddenBias: List[float], outputWeights: List[float], outputBias: float, steps: int, learningRate: float) -> List[float]:
    X = []
    Y = []
    for m, it, lab in pairs:
        X.append([float(v) for v in members[m]] + [float(v) for v in items[it]])
        Y.append(float(lab))
    n = len(X)
    F = len(X[0]) if n else 0
    H = len(hiddenBias)

    W = [[float(v) for v in row] for row in hiddenWeights]
    b = [float(v) for v in hiddenBias]
    w2 = [float(v) for v in outputWeights]
    b2 = float(outputBias)

    def sigmoid(z):
        if z >= 0:
            return 1.0 / (1.0 + math.exp(-z))
        e = math.exp(z)
        return e / (1.0 + e)

    for _ in range(steps):
        gW = [[0.0] * F for _ in range(H)]
        gb = [0.0] * H
        gw2 = [0.0] * H
        gb2 = 0.0
        for i in range(n):
            x = X[i]
            a = [0.0] * H
            r = [0.0] * H
            for h in range(H):
                s = b[h]
                row = W[h]
                for d in range(F):
                    s += row[d] * x[d]
                a[h] = s
                r[h] = s if s > 0.0 else 0.0
            z = b2
            for h in range(H):
                z += w2[h] * r[h]
            p = sigmoid(z)
            dz = (p - Y[i]) / n
            gb2 += dz
            for h in range(H):
                gw2[h] += dz * r[h]
                if a[h] > 0.0:
                    dr = dz * w2[h]
                    gb[h] += dr
                    grow = gW[h]
                    for d in range(F):
                        grow[d] += dr * x[d]
        for h in range(H):
            row = W[h]
            grow = gW[h]
            for d in range(F):
                row[d] -= learningRate * grow[d]
            b[h] -= learningRate * gb[h]
            w2[h] -= learningRate * gw2[h]
        b2 -= learningRate * gb2

    probs = []
    total = 0.0
    for i in range(n):
        x = X[i]
        z = b2
        for h in range(H):
            s = b[h]
            row = W[h]
            for d in range(F):
                s += row[d] * x[d]
            if s > 0.0:
                z += w2[h] * s
        p = sigmoid(z)
        probs.append(p)
        total += max(z, 0.0) - Y[i] * z + math.log1p(math.exp(-abs(z)))
    probs.append(total / n if n else 0.0)
    return probs
