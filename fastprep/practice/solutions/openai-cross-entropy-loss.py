# Direct formula: mean of -ln(p[i][label[i]]) over the batch.
import math
from typing import List, Optional, Any


def crossEntropyLoss(probabilities: List[List[float]], labels: List[int]) -> float:
    n = len(labels)
    if n == 0:
        return 0.0
    total = 0.0
    for row, lab in zip(probabilities, labels):
        p = row[lab]
        if p <= 0.0:
            p = 1e-300
        total -= math.log(p)
    return total / n
