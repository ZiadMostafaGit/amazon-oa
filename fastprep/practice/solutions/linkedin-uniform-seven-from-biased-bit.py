# Von Neumann debiasing with rejection sampling for 0..6, plus fixed-width rejection sampling for the p-biased bit.
from typing import List, Optional, Any


def generateRandomOutputs(biasedBits: List[int], uniformBits: List[int], pNumerator: int, pDenominator: int) -> List[int]:
    # Part 1: debias pairs, then take groups of 3 fair bits (MSB first), rejecting 7.
    uniform_value = -1
    group = []
    i = 0
    while i + 1 < len(biasedBits):
        a, b = biasedBits[i], biasedBits[i + 1]
        i += 2
        if a == b:
            continue
        group.append(0 if (a == 0 and b == 1) else 1)
        if len(group) == 3:
            value = (group[0] << 2) | (group[1] << 1) | group[2]
            group = []
            if value != 7:
                uniform_value = value
                break

    # Part 2: minimum-width groups from the fair tape, rejecting values >= pDenominator.
    width = (pDenominator - 1).bit_length()
    biased_value = -1
    j = 0
    while True:
        if width == 0:
            accepted = 0
        else:
            if j + width > len(uniformBits):
                break
            accepted = 0
            for _ in range(width):
                accepted = (accepted << 1) | uniformBits[j]
                j += 1
            if accepted >= pDenominator:
                continue
        biased_value = 0 if accepted < pNumerator else 1
        break

    return [uniform_value, biased_value]
