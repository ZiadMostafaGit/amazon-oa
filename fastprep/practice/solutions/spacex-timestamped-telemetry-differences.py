# Single pass pairing each timestamp with the difference of the aligned samples.
from typing import List, Optional, Any


def telemetryDifferences(timestamps: List[int], leftValues: List[int], rightValues: List[int]) -> List[List[int]]:
    return [[timestamps[i], leftValues[i] - rightValues[i]] for i in range(len(timestamps))]
