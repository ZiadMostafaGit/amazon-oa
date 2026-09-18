# Bottom-up tree DP (children have larger indices): min(bulk call here, sum of children plans).
from typing import List, Optional, Any


def fileEncryptionSummary(parent: List[int], type: List[int], encrypted: List[bool], requestTime: int, fileTime: int) -> List[int]:
    n = len(parent)
    fc = [0] * n          # file nodes in subtree
    uc = [0] * n          # initially unencrypted files in subtree
    childsum = [0] * n    # sum of children's optimal costs
    dp = 0
    enc_total = 0
    unenc_total = 0
    for i in range(n - 1, -1, -1):
        if type[i] == 1:
            fc[i] = 1
            if encrypted[i]:
                uc[i] = 0
                dp = 0
                enc_total += 1
            else:
                uc[i] = 1
                dp = requestTime + fileTime
                unenc_total += 1
        else:
            if uc[i] == 0:
                dp = 0
            else:
                bulk = requestTime + fc[i] * fileTime
                dp = bulk if bulk < childsum[i] else childsum[i]
        if i > 0:
            p = parent[i]
            fc[p] += fc[i]
            uc[p] += uc[i]
            childsum[p] += dp
    return [enc_total, unenc_total, dp]
