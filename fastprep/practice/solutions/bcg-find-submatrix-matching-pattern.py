# Brute-force every top-left corner, checking literals plus a bijective letter->digit mapping.
from typing import List, Optional, Any


def findMatchingSubmatrix(board: List[List[int]], pattern: List[str]) -> List[int]:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    k = len(pattern)
    if k == 0 or k > rows or k > cols:
        return [-1, -1]

    for top in range(rows - k + 1):
        for left in range(cols - k + 1):
            letter_to_digit = {}
            digit_to_letter = {}
            ok = True
            for r in range(k):
                prow = pattern[r]
                brow = board[top + r]
                for c in range(k):
                    ch = prow[c]
                    val = brow[left + c]
                    if ch.isdigit():
                        if val != int(ch):
                            ok = False
                            break
                    else:
                        mapped = letter_to_digit.get(ch)
                        if mapped is None:
                            if val in digit_to_letter:
                                ok = False
                                break
                            letter_to_digit[ch] = val
                            digit_to_letter[val] = ch
                        elif mapped != val:
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                return [top, left]
    return [-1, -1]
