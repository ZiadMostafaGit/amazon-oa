from typing import List


def reconstructRootStream(distributionNodes: List[int], streamAtLeaves: List[List[int]]) -> List[int]:
    m = len(distributionNodes)
    # Heap layout: internal nodes 0..m-1, leaves m..2m; children of i are 2i+1, 2i+2.
    streams = [None] * (2 * m + 1)
    for k, row in enumerate(streamAtLeaves):
        streams[m + k] = [x for x in row if x != -1]
    for i in range(m - 1, -1, -1):
        left, right = streams[2 * i + 1], streams[2 * i + 2]
        if distributionNodes[i] == 0:
            merged = left + right
        else:
            merged = [0] * (len(left) + len(right))
            merged[0::2] = left
            merged[1::2] = right
        streams[i] = merged
        streams[2 * i + 1] = streams[2 * i + 2] = None
    return streams[0]
