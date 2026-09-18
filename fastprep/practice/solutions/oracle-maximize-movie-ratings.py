# Linear DP over two states: current movie selected, or skipped (previous must then be selected).
from typing import List, Optional, Any


def maxMovieRatings(ratings: List[int]) -> int:
    n = len(ratings)
    selected = ratings[0]
    skipped = 0
    for i in range(1, n):
        new_selected = (selected if selected > skipped else skipped) + ratings[i]
        new_skipped = selected
        selected = new_selected
        skipped = new_skipped
    return selected if selected > skipped else skipped
