# Direct nested-loop cross-correlation over batch, filter, output position and channel.
from typing import List, Optional, Any


def convolveBatched(input: List[List[List[int]]], batchSize: int, channels: int, kernels: List[List[int]], kernelHeight: int, kernelWidth: int, stride: int) -> List[List[List[int]]]:
    height = len(input[0])
    width = len(input[0][0])
    outH = (height - kernelHeight) // stride + 1
    outW = (width - kernelWidth) // stride + 1
    outChannels = len(kernels)
    plane_size = kernelHeight * kernelWidth

    out: List[List[List[int]]] = []
    for b in range(batchSize):
        for f in range(outChannels):
            kern = kernels[f]
            plane = []
            for oy in range(outH):
                row_vals = []
                base_r = oy * stride
                for ox in range(outW):
                    base_c = ox * stride
                    acc = 0
                    for c in range(channels):
                        img = input[b * channels + c]
                        koff = c * plane_size
                        for kr in range(kernelHeight):
                            irow = img[base_r + kr]
                            koff_row = koff + kr * kernelWidth
                            for kc in range(kernelWidth):
                                acc += irow[base_c + kc] * kern[koff_row + kc]
                    row_vals.append(acc)
                plane.append(row_vals)
            out.append(plane)
    return out
