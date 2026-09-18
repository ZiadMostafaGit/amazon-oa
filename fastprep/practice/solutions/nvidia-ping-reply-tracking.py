# Single pass over replies keeping the earliest eligible arrival per request id.
from typing import List, Optional, Any


def pingRoundTripTimes(sendTimes: List[int], replyIds: List[int], replyTimes: List[int], timeout: int) -> List[int]:
    n = len(sendTimes)
    best = [-1] * n
    for j in range(len(replyIds)):
        rid = replyIds[j]
        if rid < 0 or rid >= n:
            continue
        t = replyTimes[j]
        s = sendTimes[rid]
        if t < s or t > s + timeout:
            continue
        rtt = t - s
        if best[rid] == -1 or rtt < best[rid]:
            best[rid] = rtt
    return best
