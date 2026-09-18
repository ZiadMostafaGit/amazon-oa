# Hash map from message to the timestamp of its last successful print, with a 10-second window.
from typing import List


def shouldPrintSequence(timestamps: List[int], messages: List[str]) -> List[bool]:
    last_printed = {}
    result: List[bool] = []
    for ts, msg in zip(timestamps, messages):
        previous = last_printed.get(msg)
        if previous is None or ts - previous >= 10:
            last_printed[msg] = ts
            result.append(True)
        else:
            result.append(False)
    return result
