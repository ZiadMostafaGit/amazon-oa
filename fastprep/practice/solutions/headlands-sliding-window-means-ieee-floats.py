# Sliding window over decoded float32 values: running double sum of finite values plus counters for NaN/+Inf/-Inf.
import math
import struct
from typing import List, Optional, Any

QNAN = 0x7FC00000
PINF = 0x7F800000
NINF = 0xFF800000


def _to_signed(u: int) -> int:
    u &= 0xFFFFFFFF
    return u - (1 << 32) if u >= (1 << 31) else u


def _bits_to_float(b: int) -> float:
    return struct.unpack('<f', struct.pack('<I', b & 0xFFFFFFFF))[0]


def _float_to_bits(x: float) -> int:
    try:
        b = struct.unpack('<I', struct.pack('<f', x))[0]
    except OverflowError:
        b = NINF if x < 0 else PINF
    if b == 0x80000000:
        b = 0
    return b


def slidingWindowMeanBits(valueBits: List[int], k: int) -> List[int]:
    n = len(valueBits)
    if k <= 0 or k > n:
        return []
    vals = [_bits_to_float(b) for b in valueBits]

    nan_cnt = 0
    pos_cnt = 0
    neg_cnt = 0
    total = 0.0
    res = []

    def add(x: float) -> None:
        nonlocal nan_cnt, pos_cnt, neg_cnt, total
        if x != x:
            nan_cnt += 1
        elif x == math.inf:
            pos_cnt += 1
        elif x == -math.inf:
            neg_cnt += 1
        else:
            total += x

    def remove(x: float) -> None:
        nonlocal nan_cnt, pos_cnt, neg_cnt, total
        if x != x:
            nan_cnt -= 1
        elif x == math.inf:
            pos_cnt -= 1
        elif x == -math.inf:
            neg_cnt -= 1
        else:
            total -= x

    for i in range(n):
        add(vals[i])
        if i >= k:
            remove(vals[i - k])
        if i >= k - 1:
            if nan_cnt or (pos_cnt and neg_cnt):
                res.append(_to_signed(QNAN))
            elif pos_cnt:
                res.append(_to_signed(PINF))
            elif neg_cnt:
                res.append(_to_signed(NINF))
            else:
                res.append(_to_signed(_float_to_bits(total / k)))
    return res
