# Split the board into residue-mod-3 chains; a coin is reachable if the nearest token
# on its left can advance there while the tokens ahead of it pile up at the chain end.


def solution(board: str) -> int:
    total = 0
    n = len(board)
    for r in range(3):
        chain = board[r::3]
        m = len(chain)
        token_positions = [i for i, c in enumerate(chain) if c == 'T']
        if not token_positions:
            continue
        first_token = token_positions[0]
        for p, c in enumerate(chain):
            if c != 'C' or p < first_token:
                continue
            ahead = sum(1 for t in token_positions if t > p)
            if p + ahead <= m - 1:
                total += 1
    return total
