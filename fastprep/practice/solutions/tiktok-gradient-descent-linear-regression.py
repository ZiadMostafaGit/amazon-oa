# Batch gradient descent on mean squared error with synchronous bias/theta updates.
from typing import List, Optional, Any


def fitLinearRegression(xTrain: List[List[float]], yTrain: List[float], initialBias: float, initialThetas: List[float], learningRate: float, iterations: int) -> List[float]:
    n = len(xTrain)
    m = len(initialThetas)
    b = float(initialBias)
    thetas = [float(t) for t in initialThetas]
    for _ in range(iterations):
        dB = 0.0
        dT = [0.0] * m
        for i in range(n):
            row = xTrain[i]
            pred = b
            for k in range(m):
                pred += thetas[k] * row[k]
            err = yTrain[i] - pred
            dB += err
            for k in range(m):
                dT[k] += row[k] * err
        factor = -2.0 / n
        dB *= factor
        b -= learningRate * dB
        for k in range(m):
            thetas[k] -= learningRate * (dT[k] * factor)
    return [b] + thetas
