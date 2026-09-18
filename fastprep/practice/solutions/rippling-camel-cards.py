# Rank hands by an extensible table of type classifiers, then break ties right-to-left.
from collections import Counter


def _hand_type(hand: str) -> int:
    counts = sorted(Counter(hand).values(), reverse=True)
    # ordered strongest -> weakest; new types can be inserted into this table
    table = [
        ([4], 5),        # four of a kind
        ([2, 2], 4),     # two pair
        ([3, 1], 3),     # three of a kind
        ([2, 1, 1], 2),  # one pair
        ([1, 1, 1, 1], 1),  # high card
    ]
    for shape, rank in table:
        if counts == shape:
            return rank
    return 0


def evaluate(hand1: str, hand2: str) -> str:
    t1 = _hand_type(hand1)
    t2 = _hand_type(hand2)
    if t1 != t2:
        return "HAND_1" if t1 > t2 else "HAND_2"
    for a, b in zip(reversed(hand1), reversed(hand2)):
        if a != b:
            return "HAND_1" if a > b else "HAND_2"
    return "TIE"
