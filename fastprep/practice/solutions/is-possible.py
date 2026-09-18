# Reverse the operations from (c, d) with Euclid-style subtraction until it drops below (a, b).
def isPossible(a: int, b: int, c: int, d: int) -> str:
    while c >= a and d >= b:
        if c == a and d == b:
            return "Yes"
        if c > d:
            if d <= 0:
                break
            k = (c - a) // d
            if k <= 0:
                break
            c -= k * d
        else:
            if c <= 0:
                break
            k = (d - b) // c
            if k <= 0:
                break
            d -= k * c
    return "No"
