# Direct board simulation: per-piece pseudo-legal move rules plus a king-safety (check) filter.
from typing import List, Optional, Any


def playChess(moves: List[str]) -> List[str]:
    board = [
        list("rnbqkbnr"),
        list("pppppppp"),
        list("........"),
        list("........"),
        list("........"),
        list("........"),
        list("PPPPPPPP"),
        list("RNBQKBNR"),
    ]

    def is_white(p: str) -> bool:
        return p != '.' and p.isupper()

    def is_black(p: str) -> bool:
        return p != '.' and p.islower()

    def owns(p: str, white: bool) -> bool:
        return is_white(p) if white else is_black(p)

    def clear_path(r1: int, c1: int, r2: int, c2: int) -> bool:
        dr = (r2 > r1) - (r2 < r1)
        dc = (c2 > c1) - (c2 < c1)
        r, c = r1 + dr, c1 + dc
        while (r, c) != (r2, c2):
            if board[r][c] != '.':
                return False
            r += dr
            c += dc
        return True

    def pseudo_legal(r1: int, c1: int, r2: int, c2: int, white: bool) -> bool:
        piece = board[r1][c1]
        target = board[r2][c2]
        if target != '.' and owns(target, white):
            return False
        if target.lower() == 'k':
            return False
        kind = piece.lower()
        dr = r2 - r1
        dc = c2 - c1
        adr, adc = abs(dr), abs(dc)
        if kind == 'p':
            direction = -1 if white else 1
            start_row = 6 if white else 1
            last_row = 0 if white else 7
            if r2 == last_row:
                return False
            if dc == 0:
                if dr == direction and target == '.':
                    return True
                if (r1 == start_row and dr == 2 * direction
                        and board[r1 + direction][c1] == '.' and target == '.'):
                    return True
                return False
            if adc == 1 and dr == direction:
                return target != '.' and not owns(target, white)
            return False
        if kind == 'n':
            return (adr, adc) in ((1, 2), (2, 1))
        if kind == 'b':
            return adr == adc and adr > 0 and clear_path(r1, c1, r2, c2)
        if kind == 'r':
            return (dr == 0) != (dc == 0) and clear_path(r1, c1, r2, c2)
        if kind == 'q':
            if adr == adc and adr > 0:
                return clear_path(r1, c1, r2, c2)
            if (dr == 0) != (dc == 0):
                return clear_path(r1, c1, r2, c2)
            return False
        if kind == 'k':
            return max(adr, adc) == 1
        return False

    def attacks(r1: int, c1: int, r2: int, c2: int) -> bool:
        piece = board[r1][c1]
        kind = piece.lower()
        white = is_white(piece)
        dr = r2 - r1
        dc = c2 - c1
        adr, adc = abs(dr), abs(dc)
        if kind == 'p':
            direction = -1 if white else 1
            return dr == direction and adc == 1
        if kind == 'n':
            return (adr, adc) in ((1, 2), (2, 1))
        if kind == 'b':
            return adr == adc and adr > 0 and clear_path(r1, c1, r2, c2)
        if kind == 'r':
            return (dr == 0) != (dc == 0) and clear_path(r1, c1, r2, c2)
        if kind == 'q':
            if adr == adc and adr > 0:
                return clear_path(r1, c1, r2, c2)
            return (dr == 0) != (dc == 0) and clear_path(r1, c1, r2, c2)
        if kind == 'k':
            return max(adr, adc) == 1
        return False

    def in_check(white: bool) -> bool:
        king = 'K' if white else 'k'
        kr = kc = -1
        for r in range(8):
            for c in range(8):
                if board[r][c] == king:
                    kr, kc = r, c
                    break
            if kr != -1:
                break
        if kr == -1:
            return False
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p != '.' and owns(p, not white) and attacks(r, c, kr, kc):
                    return True
        return False

    white_turn = True
    result: List[str] = []

    for mv in moves:
        c1 = ord(mv[0]) - 97
        r1 = 8 - int(mv[1])
        c2 = ord(mv[2]) - 97
        r2 = 8 - int(mv[3])
        piece = board[r1][c1]
        ok = False
        if piece != '.' and owns(piece, white_turn) and pseudo_legal(r1, c1, r2, c2, white_turn):
            captured = board[r2][c2]
            board[r2][c2] = piece
            board[r1][c1] = '.'
            if in_check(white_turn):
                board[r1][c1] = piece
                board[r2][c2] = captured
            else:
                ok = True
        result.append("LEGAL" if ok else "ILLEGAL")
        if ok:
            white_turn = not white_turn

    for r in range(8):
        result.append(''.join(board[r]))
    return result
