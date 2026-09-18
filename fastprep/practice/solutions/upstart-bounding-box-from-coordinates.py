# Single linear scan tracking min/max of x and y.
from typing import List, Optional, Any


def boundingBoxFromCoordinates(coordinates: List[List[int]]) -> List[int]:
    min_x = min_y = None
    max_x = max_y = None
    for point in coordinates:
        x = point[0]
        y = point[1]
        if min_x is None:
            min_x = max_x = x
            min_y = max_y = y
        else:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
    return [min_x, min_y, max_x - min_x, max_y - min_y]
